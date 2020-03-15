import string

with open("./I.txt","w") as fst:						# write fst data in I.txt
	for letter in string.ascii_uppercase:								
		fst.write("0 1 %s %s 1000\n" %(letter,letter)) 	# write in Arc appropriate form
	fst.write("1 0\n")