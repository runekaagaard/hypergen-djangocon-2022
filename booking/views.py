from contextlib import contextmanager
from itertools import groupby

from hypergen.imports import *
from booking.models import Timeslot

def hprint(*args, **kwargs):
    # TODO: Move this upstream.
    # TODO: Make custom support for:
    #           - Queryset
    #           - values and values_list
    #           - query (sql)
<<<<<<< HEAD
    #           - grouper
=======
>>>>>>> 2d1ef198794dae6f5c4bcb611403294962d2c533
    from pprint import pformat
    d = dict

    def fmt(x):
        dd(pformat(x, indent=4, width=120),
           span(" (", x.__class__.__module__, ".",
                type(x).__name__, ")", style=d(color="green")))

    with div(style=d(border="1px solid grey", padding="0 4px", background_color="#eee")):
        if len(args) > 0 or kwargs:
            for i, arg in enumerate(args, 1):
                with dl(style=d(margin=0)):
                    dt("arg", i, style=d(font_weight="bold"), sep=" ")
                    fmt(arg)
        else:
            div(code(pformat(args[0], indent=4, width=120)))

        for k, v in kwargs.items():
            with dl(style=d(margin=0)):
                dt(k, style=d(font_weight="bold"))
                fmt(v)

def menu():
    a("My bookings", href=my_bookings.reverse())
    span(" ")
    a("Book timeslot", href=book_timeslot.reverse())

@liveview(perm="booking.view_booking")
def my_bookings(request):
    menu()
    for timeslot in Timeslot.objects.filter(booked_to=request.user):
        li(timeslot.start, timeslot.end, timeslot.doctor, sep=" | ")

@liveview(perm="booking.create_booking")
def book_timeslot(request):
    menu()
    timeslots = Timeslot.objects.filter(booked_to=None).order_by("start")
<<<<<<< HEAD
    timeslots_grouped = groupby(timeslots, key=lambda x: x.start.date())
    hprint(timeslots, {"ok": 42}, im_doing_it=True, so_true="Go giants!", group=timeslots_grouped,
           first=next(timeslots_grouped))

    for date, group in timeslots_grouped:
=======
    hprint(timeslots, {"ok": 42}, im_doing_it=True, so_true="Go giants!")

    for date, group in groupby(timeslots, key=lambda x: x.start.date()):
>>>>>>> 2d1ef198794dae6f5c4bcb611403294962d2c533
        h2(date)
        for timeslot in group:
            li(timeslot.start, timeslot.end, timeslot.doctor, sep=" | ")
