# -*- coding: utf-8 -*-

with open("./oI.txt","w") as fst:
	for letter in u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ':
		fst.write("0 1 " + letter.encode('utf-8') + " " + letter.encode('utf-8') + " 0\n")
	fst.write("1 0\n")