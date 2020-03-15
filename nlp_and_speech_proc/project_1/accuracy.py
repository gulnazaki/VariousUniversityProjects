from os import system
import string

def make_word(file):
	word = ""
	for line in file.readlines():
		if not line.startswith("0") and "<eps>" not in line:
			word = line.split()[3] + word
	return word;

with open("./data/test_greng.txt","r") as greng, open("./data/test_gr.txt","r") as gr, open("./translation.txt","w") as tran, open("./accuracy.txt","w") as stats:
	greng = [i.split() for i in greng.readlines()]
	gr = [i.split() for i in gr.readlines()]
	all_words = correct = engr = blank = wrong = 0
	for line in range(len(greng)):
		for word in range(len(greng[line])):
			i = 0
			with open("./W.txt","w") as fsa:
				for letter in greng[line][word]:
					fsa.write("%d %d %s %s 0\n" %(i,i+1,letter,letter))
					i = i + 1
				fsa.write("%d 0\n" %i)
			system('fstcompile --isymbols=syms.txt --osymbols=syms.txt W.txt W.fst')
			system('fstcompose W.fst T.fst Final.fst')
			system('fstshortestpath Final.fst Final.fst')
			system('fstprint --isymbols=syms.txt --osymbols=syms.txt Final.fst > temp.txt')
			with open("./temp.txt","r") as temp:
				translated = make_word(temp)
				print translated
			tran.write(translated + " ")
			all_words = all_words + 1
			if translated == gr[line][word]:
				correct = correct + 1
			elif translated == "":
				blank = blank + 1
			elif translated[0] not in string.ascii_uppercase and gr[line][word][0] in string.ascii_uppercase:
				engr = engr + 1
			else:
				wrong = wrong + 1
		tran.write("\n")
	stats.write("Correct translated words: %d %.3f%%\n"%(correct,round(float(correct)*100/all_words,3)))
	stats.write("English words translated to Greek: %d %.3f%%\n"%(engr,round(float(engr)*100/all_words,3)))
	stats.write("Words not existing in dictionaries: %d %.3f%%\n"%(blank,round(float(blank)*100/all_words,3)))
	stats.write("Wrong translated words: %d %.3f%%\n"%(wrong,round(float(wrong)*100/all_words,3)))