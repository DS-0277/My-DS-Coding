class Order:
    def __init__(self, order_id, customer_name, order_details):
        self.order_id = order_id
        self.customer_name = customer_name
        self.order_details = order_details

    def __str__(self):
        return (
            "Order ID: " + str(self.order_id) +
            ", Customer: " + str(self.customer_name) +
            ", Order Details: " + str(self.order_details)
        )

class Node:
    def __init__(self, order):
        self.order = order
        self.next = None

class OrderLinkedList:
    def __init__(self):
        self.head = None

    def append(self, order):
        new_node = Node(order)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.order)
            current = current.next

    def reverse(self):
        previous = None
        current = self.head
        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        self.head = previous


orders = OrderLinkedList()
orders.append(Order(1, "Bob", "Laptop"))
orders.append(Order(2, "John", "Mouse"))
orders.append(Order(3, "Anny", "Keyboard"))


print("\nOriginal Linked List:")
orders.display()

orders.reverse()

print("\nReversed Linked List:")
orders.display()