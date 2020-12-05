#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict as od
from pydub import AudioSegment
from pydub.playback import play
import random, os

l = [
	(" ΤΗΝ ", " ΤΗ "),
	(" ΣΤΗΝ ", " ΣΤΗ "),
	(" ΤΟΝ ", " ΤΟ "),
	(" ΣΤΟΝ ", " ΣΤΟ "),
	("ΠΠ", "Π"),
	("ΜΜ", "Μ"),
	("ΚΚ", "Κ"),
	("ΛΛ", "Λ"),
	("ΝΝ", "Ν"),
	("ΤΤ", "Τ"),
	("ΓΚ","ΓΓ"),
	("ΑΥ","ΑΦ"),
	("ΕΥ","ΕΒ"),
	("ΕΙ","Ι"),
	("ΑΙ","Ε"),
	("ΟΙ","Ι"),
	("Η","Ι"),
	("Ω","Ο"),
	("Υ","Ι")]
l = od(l)

def check_validity(inp):
	if len(inp) == 0:
		return False
	for i in inp.decode("UTF-8"):
		if not ((i >= u"Α" and i <= u"Ω") or i == u" "):
			return False
	return True

def read_input():
	print "Πληκτρολογήστε αυτό που νομίζετε πως ακούσατε (κεφαλαία χωρίς τόνους):"
	inp = raw_input()
	while (not check_validity(inp)):
		print "Παρακαλώ πληκτρολογήστε ελληνικά κεφαλαία χωρίς τόνους!"
		inp = raw_input()
	return inp

def lbtmz(inp):
	for k,v in l.items():
		inp = inp.replace(k,v)
	# restore all "ΟΥ"s
	inp = inp.replace("ΟΙ", "ΟΥ")
	# need special treatment for the word "ΤΣΑΙ"
	inp = inp.replace("ΤΣΕ", "ΤΣΑΙ")
	inp = inp.replace("ΤΣΑΦ", "ΤΣΑΙ")
	# we replace also "ΤΣΕΠΗ" potential changes
	inp = inp.replace("ΤΣΑΙΠΙ", "ΤΣΕΠΙ")
	# and "ΠΡΩΙ"
	inp = inp.replace("ΠΡΟΥ", "ΠΡΟΙ")
	inp = inp.replace("ΠΡΙ" , "ΠΡΟΙ")

	return inp

def correct(inp, sentence):
	sentence = sentence[:-2]
	return lbtmz(inp) == lbtmz(sentence)

# redirect stderror
fd = os.open('/dev/null', os.O_WRONLY)
os.dup2(fd, 2)

# number of available sentences
sen_avail = 30

# number of noise levels
noise_n = 7

# number of sentences to be tested
sen_n = noise_n * 2

# data preparation:
# import sentences from recorded files
sentences = []
for n in xrange(1, sen_avail+1):
	sentences.append(AudioSegment.from_file("sentences/" + str(n) + ".wav"))

# import different intensity level noises
noise = []
for n in xrange(1, 8):
	noise.append(AudioSegment.from_file("noise/n_" +str(n) +".wav"))

# a list to store already tested sentences
indexes = []

# a list to store right/wrong answers
stats = []

# hidden hearing loss test:
print "\n~~~~~ Hidden Hearing Loss Test ~~~~~\n"
print "Θα ακούσετε 14 προτάσεις. Πληκτρολογήστε αυτό που νομίζετε ότι ακούσατε, με κεφαλαίους ελληνικούς χαρακτήρες (χωρίς τόνους)."
print "Πατήστε <Enter> για να ξεκινήσετε."
raw_input()

with open("sentences/sentences.txt","r") as file:
	correct_sentences = file.readlines()
	
for n in range(sen_n):
	rand = random.randint(0, sen_avail-1)
	while rand in indexes:
		rand = random.randint(0, sen_avail-1)
	indexes.append(rand)
	print "Πρόταση " + str(n+1) + " από " + str(sen_n)
	play(sentences[rand].overlay(noise[n/2]))

	inp = read_input()
	stats.append(correct(inp, correct_sentences[rand]))
	if correct(inp, correct_sentences[rand]):
		print "\nΣωστή απάντηση"
	else:
		print "\nΛάθος απάντηση"
	print "Γράψατε   -> %s" % inp
	print "Ακούστηκε -> %s" % correct_sentences[rand]

print "Ακούσατε σωστά %d στις %d προτάσεις (%0.2f%%)" % (stats.count(True), sen_n, ((stats.count(True)*100.0)/sen_n))
