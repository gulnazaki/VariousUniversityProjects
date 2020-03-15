# -*- coding: utf-8 -*-
import string

with open("./stats.txt","r") as stats, open("./probs.txt","w") as probs, open("./syms.txt","w") as syms:
    # open stats.txt to read statistics, convert it to probabilities (probs.txt) and create symbols to be used for the fst-compiler
    syms.write("<eps> 0\n")
    num = 1                                                                   # ascending order of symbols
    I = []
    syms.write("<eps> 0\n")
    O = []                                                                     # list containing output symbols so we dont print them again when we encounter them
    for line in stats:
        if line[0] in string.ascii_uppercase or line[0].isdigit():              
            latin,rest = line.split(":")                                       # split original letters (latin or nums) and the converted characters (greek)
            syms.write(latin + " %d\n" %num)
            num = num + 1
            I.append(latin)
            probs.write(latin + ": ")  
            grstats = rest.split()                                             # split greek letters (grstats is a letter - digit set)
            sum = 0
            for i in grstats:
            	if i.isdigit():                                                # total corresponding number (sum)
                	sum = sum + int(i)
            for i in grstats:
                if i.isdigit():
                    probs.write("%f\t" %(float(i)/sum))                        # calculate probability
                else:
                    probs.write(i + "->")
                    if i in O:
                        pass
                    else:
                        syms.write(i + " %d\n" %num)
                        num = num + 1
                        O.append(i)
            probs.write("\n")
    
    for char in string.ascii_uppercase:
        if char not in I:
            syms.write(char + " %d\n" %num)
            num = num + 1