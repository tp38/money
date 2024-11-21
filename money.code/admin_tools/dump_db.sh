#!/bin/bash

cd /code

source /opt/venv/bin/activate

python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 3 --format json > db.json

deactivate
