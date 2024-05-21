#!/bin/bash

cd /home/th/Code/Python/Django/
tar --exclude='money.docs'\
    --exclude='money.postgres'\
    --exclude='.svn'\
    --exclude='__pycache__'\
    --exclude='migrations'\
    -cvzf money.tar.gz ./money_dev
