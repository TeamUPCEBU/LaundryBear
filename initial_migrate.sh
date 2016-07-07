#!/usr/bin/env sh

python manage.py migrate || TRUE
python manage.py migrate contenttypes || TRUE
python manage.py migrate sites || TRUE
python manage.py migrate || TRUE
