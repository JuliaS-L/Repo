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
sizex=101
sizey=103
quad1=0
quad2=0
quad3=0
quad4=0
for x in f: 
    input.append(x.strip())
for x in input: 
    xp = int(x[x.find("=")+1:x.find(",")])
    yp = int(x[x.find(",")+1:x.find(" ")])
    v = x[x.find("v="):]
    xv = int(v[v.find("=")+1:v.find(",")])
    yv = int(v[v.find(",")+1:])
    posx100 = (xp+xv*100)%sizex
    posy100 = (yp+yv*100)%sizey
    if posx100<int(sizex/2):
        if posy100<int(sizey/2):
            quad1+=1
        elif posy100>int(sizey/2):
            quad2+=1
    elif posx100>int(sizex/2):
        if posy100<int(sizey/2):
            quad3+=1
        elif posy100>int(sizey/2):
            quad4+=1

print (quad1*quad2*quad3*quad4)

for rep in range(7132):
    robots = []
    for x in input: 
        xp = int(x[x.find("=")+1:x.find(",")])
        yp = int(x[x.find(",")+1:x.find(" ")])
        v = x[x.find("v="):]
        xv = int(v[v.find("=")+1:v.find(",")])
        yv = int(v[v.find(",")+1:])
        robots.append( ((xp+xv*rep)%sizex, (yp+yv*rep)%sizey))

    for x in robots: 
        if (x[0],x[1]+1) in robots and (x[0],x[1]+2) in robots and (x[0],x[1]+3) in robots and (x[0],x[1]+4) in robots and (x[0],x[1]+5) in robots and (x[0],x[1]+6) in robots and (x[0],x[1]+7) in robots and (x[0],x[1]+8) in robots and (x[0],x[1]+9) in robots:
            print (rep)
            for x in range (sizex):

                res = ""
                for y in range(sizey):
                    if (x,y) in robots:
                        res+="x"
                    else:
                        res+="."
                print(res)
