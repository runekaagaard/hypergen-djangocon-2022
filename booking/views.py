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

    @component
    def typeinfo(x):
        span(" (", x.__class__.__module__, ".", type(x).__name__, ")", style=d(color="darkgrey"))

    def fmt(x):
        pre(code(pformat(x, width=120)))

    with div(style=d(padding="8px", margin="4px 0 0 0", background="#ffc", color="black",
                     font_family="sans-serif")):
        if len(args) == 1 and not kwargs:
            div(typeinfo(args[0]))
            fmt(args[0])
        else:
            for i, arg in enumerate(args, 1):
                div(b("arg", i, sep=" "), typeinfo(arg))
                fmt(arg)

        for k, v in kwargs.items():
            div(b(k), typeinfo(v))
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
    from pprint import pprint
    doctype()
    with html():
        with head():
            link(href="https://unpkg.com/chota")
        with body(style=dict(margin="20px auto")), div(class_="container"):
            menu()
            timeslots_by_date = Timeslot.available_by_date()

            for date, timeslots in timeslots_by_date:
                h2(date)
                with table():
                    thead(tr(th(x) for x in ("Time", "Doctor", "Actions")))
                    with tbody():
                        for timeslot in timeslots:
                            with tr():
                                td(timeslot)
                                td(timeslot.doctor)
                                td(button("Book"))
