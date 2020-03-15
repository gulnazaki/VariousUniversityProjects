# -*- coding: utf-8 -*-
import codecs

with codecs.open("./slp_spell_data/train_wr.txt","r",encoding='utf-8') as wr, codecs.open("./slp_spell_data/train_co.txt","r",encoding='utf-8') as co:
	wr = [i.split() for i in wr.readlines()]
	co = [i.split() for i in co.readlines()]
	WR = []
	CO = []
	insertions = deletions = subs = swaps = 0
	for line in range(len(wr)):
		for word in range(len(wr[line])):
			wrong = wr[line][word]
			correct = co[line][word]
			if wrong == correct:
				pass
			else:
				if len(wrong) > len(correct):
					j = 0
					for i in range(len(correct)):
						if wrong[j] == correct[i]:
							j+=1
						elif wrong[j+1:] == correct[i:]:
							insertions+=1
							break
						else:
							WR.append((wrong[:j] + wrong[(j+1):],"in"))
							CO.append(correct)
							break
				elif len(wrong) < len(correct):
					j = 0
					for i in range(len(wrong)):
						if wrong[i] == correct[j]:
							j+=1
						elif wrong[i:] == correct[j+1:]:
							deletions+=1
							break
						else:
							WR.append((wrong[:i] + correct[j] + wrong[i:],"del"))
							CO.append(correct)
							break
				else:
					for i in range(len(wrong)):
						if wrong[i] == correct[i]:
							pass
						elif wrong[i+1:] == correct[i+1:]:
							subs+=1
							break
						elif wrong[i+1] == correct[i+1]:
							WR.append((wrong[:i] + correct[i] + wrong[i+1:],"sub"))
							CO.append(correct)
							break
						elif wrong[i+1] == correct[i] and wrong[i] == correct[i+1] and wrong[i+2:] == correct[i+2:]:
							swaps+=1
							break
	
	for i in range(len(WR)):
		correct = CO[i]
		wrong = WR[i][0]
		prev = WR[i][1]
		if len(wrong) > len(correct):
			j = 0
			for i in range(len(correct)):
				if wrong[j] == correct[i]:
					j+=1
				elif wrong[j+1:] == correct[i:]:
					insertions+=1
					if prev == "sub":
						subs+=1
					elif prev == "del":
						deletions+=1
					else:
						insertions+=1
					break
		elif len(wrong) < len(correct):
			j = 0
			for i in range(len(wrong)):
				if wrong[i] == correct[j]:
					j+=1
				elif wrong[i:] == correct[j+1:]:
					deletions+=1
					if prev == "sub":
						subs+=1
					elif prev == "del":
						deletions+=1
					else:
						insertions+=1
					break
		else:
			for i in range(len(wrong)):
				if wrong[i] == correct[i]:
					pass
				elif wrong[i+1:] == correct[i+1:]:
					subs+=1
					if prev == "sub":
						subs+=1
					elif prev == "del":
						deletions+=1
					else:
						insertions+=1
					break
				elif wrong[i+1] == correct[i+1]:
					print wrong
					break
				elif wrong[i+1] == correct[i] and wrong[i] == correct[i+1] and wrong[i+2:] == correct[i+2:]:
					swaps+=1
					break

total = insertions + deletions + subs + swaps

with open("./omistakes.txt","w") as txt:
	txt.write("Total Mistakes: %d\n" %total)
	txt.write("Insertions: %d\t%.2f%%\n" %(insertions,round(float(insertions*100)/total,2)))
	txt.write("Deletions: %d\t%.2f%%\n" %(deletions,round(float(deletions*100)/total,2)))
	txt.write("Substitutions: %d\t%.2f%%\n" %(subs,round(float(subs*100)/total,2)))
	txt.write("Swaps: %d\t%.2f%%\n" %(swaps,round(float(swaps*100)/total,2)))