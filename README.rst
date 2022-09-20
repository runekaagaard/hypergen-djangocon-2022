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

Then navigate to `http://127.0.0.1:8000 <http://127.0.0.1:8000>`_ that logs you in automatically, then redirects to the ``free`` liveview.

Interesting files
=================

`booking/models.py <https://github.com/runekaagaard/hypergen-djangocon-2022/blob/main/booking/models.py>`_
  The Doctor and Timeslot models.
`booking/urls.py <https://github.com/runekaagaard/hypergen-djangocon-2022/blob/main/booking/urls.py>`_
  The ``autourls()`` function that creates urls for all liveviews and actions automatically.
`booking/views.py <https://github.com/runekaagaard/hypergen-djangocon-2022/blob/main/booking/views.py>`_
  Skeleton of liveviews, actions, template functions and base templates where we will build the app.

Less interesting files
======================

`djangocon2022/settings.py <https://github.com/runekaagaard/hypergen-djangocon-2022/blob/main/djangocon2022/settings.py>`_
  The main settings file. ``booking`` is added to ``INSTALLED_APPS``. ``hypergen.context.context_middleware`` is added to ``MIDDLEWARE``.
`djangocon2022/urls.py <https://github.com/runekaagaard/hypergen-djangocon-2022/blob/main/djangocon2022/urls.py>`_
  The main urls file. The booking app is added. ``/`` logs the user in automatically.
`booking/pasta.py <https://github.com/runekaagaard/hypergen-djangocon-2022/blob/main/booking/pasta.py>`_
  Some stuff we might copy/paste during the presentation.

