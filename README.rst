Installation
============

Install the example code like so::

  git clone https://github.com/runekaagaard/hypergen-djangocon-2022.git
  cd hypergen-djangocon-2022
  python3 -m venv venv
  source venv/bin/activate
  pip install Django==4.1.1 django-hypergen==0.9.10
  python manage.py migrate
  python manage.py runserver

Interesting files
=================

booking/models.py
  The Doctor and Timeslot models.
booking/urls.py
  The autourls() function that creates urls for all liveviews and actions automatically.
booking/views.py
  Empty skeleton of liveviews, actions, template functions and base templates where we will build the app.
