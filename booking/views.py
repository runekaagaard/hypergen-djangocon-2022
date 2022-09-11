from contextlib import contextmanager

from hypergen.imports import *
from hypergen.plugins.alertify import AlertifyPlugin

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.templatetags.static import static

from booking.models import Timeslot

### Templates ###

### Liveviews ###

@liveview(perm="booking.create_booking")
def free(request):
    h1("Hello djangocon 2022 from Hypergen <3")

### Actions ###
