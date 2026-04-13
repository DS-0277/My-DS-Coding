from datetime import datetime

class Ticket:
    def __init__(self, ticket_number):
        # Store ticket number
        self.ticket_number = ticket_number
        # Store date and time when ticket is created
        self.timestamp = datetime.now()
    def __str__(self):
        return "Ticket #" + str(self.ticket_number) + " | Created at " + str(self.timestamp)