import os
import django
import random
from faker import Faker
from datetime import timedelta, datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

from events.models import Category, Event, Participant 
fake = Faker()

def populate_event_data():
    # clear old data (optional)
    Category.objects.all().delete()
    Event.objects.all().delete()
    Participant.objects.all().delete()


    # create Category:
    categories = []
    for _ in range(5):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            description = fake.paragraph()
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")

    # create Event:
    events = []
    for _ in range(10):
        start_date = fake.date_between(start_date="-30d", end_date="+30d")
        start_time = fake.time_object()
        event = Event.objects.create(
            name = fake.bs().title(),
            description = fake.paragraph(),
            date = start_date,
            time = start_time,
            location = fake.address(),
            category = random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # create Participant:
    participants = []
    for _ in range(30):
        participant = Participant.objects.create(
            name = fake.name(),
            email = fake.unique.email()
        )
        participant.events.set(random.sample(events, random.randint(1,3)))
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    print("\Event data populated successfully!")

if __name__ == "__main__":
    populate_event_data()