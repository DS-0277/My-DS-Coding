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
    generate_tickets(queue, 10)
    print("\nTickets waiting in queue:", queue.size())


# Normal Cases:

# Case 1: generate_tickets(queue, 1)
# ==> Generated: Ticket #1 | Created at 2026-02-10 00:52:50.585686
#
# ==> Tickets waiting in queue: 1

# Case 2: generate_tickets(queue, 3)
# ==> Generated: Ticket #1 | Created at 2026-02-10 00:54:47.816116
# ==> Generated: Ticket #2 | Created at 2026-02-10 00:54:49.142269
# ==> Generated: Ticket #3 | Created at 2026-02-10 00:54:50.642741
# 
# ==> Tickets waiting in queue: 3

# Case 3: generate_tickets(queue, 10)
# ==> Generated: Ticket #1 | Created at 2026-02-10 00:56:03.425901
# ==> Generated: Ticket #2 | Created at 2026-02-10 00:56:04.834709
# ==> Generated: Ticket #3 | Created at 2026-02-10 00:56:05.796589
# ==> Generated: Ticket #4 | Created at 2026-02-10 00:56:06.549576
# ==> Generated: Ticket #5 | Created at 2026-02-10 00:56:07.153516
# ==> Generated: Ticket #6 | Created at 2026-02-10 00:56:08.252871
# ==> Generated: Ticket #7 | Created at 2026-02-10 00:56:09.638395
# ==> Generated: Ticket #8 | Created at 2026-02-10 00:56:10.741102
# ==> Generated: Ticket #9 | Created at 2026-02-10 00:56:11.638490
# ==> Generated: Ticket #10 | Created at 2026-02-10 00:56:12.146954
#
# ==> Tickets waiting in queue: 10


# Edge Cases:

# Case 1: generate_tickets(queue, 0)     ==> Tickets waiting in queue: 0
# Case 2: generate_tickets(queue, -1)    ==> Tickets waiting in queue: 0
# Case 3: generate_tickets(queue, 'a')   ==> 'TypeError: can only concatenate str (not "int") to str'
