Installation
============

Install the example like so::

  git clone https://github.com/runekaagaard/hypergen-djangocon-2022.git
  cd hypergen-djangocon-2022
  python3 -m venv venv
  source venv/bin/activate
  pip install Django==4.1.1 django-hypergen==0.9.10
  python manage.py migrate
  python manage.py runserver
