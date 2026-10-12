"""Property checks for recurrent SCC correspondence under higher-block lifting.

Finite checks support the graph theorem in issue #48; they do not replace it.
"""
from collections import defaultdict
import itertools
import unittest

from std_tools.sft_closure import (
    allowed_blocks,
    recurrent_cyclic_edges,
    strongly_connected,
)


def endpoints(word):
    return word[:-1], word[1:]


def constituent_windows(word, length):
    return [word[i:i + length] for i in range(len(word) - length + 1)]


def recurrent_edge_sccs(edges):
    """Partition a recurrent edge set into SCC edge sets."""
    edges = list(edges)
    if not edges:
        return []

    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    vertices = set()
    for edge in edges:
        u, v = endpoints(edge)
        vertices.update((u, v))
        outgoing[u].append(v)
        incoming[v].append(u)

    # Kosaraju vertex SCCs.
    seen = set()
    order = []

    def visit(u):
        if u in seen:
            return
        seen.add(u)
        for v in outgoing[u]:
            visit(v)
        order.append(u)

    for vertex in sorted(vertices):
        visit(vertex)

    comp_of = {}
    components = []

    def collect(u, idx):
        if u in comp_of:
            return
        comp_of[u] = idx
        components[idx].add(u)
        for v in incoming[u]:
            collect(v, idx)

    for vertex in reversed(order):
        if vertex not in comp_of:
            components.append(set())
            collect(vertex, len(components) - 1)

    edge_components = [set() for _ in components]
    for edge in edges:
        u, v = endpoints(edge)
        self_idx = comp_of[u]
        # A recurrent edge must stay within one vertex SCC.
        if self_idx != comp_of[v]:
            raise AssertionError(("recurrent edge crosses SCCs", edge))
        edge_components[self_idx].add(edge)

    return [frozenset(x) for x in edge_components if x]


def binary_words(length):
    return ["".join(p) for p in itertools.product("01", repeat=length)]


class RecurrentSccLiftCorrespondence(unittest.TestCase):
    def assert_component_lift(self, alphabet, allowed, m, s, L):
        raw_s = allowed_blocks(alphabet, allowed, m, s)
        core_s = recurrent_cyclic_edges(raw_s)
        base_components = recurrent_edge_sccs(core_s)

        raw_L = allowed_blocks(alphabet, allowed, m, L)
        core_L = recurrent_cyclic_edges(raw_L)
        lifted_components = recurrent_edge_sccs(core_L)

        base_union = set(core_s)
        expected_recurrent_L = {
            word
            for word in raw_L
            if all(
                block in base_union
                for block in constituent_windows(word, s)
            )
        }
        self.assertEqual(
            set(core_L),
            expected_recurrent_L,
            (alphabet, tuple(sorted(allowed)), m, s, L, "recurrent-edge iff"),
        )

        predicted = []
        for component in base_components:
            lift = {
                word
                for word in core_L
                if all(
                    block in component
                    for block in constituent_windows(word, s)
                )
            }
            self.assertTrue(lift, (alphabet, allowed, m, s, L, component))
            self.assertTrue(strongly_connected(lift))
            predicted.append(frozenset(lift))

        # Every recurrent lifted edge uses only recurrent base edges.
        for word in core_L:
            blocks = constituent_windows(word, s)
            self.assertTrue(all(block in base_union for block in blocks))

            containing = [
                component
                for component in base_components
                if all(block in component for block in blocks)
            ]
            self.assertEqual(len(containing), 1, (word, blocks, base_components))

        self.assertEqual(
            {frozenset(c) for c in lifted_components},
            {frozenset(c) for c in predicted},
            (alphabet, tuple(sorted(allowed)), m, s, L),
        )
        self.assertEqual(len(lifted_components), len(base_components))

    def test_transient_connector_between_two_loops(self):
        # Raw connector 01 is allowed but transient. Recurrent base SCCs are
        # the two self-loops 00 and 11 and remain separate at every lift.
        allowed = {"00", "01", "11"}
        for L in range(2, 7):
            self.assert_component_lift("01", allowed, 2, 2, L)

        self.assertEqual(
            set(recurrent_cyclic_edges(allowed_blocks("01", allowed, 2, 5))),
            {"00000", "11111"},
        )

    def test_period_two_component_plus_loop_with_transient_connector(self):
        # {01,10} is a period-two recurrent SCC, {22} is a loop SCC,
        # and 12 is a one-way transient connector.
        allowed = {"01", "10", "12", "22"}
        for L in range(2, 8):
            self.assert_component_lift("012", allowed, 2, 2, L)

        # Period 2 is shorter than lifted order 6 and still survives by wrap.
        recurrent6 = set(
            recurrent_cyclic_edges(allowed_blocks("012", allowed, 2, 6))
        )
        self.assertIn("010101", recurrent6)
        self.assertIn("101010", recurrent6)
        self.assertIn("222222", recurrent6)
        self.assertNotIn("010122", recurrent6)

    def test_all_small_binary_presentations(self):
        checks = 0
        for m in (2, 3):
            blocks = binary_words(m)
            for mask in range(1 << len(blocks)):
                allowed = {
                    block
                    for i, block in enumerate(blocks)
                    if mask & (1 << i)
                }
                for s in range(m, 5):
                    core_s = recurrent_cyclic_edges(
                        allowed_blocks("01", allowed, m, s)
                    )
                    if not core_s:
                        continue
                    for L in range(s, 6):
                        self.assert_component_lift("01", allowed, m, s, L)
                        checks += 1

        self.assertGreater(checks, 250)


if __name__ == "__main__":
    unittest.main()
