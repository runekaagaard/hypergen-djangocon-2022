from contextlib import contextmanager

from hypergen.imports import *
from hypergen.plugins.alertify import AlertifyPlugin

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.templatetags.static import static

from booking.models import Timeslot

### Templates ###

def menu():
    with nav(class_="tabs nav-center"):
        a("Book timeslot", href=book_timeslot.reverse(), class_active="active")
        a("My bookings", href=my_bookings.reverse(), class_active="active")

@contextmanager
def base_template():
    doctype()
    with html():
        with head():
            link(href=static("chota.css"))
        with body(), div(class_="container"):
            h1("Doctor booking")
            with div(id="target"):
                yield

base_template.target_id = "target"

def timeslot_template(timeslots_by_date, query=""):
    menu()
    with p():
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
                                   onclick=callback(book, query, timeslot.pk)))

@contextmanager
def card(title, description):
    with div(class_="card"):
        header(h4(title))
        p(description)
        with footer(class_="is-right"):
            yield

@contextmanager
def row():
    with div(class_="row"):
        yield

@contextmanager
def col(n):
    with div(class_=f"col-{n}"):
        yield

### Liveviews ###

liveview_settings = dict(base_template=base_template, user_plugins=[AlertifyPlugin()])

@liveview(perm="booking.create_booking", **liveview_settings)
def book_timeslot(request):
    timeslots_by_date = Timeslot.available_by_date()
    timeslot_template(timeslots_by_date)

@liveview(perm="booking.view_booking", **liveview_settings)
def my_bookings(request):
    menu()
    with row():
        for timeslot in Timeslot.objects.filter(booked_to=request.user).order_by("start"):
            with col(4), card(timeslot.fmt_datetime, timeslot.doctor):
                a("Cancel", class_="button error", id=("timeslot", timeslot.pk),
                  onclick=callback(cancel_timeslot, timeslot.pk, confirm="Are you sure?"))

### Actions ###

@action(perm="booking.create_booking", **liveview_settings)
def filter_timeslots(request, query):
    timeslots_by_date = Timeslot.available_by_date(query)
    timeslot_template(timeslots_by_date)

@action(perm="booking.create_booking", **liveview_settings)
def book(request, query, timeslot_id):
    messages.add_message(request, messages.SUCCESS, "You booked a new time. Good stuff <3")
    Timeslot.objects.filter(pk=timeslot_id).update(booked_to=request.user)

    timeslots_by_date = Timeslot.available_by_date(query)
    timeslot_template(timeslots_by_date)

    return HttpResponseRedirect(my_bookings.reverse())

@action(perm="booking.create_booking", base_view=my_bookings, **liveview_settings)
def cancel_timeslot(request, timeslot_id):
    Timeslot.objects.filter(pk=timeslot_id).update(booked_to=None)
    messages.add_message(request, messages.WARNING, "The timeslot is GONE!")
