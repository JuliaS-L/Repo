import os
import re
import itertools
import sympy
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input=[]
sum=0
sum2 = 0
trailheads=[]
for x in f: 
    input.append(x.strip())
for x in range(len(input)): 
    for y in range(len(input[x])):
        if input[x][y]=="0":
            trailheads.append([x,y])
print (trailheads)

def find_next_step(x):
    current_step = input[x[0]][x[1]]
    output = []
    input[x[0]][min(len(input[0])-1,x[1]+1)]==str(int(current_step)+1) and output.append((x[0],x[1]+1))
    input[x[0]][max(x[1]-1,0)]==str(int(current_step)+1) and output.append((x[0],x[1]-1))
    input[min(len(input[0])-1,x[0]+1)][x[1]]==str(int(current_step)+1) and output.append((x[0]+1,x[1]))
    input[max(x[0]-1,0)][x[1]]==str(int(current_step)+1) and output.append((x[0]-1,x[1]))
    return output



for a in trailheads:
    ones=[]
    twos=[]
    threes=[]
    fours=[]
    fives=[]
    sixes=[]
    sevens=[]
    eights=[]
    nines=[]
    ones = find_next_step(a)
    for b in ones: 
        twos += find_next_step(b)
    for c in twos:
        threes += find_next_step(c)
    for d in threes: 
        fours += find_next_step(d)
    for e in fours:
        fives += find_next_step(e)
    for f in fives:
        sixes += find_next_step(f)
    for g in sixes:
        sevens += find_next_step(g)
    for h in sevens:
        eights+=find_next_step(h)
    for i in eights:
        nines += find_next_step(i)
    sum+=len(set(nines))
    sum2+=len(nines)
print (sum)
print (sum2)