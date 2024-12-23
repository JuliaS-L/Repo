import os
import re
import itertools
import collections
import sympy
from functools import reduce
import time
start_time = time.time()
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))

program = []
for x in f: 
    program.append(int(x.strip()))
# print (program)

def secret_number(x):
    mult = x*64
    x = x^mult
    x = x%16777216
    div= int(x/32)
    x = x^div
    x = x%16777216
    multi = x*2048
    x = x^multi
    x = x%16777216
    return x
result = 0
for x in program: 
    for y in range(2000):
        x = secret_number(x)
    result+=x
print ("Part 1",result)

sequence_lists = [] # set of 4 sequences
diff_sequence_lists = [] #set of all difference lists across inputs
sequences = []
for x in program: 
    sequence = [x%10]
    for y in range(2000):
        x = secret_number(x)
        sequence.append(x%10)
    diff_sequence = []
    for c in range(1,len(sequence)):
        diff_sequence.append(sequence[c]-sequence[c-1])
    # print (diff_sequence)
    for i in range(0, len(diff_sequence)-4, 1):
        # if diff_sequence[i : i + 4] not in sequence_lists:
        sequence_lists.append('.'+'.'.join(str(i) for i in diff_sequence[i : i + 4])) # i should go for unique ones only
    diff_sequence_lists.append('.'.join(str(i) for i in diff_sequence))
    sequences.append(sequence)
sequence_lists = list(set(sequence_lists))
print (len(sequence_lists)) #3421144
# set from list reduces it to 40951
bananas = 0
best_seq = ''
counter =0
# checked_sequences=[]
for x in sequence_lists:
    counter+=1
    seq = x
    score=0
    if counter%1000==0:
        print(counter,bananas)
    for c,y in enumerate(diff_sequence_lists):
        if seq in y:
            start_of_seq = y.index(seq)
            dots = y[:start_of_seq+len(seq)+1].count(".")
            banana =sequences[c][dots]
            score+=banana
    if score>bananas:
        bananas = score
        best_seq = seq
print ("Part 2",bananas,best_seq)
# this runs, gets the right result on sample, but is not performant on main input