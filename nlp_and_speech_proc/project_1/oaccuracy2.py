# -*- coding: utf-8 -*-
import codecs
from os import system
import string

def make_word(file):
	word = ""
	for line in file.readlines():
		if not line.startswith("0") and "<eps>" not in line:
			word = line.split()[3] + word
	return word;

with codecs.open("./slp_spell_data/test_wr.txt","r",encoding='utf-8') as wr, codecs.open("./slp_spell_data/test_co.txt","r",encoding='utf-8') as co, open("./otranslationS2.txt","w") as tran2, open("./oaccuracyS2.txt","w") as stats2:
	wr = [i.split() for i in wr.readlines()]
	co = [i.split() for i in co.readlines()]
	all_words = correct = blank = wrong = 0
	for line in range(len(wr)):
		for word in range(len(wr[line])):
			i = 0
			with codecs.open("./oW.txt","w",encoding='utf-8') as fst:
				for letter in wr[line][word]:
					fst.write("%d %d %s %s 0\n" %(i,i+1,letter,letter))
					i = i + 1
				fst.write("%d 0\n" %i)
			system('fstcompile --isymbols=syms.txt --osymbols=syms.txt oW.txt oW.fst')
			system('fstcompose oW.fst oS2.fst out.fst')
			system('fstcompose out.fst A1_opt.fst oFS2.fst')
			system('fstshortestpath oFS2.fst oFS2.fst')
			system('fstprint --isymbols=syms.txt --osymbols=syms.txt oFS2.fst > temp.txt')
			with open("./temp.txt","r") as temp:
				orthographed = make_word(temp)
			tran2.write(orthographed + " ")
			all_words = all_words + 1
			if orthographed == co[line][word].encode('utf-8'):
				correct = correct + 1
			elif orthographed == "":
				blank = blank + 1
			else:
				wrong = wrong + 1
		tran2.write("\n")
	stats2.write("Correct orthographed words: %d %.3f%%\n"%(correct,round(float(correct)*100/all_words,3)))
	stats2.write("Words not orthographed at all (not in the dictionary): %d %.3f%%\n"%(blank,round(float(blank)*100/all_words,3)))
	stats2.write("Wrong orthographed words: %d %.3f%%\n"%(wrong,round(float(wrong)*100/all_words,3)))