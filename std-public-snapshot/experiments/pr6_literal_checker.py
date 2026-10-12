"""Independent bounded literal checker for STD PR #6 head private-history-omitted; no std_tools imports."""
from collections import Counter, defaultdict
from itertools import product
import json

PR6="private-history-omitted"

def cc(w,k):
    return Counter() if not w else Counter(''.join(w[(i+j)%len(w)] for j in range(k)) for i in range(len(w)))

def adm(w,A,m):
    return all(''.join(w[(i+j)%len(w)] for j in range(m)) in A for i in range(len(w)))

def tr(w,r,emit):
    return ''.join(emit(''.join(w[(i+j)%len(w)] for j in range(-r,r+1))) for i in range(len(w)))

def lin(alpha,A,m,L):
    return [''.join(p) for p in product(alpha,repeat=L) if all(''.join(p[i:i+m]) in A for i in range(L-m+1))]

def cols(alpha,A,m,r,emit,k,R):
    s=max(m,2*r+1); d=(k-1)*(R+1); L=s+d; C={}
    for e in lin(alpha,A,m,L):
        q=[emit(e[j:j+2*r+1]) for j in range(d+1)]; stream=''.join(q); c=Counter()
        for z in range(len(q[0])):
            b=stream[z:z+k]
            if len(b)!=k: raise AssertionError(('bound',e,b))
            c[b]+=1
        C[e]=c
    return L,C

def family(alpha,A,m,r,emit,k,R,N):
    L,C=cols(alpha,A,m,r,emit,k,R); checked=short=empty=outshort=0
    for n in range(1,N+1):
        for p in product(alpha,repeat=n):
            w=''.join(p)
            if not adm(w,A,m): continue
            y=tr(w,r,emit); direct=cc(y,k); pred=Counter()
            for i in range(n): pred.update(C[''.join(w[(i+j)%n] for j in range(L))])
            if direct != +pred: raise AssertionError((w,y,direct,+pred,L))
            checked+=1; short+=n<L; empty+=not y; outshort+=0<len(y)<k
    return dict(L=L,columns=len(C),words=checked,period_lt_L=short,empty_outputs=empty,nonempty_output_lt_k=outshort)

def words(alpha,A,m,N):
    return [''.join(p) for n in range(1,N+1) for p in product(alpha,repeat=n) if adm(''.join(p),A,m)]

def conflict(W,T,h,k):
    seen={}
    for w in W:
        a=tuple(sorted(cc(w,h).items())); b=tuple(sorted(cc(T(w),k).items()))
        if a in seen and seen[a][1]!=b: return [seen[a][0],w]
        seen[a]=(w,b)

def recurrent(E):
    adj=defaultdict(list)
    for e in E: adj[e[:-1]].append(e[1:])
    def reach(s,t):
        Q=[s]; S=set()
        while Q:
            u=Q.pop()
            if u==t:return True
            if u in S:continue
            S.add(u);Q.extend(adj[u])
        return False
    return [e for e in E if reach(e[1:],e[:-1])]

def run():
    A3={a+b for a in '012' for b in '012' if a+b!='00'}
    f1=family('012',A3,2,0,lambda w:{'0':'','1':'a','2':'b'}[w],2,1,7)
    A={''.join(p) for p in product('01',repeat=3)}-{'000'}
    f2=family('01',A,3,1,lambda w:'' if w[1]=='0' else ('ab' if w[0]=='0' else 'b'),3,2,9)
    f3=family('01',{'0','1'},1,0,lambda w:'' if w=='0' else 'x',1,0,9)
    full=[''.join(p) for n in range(1,9) for p in product('01',repeat=n)]
    no00=words('01',{'01','10','11'},2,12); ident=lambda w:w
    if conflict(no00,ident,1,2): raise AssertionError('no00 C1->C2')
    X,Y='011101','011011'
    if cc(X,2)!=cc(Y,2) or cc(X,3)==cc(Y,3): raise AssertionError('named witness')
    issue7={}
    for name,A2 in [('transient',{'00','01'}),('empty',{'01'}),('multi',{'00','01','11'})]:
        E=lin('01',A2,2,2); W=words('01',A2,2,10); issue7[name]=dict(raw=E,recurrent=recurrent(E),word_count=len(W))
    return {
      'status':'pass','pr6_head':PR6,'matrix_whole_word_checks':f1['words']+f2['words']+f3['words'],
      'families':[f1,f2,f3],
      'horizon':{'full_identity_k2_h1_witness':conflict(full,ident,1,2),'no00_words_through_12':len(no00),
                 'no00_identity_k2_h1_conflict':conflict(no00,ident,1,2),'no00_identity_k3_h2_witness':[X,Y]},
      'issue7':issue7,
      'scope':'bounded exact computation; not a general theorem; support-pair LP proof not audited'
    }
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
