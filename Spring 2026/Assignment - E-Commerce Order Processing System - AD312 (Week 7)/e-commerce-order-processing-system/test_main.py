from main import Order, OrderLinkedList

# Normal Test Cases

# Case 1: Test whether the node is successfully inserted into the linked list
def test_append():
    orders = OrderLinkedList()
    orders.append(Order(1, "Bob", "Laptop"))
    assert orders.head.order.order_id == 1

# Case 2: Test whether the multiple nodes could be inserted into the linked list
def test_multiple():
    orders = OrderLinkedList()
    orders.append(Order(1, "Bob", "Laptop"))
    orders.append(Order(2, "John", "Mouse"))
    orders.append(Order(3, "Anny", "Keyboard"))
    assert orders.head.order.order_id == 1

# Case 3: Test whether the reverse function works
def test_reverse():
    orders = OrderLinkedList()
    orders.append(Order(1, "Bob", "Laptop"))
    orders.append(Order(2, "John", "Mouse"))
    orders.reverse()
    assert orders.head.order.order_id == 2


# Edge Test Cases

# Case 1: Test when there is an empty linked list
def test_empty():
    orders = OrderLinkedList()
    assert orders.head is None

# Case 2: Test when we reverse for one node
def test_reverse_itself():
    orders = OrderLinkedList()
    orders.append(Order(1, "Bob", "Laptop"))
    orders.reverse()
    assert orders.head.order.order_id == 1

# Case 3: Test when we reverse twice
def test_reverse_twice():
    orders = OrderLinkedList()
    orders.append(Order(1, "Bob", "Laptop"))
    orders.append(Order(2, "John", "Mouse"))
    orders.reverse()
    orders.reverse()
    assert orders.head.order.order_id == 1