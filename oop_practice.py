
class Event:

    def __init__(self, event_name, event_date, venue):
        self.event_name = event_name
        self.event_date = event_date
        self.venue = venue


event1 = Event("Annual Sports Meet", "20-12-2026", "Main Ground")

print(event1.event_name)
print(event1.event_date)
print(event1.venue)

event2 = Event("Cultural Fest", "15-01-2027", "Auditorium")

print(event2.event_name)
print(event2.event_date)
print(event2.venue)

def display_details(self):
    print("Event:", self.event_name)
    print("Date:", self.event_date)
    print("Venue:", self.venue)