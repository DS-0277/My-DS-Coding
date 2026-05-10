class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def isHealthRecordSymmetric(head):
    values = []
    current = head
    while current is not None:
        values.append(current.value)
        current = current.next
    return values == values[::-1]

node1 = Node(70)
node2 = Node(80)
node3 = Node(90)
node4 = Node(80)
node5 = Node(70)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5


print(isHealthRecordSymmetric(node1))

# TEST CASES

# Normal Test Cases
# Case 1: (70, 80, 90, 80, 70) ==> Show "True" as expected
# Case 2: (70, 80, 80, 70) ==> Show "True" as expected
# Case 3: (70, 80, 90) ==> Show "False" as expected


# Edge Test Cases
# Case 1: (70) ==> Show "True" as expected
# Case 2: (70, 70) ==> Show "True" as expected
# Case 3: (70, 80, 90, 80, 50) ==> Show "False" as expected

# Time and Space Complexity ==> O(n)