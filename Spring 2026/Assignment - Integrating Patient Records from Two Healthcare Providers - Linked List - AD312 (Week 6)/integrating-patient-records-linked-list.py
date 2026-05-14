class Node:
    def __init__(self, ssn, age, full_name):
        self.ssn = ssn
        self.age = age
        self.full_name = full_name
        self.next = None

def mergedPatientRecords(list1, list2):
    dummy = Node(0, 0, "")
    current = dummy

    while list1 and list2:
        if list1.ssn <= list2.ssn:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    if list1:
        current.next = list1
    if list2:
        current.next = list2

    return dummy.next


def printList(head):
    current = head
    while current:
        print(
            "SSN:", current.ssn,
            "Age:", current.age,
            "Full Name:", current.full_name
        )
        current = current.next

# Create List1
a = Node(100, 20, "Mike")
b = Node(250, 40, "John")
c = Node(300, 60, "Michael")

a.next = b
b.next = c

list1 = a

# Create List2
d = Node(120, 35, "Bob")
e = Node(250, 15, "Sarah")
f = Node(350, 50, "Andrew")

d.next = e
e.next = f

list2 = d


merge = mergedPatientRecords(list1, list2)

print("Merged Patient Records:")
printList(merge)


# TEST CASES

# Normal Cases

# Case 1: Normal Merge
# list1: 100, 250, 300
# list2: 120, 250, 350
# Output: 100, 120, 250, 250, 300, 350

# Case 2: Duplicate Merge
# list1: 100, 250
# list2: 100, 250
# Output: 100, 100, 250, 250

# Case 3: list1 is generally smaller than list2
# list1: 100, 150
# list2: 200, 250
# Output: 100, 150, 200, 250


# Edge Cases

# Case 1: list1 is blank
# list1: (empty)
# list2: 200, 250
# Output: 200, 250

# Case 2: list2 is blank
# list1: 200, 250
# list2: (empty)
# Output: 200, 250

# Case 3: both list1 and list2 are blank
# list1: (empty)
# list2: (empty)
# Output: (empty)




