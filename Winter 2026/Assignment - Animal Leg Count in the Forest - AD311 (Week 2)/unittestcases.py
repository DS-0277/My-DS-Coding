import unittest
from project import count_four_animals

class TestCountFourAnimals(unittest.TestCase):
    # Normal Test Cases
    def test_normal_case_1(self):
        animals = ['lion', 'monkey', 'deer', 'snake', 'elephant']
        self.assertEqual(count_four_animals(animals), 3)
    def test_normal_case_2(self):
        animals = ['frog', 'horse', 'spider', 'ant']
        self.assertEqual(count_four_animals(animals), 1)
    def test_normal_case_3(self):
        animals = ['lion', 'deer', 'elephant', 'horse', 'dog', 'cat']
        self.assertEqual(count_four_animals(animals), 6)
    # Edge Test Cases
    def test_edge_case_1(self):
        animals = ['snake', 'worm', 'spider']
        self.assertEqual(count_four_animals(animals), 0)
    def test_edge_case_2(self):
        animals = ['frog', 'Horse', 'spider', 'ant']
        self.assertEqual(count_four_animals(animals), 0)
    def test_edge_case_3(self):
        animals = ['frog', ' horse', 'spider', 'ant']
        self.assertEqual(count_four_animals(animals), 0)
    def test_edge_case_4(self):
        self.assertEqual(count_four_animals([]), 0)

if __name__ == "__main__":
    unittest.main()
