import math
import unittest

from range_minimum_query import RMQ


class TestRMQ(unittest.TestCase):
    def test_simple_interval(self):
        r = RMQ([3, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(r.query(0, 8), 1)
        self.assertEqual(r.query(2, 5), 1)
        self.assertEqual(r.query(0, 1), 3)
        self.assertEqual(r.query(6, 8), 2)

    def test_full_range(self):
        r = RMQ([7, 2, 5, 1, 8, 3])
        self.assertEqual(r.query(0, 6), 1)

    def test_single_element(self):
        r = RMQ([42, 7, 13])
        self.assertEqual(r.query(1, 2), 7)
        self.assertEqual(r.query(0, 1), 42)
        self.assertEqual(r.query(2, 3), 13)

    def test_increasing_values(self):
        r = RMQ([1, 2, 3, 4, 5])
        for i in range(5):
            for j in range(i + 1, 6):
                self.assertEqual(r.query(i, j), i + 1)

    def test_decreasing_values(self):
        r = RMQ([5, 4, 3, 2, 1])
        for i in range(5):
            for j in range(i + 1, 6):
                self.assertEqual(r.query(i, j), 6 - j)

    def test_brute_force_random(self):
        import random
        rng = random.Random(20240601)
        for _ in range(200):
            n = rng.randint(1, 40)
            data = [rng.randint(-50, 50) for _ in range(n)]
            r = RMQ(data)
            for _ in range(20):
                i = rng.randint(0, n - 1)
                j = rng.randint(i + 1, n)
                self.assertEqual(r.query(i, j), min(data[i:j]))

    def test_negative_numbers(self):
        r = RMQ([-5, -2, -8, -1, -9])
        self.assertEqual(r.query(0, 5), -9)
        self.assertEqual(r.query(0, 3), -8)
        self.assertEqual(r.query(2, 4), -8)

    def test_strings(self):
        # Comparison is by ``<``; strings work the same as ints.
        r = RMQ(["banana", "apple", "cherry", "apricot"])
        self.assertEqual(r.query(0, 4), "apple")
        self.assertEqual(r.query(2, 4), "apricot")

    def test_tuple_values(self):
        # Tuples are ordered lexicographically, which is fine for the
        # sparse table; this just exercises non-numeric comparables.
        r = RMQ([(2, 1), (1, 9), (1, 2), (3, 0)])
        self.assertEqual(r.query(0, 4), (1, 2))
        self.assertEqual(r.query(0, 2), (1, 9))

    def test_power_of_two_length(self):
        n = 16
        data = list(range(n, 0, -1))
        r = RMQ(data)
        self.assertEqual(r.query(0, n), 1)
        self.assertEqual(r.query(0, 8), n - 7)
        self.assertEqual(r.query(8, 16), 1)

    def test_non_power_of_two_length(self):
        n = 17
        data = list(range(n, 0, -1))
        r = RMQ(data)
        self.assertEqual(r.query(0, n), 1)
        self.assertEqual(r.query(0, 8), n - 7)
        self.assertEqual(r.query(9, 17), 1)

    def test_len(self):
        self.assertEqual(len(RMQ([1, 2, 3])), 3)
        self.assertEqual(len(RMQ([])), 0)

    def test_empty_data(self):
        r = RMQ([])
        with self.assertRaises(IndexError):
            r.query(0, 0)

    def test_empty_interval(self):
        r = RMQ([1, 2, 3])
        with self.assertRaises(IndexError):
            r.query(1, 1)

    def test_lo_out_of_range(self):
        r = RMQ([1, 2, 3])
        with self.assertRaises(IndexError):
            r.query(-1, 2)
        with self.assertRaises(IndexError):
            r.query(3, 3)

    def test_hi_out_of_range(self):
        r = RMQ([1, 2, 3])
        with self.assertRaises(IndexError):
            r.query(0, 4)
        with self.assertRaises(IndexError):
            r.query(2, 4)

    def test_inverted_interval(self):
        r = RMQ([1, 2, 3])
        with self.assertRaises(IndexError):
            r.query(2, 1)

    def test_accepts_generator(self):
        # Any sequence is accepted; generators are materialised into a
        # list during construction.
        r = RMQ(iter([5, 3, 4, 1, 2]))
        self.assertEqual(r.query(0, 5), 1)
        self.assertEqual(r.query(0, 2), 3)

    def test_large_input(self):
        n = 2000
        data = list(range(n, 0, -1))
        r = RMQ(data)
        self.assertEqual(r.query(0, n), 1)
        self.assertEqual(r.query(n // 2, n), 1)
        self.assertEqual(r.query(0, n // 2), n - n // 2 + 1)


if __name__ == "__main__":
    unittest.main()
