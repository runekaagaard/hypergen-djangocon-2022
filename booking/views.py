from contextlib import contextmanager
from itertools import groupby

from hypergen.imports import *

from django.http import HttpResponseRedirect

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
    with nav(class_="tabs nav-center"):
        a("Book timeslot", href=book_timeslot.reverse(), class_="active")
        a("My bookings", href=my_bookings.reverse())

    p(" ")

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            link(href="https://unpkg.com/chota")
        with body(style=dict(margin="20px auto")), div(class_="container"):
            menu()
            with div(id="target"):
                yield

base_template.target_id = "target"

def timeslot_template(timeslots_by_date, query=""):
    with p(style=dict(margin_top="20px")):
        input_(placeholder="Search for your doctors name", oninput=callback(filter_timeslots, THIS, debounce=50),
               id="filter-timeslots", autofocus=True)

    with table(class_="striped"):
        thead(tr(th(x) for x in ("Date", "Time", "Doctor", "Actions")))
        with tbody():
            for date, timeslots in timeslots_by_date:
                tr(th(date, colspan="4"))
                for timeslot in timeslots:
                    with tr():
                        td()
                        td(timeslot.fmt_time)
                        td(timeslot.doctor)
                        td(
                            button("Book", id=("book-timeslot", timeslot.pk),
                                   onclick=callback(book_timeslot2, query, timeslot.pk)))

@liveview(perm="booking.create_booking", base_template=base_template)
def book_timeslot(request):
    timeslots_by_date = Timeslot.available_by_date()
    timeslot_template(timeslots_by_date)

@action(perm="booking.create_booking", target_id="target")
def filter_timeslots(request, query):
    timeslots_by_date = Timeslot.available_by_date(query)
    timeslot_template(timeslots_by_date)

@action(perm="booking.create_booking", target_id="target")
def book_timeslot2(request, query, timeslot_id):
    command("alert", f"You booked a new time. Good stuff.")
    Timeslot.objects.filter(pk=timeslot_id).update(booked_to=request.user)

    timeslots_by_date = Timeslot.available_by_date(query)
    timeslot_template(timeslots_by_date)

@contextmanager
def card(title, description):
    with div(class_="card"):
        header(h4(title))
        p(description)
        with footer(class_="is-right"):
            yield

@liveview(perm="booking.view_booking", base_template=base_template)
def my_bookings(request):
    with div(class_="row"):
        for timeslot in Timeslot.objects.filter(booked_to=request.user).order_by("start"):
            with div(class_="col-4"), card(timeslot.fmt_datetime, timeslot.doctor):
                a("Cancel", class_="button error", id=("timeslot", timeslot.pk),
                  onclick=callback(cancel_timeslot, timeslot.pk, confirm_="Are you sure?"))

@action(perm="booking.create_booking", target_id="target", base_view=my_bookings)
def cancel_timeslot(request, timeslot_id):
    command("alert", f"Time is gone forever!")
    Timeslot.objects.filter(pk=timeslot_id).update(booked_to=None)
