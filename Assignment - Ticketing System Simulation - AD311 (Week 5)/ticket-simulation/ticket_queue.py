from collections import deque

class TicketQueue:
    # Create the empty queue
    def __init__(self):
        self.queue = deque()
    # Add ticket to the queue
    def enqueue(self, ticket):
        self.queue.append(ticket)
    # Remove ticket from the queue
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cannot dequeue an empty queue")
        return self.queue.popleft()
    # Check if the queue is empty
    def is_empty(self):
        return len(self.queue) == 0
    # Return the number of tickets in the queue
    def size(self):
        return len(self.queue)