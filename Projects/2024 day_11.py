import os
import re
import itertools
import sympy
import time
start_time = time.time()
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input=[]
for x in f: 
    input.append(x.strip().split(" "))
input=input[0]
start = input
def change_stones(input):
    new_input = []
    for x in input: 
        if x=="0":
            new_input.append("1")
        elif len(x)%2==0:
            new_input.append(str(int(x[:len(x)//2])))
            new_input.append(str(int(x[len(x)//2:])))
        else:
            new_input.append(str(int(x)*2024))
    return new_input
for x in range(25):
    input = change_stones(input)
print (len(input))
## PART 2
print ( time.time()-start_time)
length = 0
tuple = []
for x in range(len(start)): 
    tuple.append((start[x],start.count(start[x]))) # create a tuple with stones and their count
tuple = dict(tuple)

for r in range(75):
    new_tuple = {}
    for x in tuple: 
        new_values = change_stones([x])
        for y in new_values:
            if y in new_tuple:
                new_tuple[y]+=tuple[x]
            else:
                new_tuple[y] = tuple[x]
    tuple = new_tuple.copy()
print ( time.time()-start_time)
print (sum(tuple.values()))

