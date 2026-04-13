import unittest
from project import duplicate_zero

class TestDuplicateZero(unittest.TestCase):
    # Normal Test Cases
    def test_normal_case_1(self):
        self.assertEqual(duplicate_zero([4, 0, 1, 3, 0, 2, 5, 0]), [4, 0, 0, 1, 3, 0, 0, 2])
    def test_normal_case_2(self):
        self.assertEqual(duplicate_zero([3, 2, 1]), [3, 2, 1])
    def test_normal_case_3(self):
        self.assertEqual(duplicate_zero([1, 0, 2, 3, 4]), [1, 0, 0, 2, 3])
        
    # Edge Test Cases
    def test_edge_case_1(self):
        self.assertEqual(duplicate_zero([0]), [0])
    def test_edge_case_2(self):
        self.assertEqual(duplicate_zero([3, -2, 1]), [3, -2, 1])
    def test_edge_case_3(self):
        self.assertEqual(duplicate_zero(["three", "two", "one"]), ["three", "two", "one"])
    

if __name__ == "__main__":
    unittest.main()