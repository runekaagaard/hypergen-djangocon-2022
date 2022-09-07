from itertools import groupby
from django.db import models
from django.utils.formats import date_format

def full_name(user):
    return f"{user.first_name} {user.last_name}"

class Doctor(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Doctor id={self.pk} name="{self.name}">'

class Timeslot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="+")
    booked_to = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=None, null=True, related_name="+")

    @staticmethod
    def available_by_date():
        return [[k, list(v)] for k, v in groupby(
            Timeslot.objects.filter(booked_to=None).order_by("start"), key=lambda x: x.start.date())]

    def __str__(self):
        return f"{date_format(self.start, format='SHORT_DATETIME_FORMAT')} – {date_format(self.end, format='SHORT_DATETIME_FORMAT')}"

    def __repr__(self):
        d1 = str(self.start)[:16]
        d2 = str(self.end)[:16]
        booked_to = f' booked_to="{full_name(self.booked_to)}"' if self.booked_to else " booked_to=None"

        return f'<Timeslot id={self.pk} start="{d1}" end="{d2}" doctor="{self.doctor.name}"{booked_to}>'
