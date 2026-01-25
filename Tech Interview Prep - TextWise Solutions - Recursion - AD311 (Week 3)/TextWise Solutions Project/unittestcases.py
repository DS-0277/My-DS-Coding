import unittest
from project import reverse_string

class TestReverseString(unittest.TestCase):
    # Normal Cases
    def test_normal_case_1(self):
        self.assertEqual(reverse_string("abc"), "cba")
    def test_normal_case_2(self):
        self.assertEqual(reverse_string("hello"), "olleh")
    def test_normal_case_3(self):
        self.assertEqual(reverse_string("TextWise"), "esiWtxeT")

    # Edge Cases
    def test_edge_case_1(self):
        self.assertEqual(reverse_string(""), "")
    def test_edge_case_2(self):
        self.assertEqual(reverse_string(" "), " ")
    def test_edge_case_3(self):
        self.assertEqual(reverse_string("a"), "a")


if __name__ == "__main__":
    unittest.main()