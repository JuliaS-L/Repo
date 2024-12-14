import os
import re
import itertools
import sympy
from functools import reduce
import time
start_time = time.time()
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input=[]
result=0
for x in f: 
    input.append(x.strip())
for x in range(int((len(input)+1)/4)):
    ax = int(input[4*x][input[4*x].find("X+")+2:input[4*x].find(",")])
    bx = int(input[4*x+1][input[4*x+1].find("X+")+2:input[4*x+1].find(",")])
    ay = int(input[4*x][input[4*x].find("Y+")+2:])
    by = int(input[4*x+1][input[4*x+1].find("Y+")+2:])
    px = int(input[4*x+2][input[4*x+2].find("X=")+2:input[4*x+2].find(",")])
    py = int(input[4*x+2][input[4*x+2].find("Y=")+2:])
    state=[100,0]
    while state[0]>=0:
        while px>(state[0]*ax+state[1]*bx) and py>(state[0]*ay+state[1]*by):
            state[1]+=1
        if px==(state[0]*ax+state[1]*bx) and py==(state[0]*ay+state[1]*by):
            result+=state[0]*3+state[1]
            # print (state[0]*3+state[1],state)
            state[0]=-1
        else:
            state[0]-=1
            state[1]=0
print ("Part 1", result)

result=0


for x in range(int((len(input)+1)/4)):
    ax = int(input[4*x][input[4*x].find("X+")+2:input[4*x].find(",")])
    bx = int(input[4*x+1][input[4*x+1].find("X+")+2:input[4*x+1].find(",")])
    ay = int(input[4*x][input[4*x].find("Y+")+2:])
    by = int(input[4*x+1][input[4*x+1].find("Y+")+2:])
    px = int(input[4*x+2][input[4*x+2].find("X=")+2:input[4*x+2].find(",")])+10000000000000
    py = int(input[4*x+2][input[4*x+2].find("Y=")+2:])+10000000000000
    

    A = (px*by - py*bx) / (ax*by - ay*bx)
    B = (ax*py - ay*px) / (ax*by - ay*bx)
    if A%1==0 and B%1==0:
        result+=int(A*3+B)
print (result)