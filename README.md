Software Engineering Team3
------------
Team 3 Project for Software Engineering at Missouri State University

Prerequisite(s)
-------------
1. [python](http://www.www.python.org/ "python")
2. [django](http://www.djangoproject.com/ "django")
3. [south](http://south.aeracode.org/ "south")

Download these and install them.

If you are using an Ubuntu based Linux distribution, you can install them via:

**`sudo apt-get install python python-django python-django-south`**

Database Initalization
--------------------
To generate the initial (empty) database, run:

**`python manage.py syncdb`**
**`python manage.py migrate`**

Start the Server
--------------------
To start the server, run:

**`python manage.py runserver 0.0.0.0:8000`**
(Note, you can change 8000 to the port of your choice)

To view the root page, open: http://localhost:8000
