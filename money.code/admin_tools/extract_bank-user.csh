#!/bin/csh

source /opt/venv/bin/activate.csh

cd /usr/local/www/apache24/data/budget_v4/budget.code
rm 0*

echo -e "\n>>> Extract banks and users"
python3.9 manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude management --exclude wallets --exclude admin --indent 3 --format json > 00-banks-users.json

echo -e "\n>>> Extract budgetitemref"
python3.9 manage.py dumpdata management.budgetitemref --indent 3 --format json > 01-budgetitemref.json
sed -i .sav -e 's/management/budget/g' 01-budgetitemref.json

python3.9 manage.py dumpdata management.budget --indent 3 --format json > 02-month.json
sed -i .sav -e 's/management\.budget/budget\.month/g' -e 's/"month":/"start":/g' 02-month.json

echo -e "\n>>> Extract budget -> month"
python3.9 manage.py dumpdata management.budgetitem --indent 3 --format json > 03-budgetitem.json
sed -i .sav -e 's/management/budget/g' -e 's/"budget":/"month":/g' 03-budgetitem.json

echo -e "\n>>> Extract opelement"
python3.9 manage.py dumpdata management.opelement --indent 3 --format json > 04-opelement.json
sed -i .sav -e 's/management/budget/g' 04-opelement.json

scp *.json th@192.168.1.39:/home/th/Code/Python/Django/money_dev/money.code/

deactivate
