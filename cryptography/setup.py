import numpy as np
from ntru import *

while True:
	try:
		F = generatePolynomial(N)
		Fp, Fq = invertPolynomial(F,p,q)
		break
	except sym.polys.polyerrors.NotInvertible:
		pass

G = generatePolynomial(N)

h = p*Fq*G
h = sym.rem(h, xN, symmetric=False, modulus = q)

savePolynomialToFile(F, "./private_key_F.txt")
savePolynomialToFile(Fp, "./private_key_Fp.txt")

savePolynomialToFile(h, "./public_key.txt")
