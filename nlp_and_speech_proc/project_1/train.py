# -*- coding: utf-8 -*-
import string
import collections

def count(L, letter):
	counter=collections.Counter(L[letter])
	return counter.most_common();														# returns list containing most common correlations

greekf = open("./data/train_gr.txt","r")												# open greek corpus for reading
grengf = open("./data/train_greng.txt","r")												# open greeklish corpus for reading

greek = [i.split() for i in greekf.readlines()]											# greek = list containing list of every word
greng = [i.split() for i in grengf.readlines()]

E = [[]]																				# list of lists for correlations
engnum = 0																				# letter to key value id
engdict = {}																			# dictionary

for line in range(len(greek)):
	for word in range(len(greek[line])):
		greekword = unicode(greek[line][word],'utf-8')									# greek word in utf-8 encoding
		grengword = greng[line][word]
		if greekword[0] in string.ascii_uppercase:										# if greek corpus contains english characters move on
			pass
		elif len(greekword) != len(grengword):											# don't check 1-2, 2-1 correlations yet
			pass
		else:
			for letter in range(len(grengword)):										# for every letter
				 if engdict.has_key(grengword[letter]):
				 	E[engdict[grengword[letter]]].append(greekword[letter])				# if correlations exists just append
				 else:
				 	engdict.update({grengword[letter]:engnum})							# else add registry in dictionary and append correlation
				 	E.insert(engnum, [])
				 	E[engnum].append(greekword[letter])
				 	engnum = engnum + 1													# next value id

for line in range(len(greek)):
	for word in range(len(greek[line])):
		greekword = unicode(greek[line][word],'utf-8')
		grengword = greng[line][word]
		if greekword[0] in string.ascii_uppercase:
			pass
		elif len(greekword) < len(grengword):											# if greekword is shorter we have atleast a greek char corresponding to 2 latin
			i = 0
			for gletter in greekword:
				if gletter in u'ΑΒΓΖΚΛΜΝΟΠΡΣΤΧΩ' or E[engdict[grengword[i]]].count(gletter) > 3:	# these chars can't correspond to more latin also check common // no garbage
					i = i + 1
				else:
					newletter = grengword[i] + grengword[i+1]							# we need one latin and its next to correspond to a greek
					i = i + 2
					if engdict.has_key(newletter):
						E[engdict[newletter]].append(gletter)
					else:
						engdict.update({newletter:engnum})
				 		E.insert(engnum, [])
				 		E[engnum].append(gletter)
				 		engnum = engnum + 1
		elif len(grengword) < len(greekword):											# if greeklish word is shorter map a latin to 2 greek
			i = 0
			for eletter in grengword:
				if eletter in 'ABCFKLMNOPQRSTVWXZ' or E[engdict[eletter]].count(greekword[i]) > 3:
					i = i + 1
				else:
					newletter = greekword[i] + greekword[i+1]
					i = i + 2
					E[engdict[eletter]].append(newletter)

greekf.close()																			# close files
grengf.close()

stats = open("./stats.txt","w")															# write stats in stats.txt

for letter in engdict:
	stats.write(letter + ": ")
	for i in count(E, engdict[letter]):
		stats.write(i[0].encode('utf-8') + ' %d \t' % i[1])								# write char and times it appears
	stats.write('\n')

stats.close()