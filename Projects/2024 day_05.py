import os
import re
import itertools
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
rules =[]
updates = []
for x in f: 
    if x.find("|")>0:
        rules.append(x.strip())
    elif x.find(",")>0:
        updates.append(x.strip())
valids=[]
invalids=[]
for x in updates: 
    pages = x.split(",")
    state=True
    for item in itertools.combinations(pages, 2):
        if (item[1]+"|"+item[0]) in rules:
            state=False
    if state:
        valids.append(x) 
    else:
        invalids.append(x)

part1sum = 0
part2sum = 0
for x in valids: 
    x=x.split(",")
    part1sum+=int(x[int((len(x) - 1)/2)])
print (part1sum)

for x in invalids: 
    order = x.split(",")
    # print (order)
    for item in itertools.combinations(range(len(order)), 2):
        # print (order[item[1]]+"|"+order[item[0]])
        if (order[item[1]]+"|"+order[item[0]]) in rules:
            order[item[1]], order[item[0]] = order[item[0]], order[item[1]]
        # print (order)
    part2sum+=int(order[int((len(order) - 1)/2)])
print (part2sum)
