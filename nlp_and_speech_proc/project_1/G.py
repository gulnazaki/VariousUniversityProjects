import math

probs =  open("./probs.txt","r")				# open file with probability data
fst = open("./G.txt","w")						# write fst data in G.txt

lines = probs.readlines()						# lines = list containing all file lines

for line in lines:
	latin,rest = line.split(":")				# latin characters are before ":", rest of the line is greek chars and probabilities
	grprobs = rest.split()						# split greek characters->probs
	for i in grprobs:
		letter,weight = i.split("->")			# split greek characters and their probs
		weight = -math.log10(float(weight))		# cost is the negative logarithm of probability
		if len(latin) == 2:
			if latin[0] == "T":
				fst.write("0 1 %s %s %f\n" %(latin[0],letter,weight))
				fst.write("1 3 %s %s 0\n" %(latin[1],"<eps>"))
			elif latin[0] == "P":
				fst.write("0 2 %s %s %f\n" %(latin[0],letter,weight))
				fst.write("2 3 %s %s 0\n" %(latin[1],"<eps>"))
			elif latin[0] == "K":
				fst.write("0 2 %s %s %f\n" %(latin[0],letter,weight))
		else:
			fst.write("0 3 %s %s %f\n" %(latin,letter,weight))		# write in Arc appropriate form

fst.write("3 0\n")								# final state

probs.close()									# close files
fst.close()