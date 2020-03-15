# -*- coding: utf-8 -*-
import codecs

with codecs.open("./data/el_caps_noaccent.txt","r", encoding='utf-8') as dic, open("./A1.txt","w") as fsa:		# open dictionary for reading and A1.txt for storing the fsa data
	i = 0
	for line in dic:
		if line[0] == u'\ufeff':																				# utf-8 encoded files start with this special character we get rid of
			i = i + 1	
			fsa.write("0 %d %s %s 0\n" %(i,line[1].encode('utf-8'),line[1].encode('utf-8')))					# first line, 0 returns to the initial state
			fsa.write("%d 0\n" %i)
		else:
			i = i + 1
			fsa.write("0 %d %s %s 0\n" %(i,line[0].encode('utf-8'),line[0].encode('utf-8')))					# every word's first arch starts from 0
			for letter in range(1,len(line)-1):
				i = i + 1
				fsa.write("%d %d %s %s 0\n" %(i-1,i,line[letter].encode('utf-8'),line[letter].encode('utf-8')))
			fsa.write("%d 0\n" %i)																				# final state