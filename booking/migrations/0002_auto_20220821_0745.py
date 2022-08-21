import random, datetime

from django.db import migrations
from django.utils import timezone

PEOPLE = [
    "Trevor Sutherland", "Boris Paige", "Maria Black", "Diana Dowd", "Julian Buckland", "Victor White",
    "Leah Cornish", "Joshua Reid", "William Campbell", "Angela North", "Joan Glover", "Nicola Paterson",
    "Tracey Greene", "Julia Mackay", "Blake Coleman", "Colin Chapman", "William Gill", "Gordon North",
    "Jake Gibson", "Evan Hudson", "Stewart Hunter", "Charles Avery", "Amanda Bower", "Jake Stewart",
    "Brian Hunter", "Elizabeth Ince", "Molly Carr", "Nicholas Thomson", "Donna Greene", "Gordon Graham",
    "Chloe Slater", "Pippa Edmunds", "Isaac Oliver", "Joshua Mackay", "Lauren Watson", "Paul Butler",
    "Andrew Slater", "Isaac Newman", "Elizabeth Arnold", "Neil May", "William Slater", "Leonard Welch",
    "Alexandra Ellison", "Zoe Payne", "John Butler", "Emily McLean", "Hannah Kelly", "Connor Parr", "Stephen Ross",
    "Evan Paige"
]

def forward(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Timeslot = apps.get_model('booking', 'Timeslot')

    user = User.objects.create_user('admin', 'admin@example.com', '1234')
    user.first_name = "Admin"
    user.last_name = "And Patient"
    user.is_superuser = True
    user.is_staff = True
    user.save()

    users = []
    for person in PEOPLE:
        first_name, last_name = person.split(" ")
        username = person.lower().replace(" ", "")
        user = User(first_name=first_name, last_name=last_name, email=f"{username}@example.com", username=username,
                    is_staff=True)
        user.save()
        users.append(user)

    for _ in range(100):
        hour = random.randint(8, 15)
        start = datetime.datetime(2022, 10, random.randint(1, 14), hour, tzinfo=timezone.utc)
        end = start + datetime.timedelta(hours=1)
        Timeslot(start=start, end=end, doctor=random.choice(users),
                 booked_to_id=1 if random.random() > 0.9 else None).save()

def backward(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Timeslot = apps.get_model('booking', 'Timeslot')
    User.objects.all().delete()
    Timeslot.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [migrations.RunPython(forward, backward)]
