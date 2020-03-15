# -*- coding: utf-8 -*-
import math

with open("./oE.txt","w") as fst, open("./omistakes.txt","r") as mis:
	total = mis.readline().split()[2]
	ins = -math.log10(float(mis.readline().split()[1])/int(total))
	dele = -math.log10(float(mis.readline().split()[1])/int(total))
	subs = -math.log10(float(mis.readline().split()[1])/int(total))
	swaps = -math.log10(float(mis.readline().split()[1])/int(total))
	
	cnt = 2
	for i in u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ':
		fst.write("0 1 %s %s 0\n"%(i.encode('utf-8'),i.encode('utf-8')))
		fst.write("0 1 <eps> %s %f\n"%(i.encode('utf-8'),ins))
		fst.write("0 1 %s <eps> %f\n"%(i.encode('utf-8'),dele))
		for j in u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ':
			if i != j:
				fst.write("0 1 %s %s %f\n"%(i.encode('utf-8'),j.encode('utf-8'),subs))
				fst.write("0 %d %s %s %f\n"%(cnt,i.encode('utf-8'),j.encode('utf-8'),swaps))
				fst.write("%d 1 %s %s 0\n"%(cnt,j.encode('utf-8'),i.encode('utf-8')))
				cnt+=1
	fst.write("1 0\n")