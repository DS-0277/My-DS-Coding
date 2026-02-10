import time
import random
from ticket import Ticket
from ticket_queue import TicketQueue

def generate_tickets(queue, count):
    for i in range(1, count + 1):
        ticket = Ticket(i)
        queue.enqueue(ticket)
        print("Generated:", ticket)
        time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    queue = TicketQueue()
    generate_tickets(queue, 3)
    print("\nTickets waiting in queue:", queue.size())


# Normal Cases:
# Case 1: 1
# Case 2: 3
# Case 10: 10

# Edge Cases:
# Case 1: 0
# Case 2: -1
# Case 3: 'a'