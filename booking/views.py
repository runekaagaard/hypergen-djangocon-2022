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
        a("Book timeslot", href=free.reverse(), class_active="active")
        a("My bookings", href=booked.reverse(), class_active="active")

@contextmanager
def row():
    with div(class_="row"):
        yield

@contextmanager
def col(n):
    with div(class_=f"col-{n}"):
        yield

@contextmanager
def card(title, description):
    with div(class_="card"):
        header(h4(title))
        p(description)
        with footer(class_="is-right"):
            yield

@contextmanager
def base_template():
    doctype()
    with head():
        link(href=static("chota.css"))
    with body(), div(class_="container"):
        h1("Doctor booking")
        with div(id_="target"):
            yield

base_template.target_id = "target"

def free_template(timeslots_by_date):
    menu()

    with p():
        input_(placeholder="Search here", id_="search", oninput=callback(search, THIS))
    with table():
        thead(tr(th(x) for x in ["Date", "Time", "Doctor", "Action"]))
        with tbody():
            for date, timeslots in timeslots_by_date:
                tr(th(date, colspan=4))
                for timeslot in timeslots:
                    with tr():
                        td()
                        td(timeslot.fmt_time)
                        td(timeslot.doctor)
                        td(
                            button("Book", id_=["timeslot", timeslot.pk], class_="button primary",
                                   onclick=callback(book, timeslot.pk)))

### Liveviews ###

@liveview(perm="booking.create_booking", base_template=base_template, user_plugins=[AlertifyPlugin()])
def free(request):
    timeslots_by_date = Timeslot.free_by_date()
    free_template(timeslots_by_date)

@liveview(perm="booking.create_booking", base_template=base_template, user_plugins=[AlertifyPlugin()])
def booked(request):
    menu()
    with row():
        for timeslot in Timeslot.objects.filter(booked_to=request.user):
            with col(4):
                with card(timeslot, timeslot.doctor):
                    button("Cancel", id=("timeslot", timeslot.pk), class_="button error",
                           onclick=callback(cancel, timeslot.pk))

### Actions ###

@action(perm="booking.create_booking", base_template=base_template, user_plugins=[AlertifyPlugin()])
def book(request, pk):
    Timeslot.book(request, pk)

    messages.add_message(request, messages.SUCCESS, "You got it!")
    return HttpResponseRedirect(booked.reverse())

@action(perm="booking.create_booking", base_template=base_template, user_plugins=[AlertifyPlugin()])
def search(request, query):
    timeslots_by_date = Timeslot.free_by_date(query)
    free_template(timeslots_by_date)

@action(perm="booking.create_booking", base_template=base_template, user_plugins=[AlertifyPlugin()],
        base_view=booked)
def cancel(request, pk):
    Timeslot.cancel(request, pk)
    messages.add_message(request, messages.WARNING, "The timeslot is GONE!")
