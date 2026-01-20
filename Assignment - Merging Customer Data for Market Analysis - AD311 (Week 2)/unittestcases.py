import unittest
from project import mergeCustomerData

class TestMergeCustomerData(unittest.TestCase):

    # Normal Test Cases
    def test_normal_case_1(self):
        customerData1 = [101,104,107,0,0,0]
        customerData2 = [102,105,108]
        mergeCustomerData(customerData1, 3, customerData2, 3)
        self.assertEqual(customerData1, [101, 102, 104, 105, 107, 108])
    def test_normal_case_2(self):
        customerData1 = [1,2,5,0,0,0]
        customerData2 = [3,4,6]
        mergeCustomerData(customerData1, 3, customerData2, 3)
        self.assertEqual(customerData1, [1,2,3,4,5,6])
    def test_normal_case_3(self):
        customerData1 = [1,2,3,0,0,0]
        customerData2 = [4,5,6]
        mergeCustomerData(customerData1, 3, customerData2, 3)
        self.assertEqual(customerData1, [1,2,3,4,5,6])

    # Edge Test Cases
    def test_edge_case_1(self):
        customerData1 = [103]
        customerData2 = []
        mergeCustomerData(customerData1, 1, customerData2, 0)
        self.assertEqual(customerData1, [103])
    def test_edge_case_2(self):
        customerData1 = [1,2,3,0,0,0]
        customerData2 = [1,2,3]
        mergeCustomerData(customerData1, 3, customerData2, 3)
        self.assertEqual(customerData1, [1,1,2,2,3,3])
    def test_edge_case_3(self):
        customerData1 = [0,0,0]
        customerData2 = [1,2,3]
        mergeCustomerData(customerData1, 0, customerData2, 3)
        self.assertEqual(customerData1, [1,2,3])


if __name__ == "__main__":
    unittest.main()