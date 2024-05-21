#!/bin/bash
# Resets the local Django database, adding an admin login and migrations
set -e
echo ">>> Resetting the database"
./manage.py reset_db --close-sessions --noinput

echo ">>> Clearing migrations dir"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

if [ ! -d "banks/migrations" ] ; then
	mkdir 'banks/migrations'
	touch 'banks/migrations/__init__.py'
fi

if [ ! -d "budget/migrations" ] ; then
	mkdir 'budget/migrations'
	touch 'budget/migrations/__init__.py'
fi

echo -e "\n>>> Running migrations"
./manage.py makemigrations
./manage.py migrate

echo -e "\n>>> Creating new superuser 'admin'"
./manage.py createsuperuser \
   --username th \
   --email thierry.probst@free.fr \
   --noinput

password=`cat ./secret.txt`
echo -e "\n>>> Setting superuser 'admin' password"
./manage.py shell_plus --quiet-load -c "
u=User.objects.get(username='th')
u.set_password( ${password} )
u.save()
"
# Any extra data setup goes here.
echo -e "\n>>> Updating data"
./manage.py loaddata db.json

echo -e "\n>>> Database restore finished."
