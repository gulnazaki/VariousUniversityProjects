#!/bin/bash

if [ "$PWD" != "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" ]; then
    echo '[ERROR] Please run this script from inside the cli-client/ directory'
    exit 1;
fi

if ! curl -k https://localhost:8765/energy/api/HealthCheck >/dev/null 2>&1 ; then
    echo '[ERROR] Can not connect to API. Are you sure it is running?'
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

echo '[testing] installing pytest...'
pip install pytest

echo '[testing] installing cli client...'
pip install -e .

pytest
