#!/bin/bash

if [ "$PWD" != "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" ]; then
    echo '[ERROR] Please run this script from inside the back-end/ directory'
    exit 1;
fi

if [[ ! -d 'env' ]]; then
    echo '[deployment] creating Python 3 virtual environment...'
    python3 -m venv env
fi

echo '[deployment] activating environment...'
source env/bin/activate

echo '[deployment] upgrading pip...'
pip install --upgrade pip

echo '[deployment] installing requirements...'
pip install -r requirements.txt

if [ ! -f .certs/cert.pem ]; then
    echo '[deployment] creating SSL certificate...'
    ./create-certs.sh
fi

echo '[deployment] running application...'
flask run
