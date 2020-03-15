with open("./data/en_caps_noaccent.txt","r") as dic, open("./A2.txt","w") as fsa:								# open dictionary for reading and A2.txt for storing the fsa data
	i = 0
	for line in dic:
		i = i + 1
		fsa.write("0 %d %s %s 0\n" %(i,line[0],line[0]))
		for letter in range(1,len(line)-1):
			i = i + 1
			fsa.write("%d %d %s %s 0\n" %(i-1,i,line[letter],line[letter]))
		fsa.write("%d 0\n" %i)