from django.db import models

class Timeslot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    doctor = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="+")
    booked_to = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=None, null=True, related_name="+")
