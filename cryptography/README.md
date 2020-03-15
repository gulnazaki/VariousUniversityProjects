# NTRU

This is an implementation of the NTRU Post-Quantum Cryptosystem, following the structure found online and especially on this paper: https://nitaj.users.lmno.cnrs.fr/ntru3final.pdf

## Build / Installation

Currently running on python3.6.
The python modules *sympy* and *dill* are required. Make sure to install these.

## How to use:

python setup.py

python encrypt.py -m "your-message-here" -p "filename-of-public-key" (stores encrypted message into "message_enc.txt")

python decrypt.py -c "ciphertext-filename"

## Files

ntru.py contains public parameters used for NTRU Cryptosystem. That is N = 503, p = 3, q = 257. Also, contains all necessary functions for encryption, decryption, polynomial manipulation, polynomial to text and vice versa conversion.

setup.py creates public and private keys, storing them as files.

encrypt.py takes a message as an argument and using the public key provided encrypts it creating "message_enc.txt"

decrypt.py takes ciphertext file as an argument and prints the plaintext message

## Warning!

The message shouldn't exceed 83 characters.

Do not share your private key!
