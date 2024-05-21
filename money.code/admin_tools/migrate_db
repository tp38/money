#!/bin/bash

source /opt/money/bin/activate

echo -e "\n>>> Resetting the database"
./manage.py reset_db --noinput --close-sessions

echo -e "\n>>> Running migrations"
rm banks/migrations/0*.py
rm budget/migrations/0*.py

./manage.py makemigrations
./manage.py migrate

echo -e "\n>>> Loaddata"
./manage.py flush --noinput
./manage.py loaddata 00-banks-users.json
./manage.py loaddata 01-budgetitemref.json
./manage.py loaddata 02-month.json
./manage.py loaddata 03-budgetitem.json
./manage.py loaddata 04-opelement.json

echo -e "\n>>> Delete json files"
#rm *.json

deactivate
