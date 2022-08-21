from django.db import models
from django.utils.formats import date_format

def full_name(user):
    return f"{user.first_name} {user.last_name}"

class Timeslot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    doctor = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="+")
    booked_to = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=None, null=True, related_name="+")

    def __repr__(self):
        d1 = date_format(self.start, format='SHORT_DATETIME_FORMAT', use_l10n=True)
        d2 = date_format(self.end, format='SHORT_DATETIME_FORMAT', use_l10n=True)
        booked_to = f' booked_to="{full_name(self.booked_to)}"' if self.booked_to else " booked_to=None"

        return f'<Timeslot id={self.pk} start="{d1}" end="{d2}" doctor="{full_name(self.doctor)}"{booked_to}>'
