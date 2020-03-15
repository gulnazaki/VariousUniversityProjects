import argparse
from ntru import *

parser = argparse.ArgumentParser(description='Decrypt message')
parser.add_argument('-c', "--ciphertext", metavar='CIPHERTEXT',
                    help='File with encrypted message', required=True)
args = parser.parse_args()

#
# Load ciphertext and our own private keys
#

c = readPolynomialFromFile(args.ciphertext)
F = readPolynomialFromFile("./private_key_F.txt")
Fp = readPolynomialFromFile("./private_key_Fp.txt")

m = decrypt(F, c, Fp)
m = messageFromTernary(m)

print(m)
