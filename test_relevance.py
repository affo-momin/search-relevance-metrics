import unittest

from relevance import dcg, ndcg, precision, reciprocal_rank


class TestRelevance(unittest.TestCase):
    def test_perfect_order_ndcg_is_one(self):
        self.assertAlmostEqual(ndcg([4, 3, 2, 1, 0], 5), 1.0)

    def test_worse_order_scores_lower(self):
        self.assertLess(ndcg([0, 1, 2, 3, 4], 5), ndcg([4, 3, 2, 1, 0], 5))

    def test_dcg_known_value(self):
        # (2^3-1)/log2(2) + (2^2-1)/log2(3) = 7 + 1.8928
        self.assertAlmostEqual(dcg([3, 2], 2), 7 + 3 / 1.5849625, places=4)

    def test_precision_and_rr(self):
        self.assertAlmostEqual(precision([4, 1, 3, 0], 4), 0.5)
        self.assertAlmostEqual(reciprocal_rank([1, 2, 3]), 1 / 3)
        self.assertEqual(reciprocal_rank([0, 1]), 0.0)

    def test_all_zero(self):
        self.assertEqual(ndcg([0, 0, 0], 3), 0.0)


if __name__ == "__main__":
    unittest.main()
