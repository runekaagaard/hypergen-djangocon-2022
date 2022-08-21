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
    #           - grouper
    from pprint import pformat
    d = dict

    def fmt(x, tag=dd):
        tag(pformat(x, indent=4, width=120),
            span(" (", x.__class__.__module__, ".",
                 type(x).__name__, ")", style=d(color="darkgrey")))

    with div(style=d(padding="8px", margin="4px 0 0 0", background="#ffc", color="black",
                     font_family="sans-serif")):
        if len(args) == 1 and not kwargs:
            fmt(args[0], span)
        else:
            for i, arg in enumerate(args, 1):
                with dl(style=d(margin=0)):
                    dt("arg", i, style=d(font_weight="bold"), sep=" ")
                    fmt(arg)

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
    for timeslot in Timeslot.objects.filter(booked_to=request.user).order_by("start"):
        li(timeslot.start, timeslot.end, timeslot.doctor, sep=" | ")

@liveview(perm="booking.create_booking")
def book_timeslot(request):
    menu()
    timeslots = Timeslot.objects.filter().order_by("start")
    timeslots_grouped = groupby(timeslots, key=lambda x: x.start.date())
    hprint(timeslots, {"ok": 42}, im_doing_it=True, so_true="Go giants!", group=timeslots_grouped,
           first=next(timeslots_grouped))
    hprint("OK")

    for date, group in timeslots_grouped:
        h2(date)
        for timeslot in group:
            li(timeslot.start, timeslot.end, timeslot.doctor, sep=" | ")
