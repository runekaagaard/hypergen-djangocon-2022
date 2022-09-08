from contextlib import contextmanager
from itertools import groupby

from hypergen.imports import *
from hypergen.plugins.alertify import AlertifyPlugin, alertify_messages

from django.http import HttpResponseRedirect
from django.contrib import messages

from booking.models import Timeslot

### Templates ###

def menu():
    with nav(class_="tabs nav-center"):
        a("Book timeslot", href=book_timeslot.reverse(), class_active="active")
        a("My bookings", href=my_bookings.reverse(), class_active="active")

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
                            button("Book", class_="button primary", id=("book-timeslot", timeslot.pk),
                                   onclick=callback(book_timeslot2, query, timeslot.pk)))

@contextmanager
def card(title, description):
    with div(class_="card"):
        header(h4(title))
        p(description)
        with footer(class_="is-right"):
            yield

### Liveviews ###

liveview_settings = dict(base_template=base_template, user_plugins=[AlertifyPlugin()])

@liveview(perm="booking.create_booking", **liveview_settings)
def book_timeslot(request):
    timeslots_by_date = Timeslot.available_by_date()
    timeslot_template(timeslots_by_date)

@liveview(perm="booking.view_booking", **liveview_settings)
def my_bookings(request):
    with div(class_="row"):
        for timeslot in Timeslot.objects.filter(booked_to=request.user).order_by("start"):
            with div(class_="col-4"), card(timeslot.fmt_datetime, timeslot.doctor):
                a("Cancel", class_="button error", id=("timeslot", timeslot.pk),
                  onclick=callback(cancel_timeslot, timeslot.pk, confirm="Are you sure?"))

### Actions ###

@action(perm="booking.create_booking", **liveview_settings)
def filter_timeslots(request, query):
    timeslots_by_date = Timeslot.available_by_date(query)
    timeslot_template(timeslots_by_date)

@action(perm="booking.create_booking", **liveview_settings)
def book_timeslot2(request, query, timeslot_id):
    messages.add_message(request, messages.SUCCESS, "You booked a new time. Good stuff <3")
    messages.add_message(request, messages.INFO, "See your booked timeslots on this page!")
    Timeslot.objects.filter(pk=timeslot_id).update(booked_to=request.user)

    timeslots_by_date = Timeslot.available_by_date(query)
    timeslot_template(timeslots_by_date)

    # return HttpResponseRedirect(my_bookings.reverse())
    # command("hypergen.redirect", my_bookings.reverse())

@action(perm="booking.create_booking", base_view=my_bookings, **liveview_settings)
def cancel_timeslot(request, timeslot_id):
    print("ADD MESSAGE")
    messages.add_message(request, messages.WARNING, "The timeslot is GONE!")
    Timeslot.objects.filter(pk=timeslot_id).update(booked_to=None)
