import unittest
from project import growth_squares

class TestGrowthSquares(unittest.TestCase):
    # Normal Test Cases
    # Test Case 1:
    def test_normal_case_1(self):
        self.assertEqual(growth_squares([-5, -2, 0, 3, 10]), [0, 4, 9, 25, 100])
    # Test Case 2:
    def test_normal_case_2(self):
        self.assertEqual(growth_squares([-8, -3, 2, 4, 12]), [4, 9, 16, 64, 144])
    # Test Case 3:
    def test_normal_case_3(self):
        self.assertEqual(growth_squares([-2, -1, 0]), [0, 1, 4])

    # Edge Test Cases
    # Test Case 1: (no input)
    def test_edge_case_1(self):
        self.assertEqual(growth_squares([]), [])
    # Test Case 2: (one value only)
    def test_edge_case_2(self):
        self.assertEqual(growth_squares([3]), [9])
    # Test Case 3: (duplicated values)
    def test_edge_case_3(self):
        self.assertEqual(growth_squares([-2, -2]), [4, 4])


if __name__ == "__main__":
    unittest.main()