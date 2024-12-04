import os
import re
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input =[]
input+= [list(range(142))] # cheating by appending this first and hardcoding the length
for x in f:
    values = list(x)
    values.insert(0,0)
    values = values[:-1]
    values.insert(len(values), 0)
    input.append(values)
    # print (len(values))
length = len(values)
# print (length)
buffer = list(range(length))
input.append(buffer)
# print (input)

# ## possible part 2? if all directions were allowed, like 
                                # XM
                                # SA

validx=[]
# validm=[]
# valida=[]
# valids=[]

# def checkvalids_around (validlist,coordinates,letter):
#     x=coordinates[0]
#     y=coordinates[1]
#     input[x-1][y-1]==letter and validlist.append([x-1,y-1]) 
#     input[x-1][y]==letter and validlist.append([x-1,y])
#     input[x-1][y+1]==letter and validlist.append([x-1,y+1])
#     input[x][y-1]==letter and validlist.append([x,y-1])
#     input[x][y+1]==letter and validlist.append([x,y+1])
#     input[x+1][y-1]==letter and validlist.append([x+1,y-1])
#     input[x+1][y]==letter and validlist.append([x+1,y])
#     input[x+1][y+1]==letter and validlist.append([x+1,y+1])

# for x in range(len(input)):
#     for y in range(len(input)):
#         # find all x
#         if input[x][y]=='X':
#             validx+=[[x,y]] 

# for x in validx:
#     checkvalids_around(validm,x,'M')
# for x in validm:
#     checkvalids_around(valida,x,'A')
# for x in valida:
#     checkvalids_around(valids,x,'S')
# print (len(valids))


for x in range(len(input)):
    for y in range(len(input)):
        # find all x
        if input[x][y]=='X':
            validx+=[[x,y]] 
# print (validx)
part1count=0
for z in validx:
    x=z[0]
    y=z[1]
    if input[x-1][y-1]=='M' and input[max(0,x-2)][max(0,y-2)]=='A' and input[max(x-3,0)][max(y-3,0)]=='S':
        part1count+=1
    if input[x-1][y]== 'M' and input[max(0,x-2)][y]=='A' and input[max(x-3,0)][y]=='S':
        part1count+=1
    if input[x-1][y+1]=='M' and input[max(0,x-2)][min(length,y+2)]=='A' and input[max(x-3,0)][min(y+3,length)]=='S':
        part1count+=1
    if input[x][y-1]=='M' and input[x][max(0,y-2)]=='A' and input[x][max(y-3,0)]=='S':
        part1count+=1
    if input[x][y+1]=='M' and input[x][min(length,y+2)]=='A' and input[x][min(y+3,length)]=='S':
        part1count+=1
    if input[x+1][y-1]=='M' and input[min(length,x+2)][max(0,y-2)]=='A' and input[min(length,x+3)][max(y-3,0)]=='S':
        part1count+=1
    if input[x+1][y]=='M' and input[min(length,x+2)][y]=='A' and input[min(length,x+3)][y]=='S':
        part1count+=1
    if input[x+1][y+1]=='M' and input[min(length,x+2)][min(length,y+2)]=='A' and input[min(length,x+3)][min(y+3,length)]=='S':
        part1count+=1
print('part1count',part1count/2) 
## not sure why I am double counting 

part2count=0
validA = []
for x in range(len(input)):
    for y in range(len(input)):
        # find all x
        if input[x][y]=='A':
            validA+=[[x,y]] 
for z in validA:
    x=z[0]
    y=z[1]
    if ((input[x-1][y-1]=='M' and input[x+1][y+1]=='S') or (input[x-1][y-1]=='S' and input[x+1][y+1]=='M')) and ((input[x+1][y-1]=='M' and input[x-1][y+1]=='S') or (input[x+1][y-1]=='S' and input[x-1][y+1]=='M')):
        
        part2count+=1
print (part2count)