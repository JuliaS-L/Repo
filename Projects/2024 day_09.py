import os
import re
import itertools
import sympy
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input=""
sum=0
for x in f: 
    input+=x.strip()
list = []
for x,y in enumerate(input):
    # print (x,y,int(x)%2)
    if int(x)%2!=0 or x=="0":
        for z in range(int(y)):
            list.append(".")
    else:
        for z in range(int(y)):
            list.append(str(int(int(x)/2)))

old_list = list.copy()
while "." in list:
    while list[-1]==".":
        list = list[:-1]
    list = list[:list.index(".")]+[list[-1]]+list[list.index(".")+1:-1]

for x,y in enumerate(list):
    sum+=x*int(y)
print("part 1",sum)
empty_list = ""
for x in old_list: 
    if x==".":
        empty_list+="."
    else:
        empty_list+="1"

# print (old_list,empty_list)
for x in range(int(old_list[-1])+1)[::-1]:              ## loop through every id
    counting = old_list.count(str(x))                   ## how many of this id exist in the list
    max_pos = old_list.index(str(x))                    ## since an id can only move forward we only want to check up until their current position
    postition = empty_list[:max_pos].find("."*counting) ## find if there is a position where this could fit
    if postition>0:                                     ## if you find an empty space that fits
        for z in range(counting):        ## remove the values from the list from their existing positions 
            old_list[max_pos+z]="."
        for y in range(counting):               
            old_list[postition+y]=str(x)                ## replace the places where there are dots with these numbers
        empty_list = empty_list[:postition]+"1"*counting+empty_list[postition+counting:]
part2sum = 0
# print (old_list)
for x,y in enumerate(old_list):
    if y!=".":
        part2sum+=x*int(y)

print ("part2",part2sum)
