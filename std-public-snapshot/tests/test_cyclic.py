import unittest
from std_tools import cyclic_block_counts, empirical_min_horizon

class TestCyclicCounts(unittest.TestCase):
    def test_wrap_and_long_windows(self):
        self.assertEqual(cyclic_block_counts('ab', 3), {('a','b','a'):1, ('b','a','b'):1})
    def test_count_of_windows_is_length(self):
        for word in ('a', 'aaab', 'abab', 'bccbca'):
            for order in range(1,8):
                self.assertEqual(sum(cyclic_block_counts(word,order).values()), len(word))
    def test_one_block_counts(self):
        self.assertEqual(cyclic_block_counts('aba',1), {('a',):2,('b',):1})
    def test_empty_transformed_word(self):
        self.assertEqual(cyclic_block_counts('',2),{})
    def test_invalid_order(self):
        with self.assertRaises(ValueError):
            cyclic_block_counts('aba',0)

class TestEmpiricalHorizon(unittest.TestCase):
    def test_identity_needs_order_two_on_this_sample(self):
        self.assertEqual(empirical_min_horizon(['aabb','abab'],lambda x:x,2,4),2)
    def test_constant_per_symbol_output_has_sample_horizon_one(self):
        self.assertEqual(empirical_min_horizon(['aabb','abab','aaa'],lambda w:'x'*len(w),2,4),1)
    def test_finite_failure_is_not_infinity(self):
        self.assertIsNone(empirical_min_horizon(['aabb','abab'],lambda x:x,2,1))
    def test_reject_empty_source(self):
        with self.assertRaises(ValueError):
            empirical_min_horizon([''],lambda x:x,1,1)

if __name__=='__main__':
    unittest.main()
