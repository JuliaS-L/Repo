import os
import re
import itertools
import timeit
starttime = timeit.timeit()
print (starttime)
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input=[]
for x in f: 
    input.append(x.strip())

path = []
start = [0,0]
for x in range(len(input)): 
    if input[x].find('^')>0:
        start = [x,input[x].find('^')]
        path.append(start)
print (timeit.timeit())
new_start = start.copy()
dir = 'up'
while start[0]>=0 and start[0]<len(input) and start[1]>=0 and start[1]<len(input[0]):
# for x in range(30):
    tempstart = start.copy()
    if dir == 'up':
        tempstart[0] = start[0]-1
    elif dir=='down':
        tempstart[0] = start[0]+1
    elif dir=='right':
        tempstart[1] = start[1]+1
    elif dir=='left':
        tempstart[1] = start[1]-1
    if tempstart[0]<0 or tempstart[0]>=len(input) or tempstart[1]<0 or tempstart[1]>=len(input[0]):
        start=tempstart
        print (len(path))
    else:
        if input[tempstart[0]][tempstart[1]] in (".",'^'):
            if tempstart not in path:
                path.append(tempstart)
            start = tempstart
        else:
            if dir =='up':
                dir='right'
            elif dir=='down':
                dir='left'
            elif dir=='right':
                dir='down'
            elif dir=='left':
                dir='up'

print ("Part 1", timeit.timeit())
blockages = 0
def run_path(new_path,blockage,start,dir):
    while (start[0]>=0 and start[0]<len(input) and start[1]>=0 and start[1]<len(input[0])):
        tempstart = start.copy()
        if dir == 'up':
            tempstart[0] = start[0]-1
        elif dir=='down':
            tempstart[0] = start[0]+1
        elif dir=='right':
            tempstart[1] = start[1]+1
        elif dir=='left':
            tempstart[1] = start[1]-1
        if [tempstart[0],tempstart[1],dir] in new_path:
            return 1
        else:
            if tempstart[0]<0 or tempstart[0]>=len(input) or tempstart[1]<0 or tempstart[1]>=len(input[0]):
                return 0
            else:
                if input[tempstart[0]][tempstart[1]] in (".",'^') and [tempstart[0],tempstart[1]]!=blockage:
                    new_path.append([tempstart[0],tempstart[1],dir])
                    start = tempstart
                else:
                    if dir =='up':
                        dir='right'
                    elif dir=='down':
                        dir='left'
                    elif dir=='right':
                        dir='down'
                    elif dir=='left':
                        dir='up'


for x in range(len(path)):
    blockages+=run_path([new_start[0],new_start[1],'up'],path[x],new_start,'up')

# blockage has to be on the path i found above rather than trying every dot
# instead of each time finding the path from the beginning i should start where i last stopped.
print (blockages)
end = timeit.timeit()
print(end,end - starttime)