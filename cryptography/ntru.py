import numpy as np
import csv
import random
import sympy as sym
import dill

#
# This file contains all functionality required for the NTRU cryptosystem
#

# public parameter setup
N = 503         # 251 is used in most commercial applications, for improved security can become 347 or better 503 (must be prime)
p = 3               # most commonly used, needs to be relatively small 
q = 257         # must be relatively prime to p and much larger than p              

xN = [0] * (N + 1)  # ring polynomial (x^N - 1)
xN[0] = 1
xN[N] = -1


def toPoly(poly,l=N):
    x = sym.Symbol('x')
    f = 0
    for i in range(len(poly)):
        f += (x**i)*(poly[l-1-i])
    return sym.poly(f)

xN = toPoly(xN,N+1)

def generatePolynomial(N):
    poly = np.array([random.randint(-1, 1) for i in range(N)])
    return toPoly(poly,N)


def invertPolynomial(f,p,q):
    x = sym.Symbol('x')
    Fp = sym.polys.polytools.invert(f,x**N-1,domain=sym.GF(p, symmetric=False))
    Fq = sym.polys.polytools.invert(f,x**N-1,domain=sym.GF(q, symmetric=False))
    return Fp, Fq


def savePolynomialToFile(e, path):
    dill.dump(e, open(path, "wb"))
    return


def readMessageFromFile(path):
    with open(path, "r") as infile:
        msg = infile.read()
        return msg


def readPolynomialFromFile(path):
    return dill.load(open(path, "rb"))


def toTernary(n):
    e = n // 3
    q = n % 3
    if n == 0:
        return [0]
    elif e == 0:
        return [q]
    else:
        return toTernary(e) + [q]

def messageToTernary(msg):
    poly = []
    for char in msg:
        ternary = toTernary(ord(char))
        poly += [0] * (6 - len(ternary)) + ternary
    return [x - 1 for x in poly]


def fromTernary(ternaryTuple):
    dec = 0
    for i in range(len(ternaryTuple)):
        dec += ternaryTuple[len(ternaryTuple) - (i+1)] * 3 ** i
    return dec

def messageFromTernary(poly):
    poly = poly.all_coeffs()
    poly = [x + 1 for x in poly]
    msg = ""
    i = 0
    while i < len(poly):
        x = fromTernary(poly[i:i + 6])
        msg += chr(x)
        i += 6
    return msg


def encrypt(m, h, r):
    e = r*h
    e = e + toPoly(m,len(m))
    e = sym.rem(e, xN, symmetric=False, modulus = q)
    return e

def decrypt(f, e, fp):
    a = f*e
    a = sym.rem(a, xN, modulus = q)
    m = fp*a
    m = sym.rem(m, xN, modulus = p)
    return m
