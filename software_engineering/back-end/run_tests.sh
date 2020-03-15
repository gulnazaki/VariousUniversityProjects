#!/bin/bash

if [ "$PWD" != "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" ]; then
    echo '[ERROR] Please run this script from inside the back-end/ directory'
    exit 1;
fi

if [[ ! -d 'env' ]]; then
    echo '[testing] creating Python 3 virtual environment...'
    python3 -m venv env
fi

echo '[testing] activating environment...'
source env/bin/activate

echo '[testing] upgrading pip...'
pip install --upgrade pip

echo '[testing] installing requirements...'
pip install -r requirements.txt

echo -n '[testing] setting up a testing database, please wait... '
echo "create database energy_db_test" | mysql -u root "-proot" 2>/dev/null
mysqldump -u root "-proot" energy_db 2>/dev/null | mysql -u root "-proot" energy_db_test 2>/dev/null
echo 'done'

cd tests
pytest
cd ..

echo "drop database energy_db_test" | mysql -u root "-proot" 2>/dev/null
