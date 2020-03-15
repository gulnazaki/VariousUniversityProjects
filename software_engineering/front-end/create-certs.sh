#!/bin/bash

if [ "$PWD" != "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" ]; then
    echo '[ERROR] Please run this script from inside the front-end/ directory'
    exit 1;
fi

mkdir -p .certs
rm .certs/*.pem

openssl req                \
    -x509                  \
    -newkey rsa:4096       \
    -keyout .certs/key.pem \
    -out .certs/cert.pem   \
    -nodes                 \
    -days 365              \
    -subj "/C=GR/ST=Attica/L=Athens/O=KKE-TL/CN=localhost"
