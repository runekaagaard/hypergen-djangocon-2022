from contextlib import contextmanager

from hypergen.imports import *
from hypergen.plugins.alertify import AlertifyPlugin

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.templatetags.static import static

from booking.models import Timeslot

from django.utils.translation import get_language

### Templates ###

@contextmanager
def base_template():
    pass

base_template.target_id = "content"

def free_template(timeslots_by_date):
    pass

### Liveviews ###

@liveview(perm="booking.view_booking", base_template=base_template)  # pyright: ignore[reportGeneralTypeIssues]
def free(request):
    p("The free liveview.")

@liveview(perm="booking.view_booking", base_template=base_template)  # pyright: ignore[reportGeneralTypeIssues]
def booked(request):
    p("The booked liveview.")

### Actions ###

@action(perm="booking.view_booking", base_template=base_template)  # pyright: ignore[reportGeneralTypeIssues]
def search(request, query):
    pass

@action(perm="booking.add_booking", base_template=base_template)  # pyright: ignore[reportGeneralTypeIssues]
def book(request, pk):
    pass

@action(perm="booking.delete_booking", base_template=base_template)  # pyright: ignore[reportGeneralTypeIssues]
def cancel(request, pk):
    pass
