import argparse
from ntru import *

parser = argparse.ArgumentParser(description='Encrypt message')
parser.add_argument('-m', "--message", metavar='MESSAGE',
                    help='Message to encrypt', required=True)
parser.add_argument('-p', "--publicKey", metavar='KEY',
                    help="File with recipient's public key", required=True)
args = parser.parse_args()

#
# Load public key and message into ternary polynomials
#

m = messageToTernary(args.message)
h = readPolynomialFromFile(args.publicKey)

r = generatePolynomial(len(m))
e = encrypt(m, h, r)

savePolynomialToFile(e, "./message_enc.txt")
