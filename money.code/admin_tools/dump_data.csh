#!/bin/sh

source /opt/venv/bin/activate

echo -e "\n>>> Data"
python3.9 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 3 --format json > db.json

deactivate
