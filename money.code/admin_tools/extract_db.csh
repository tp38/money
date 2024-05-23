#!/bin/csh

source /opt/venv/bin/activate.csh

cd /usr/local/www/apache24/data/money/money.code

echo -e "\n>>> Full extract"
python3.9 manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 3 --format json > db.json

scp *.json th@192.168.1.39:/home/th/Code/Python/Django/money_dev/money.code/

deactivate
