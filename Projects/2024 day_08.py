import os
import re
import itertools
import sympy
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input=""
antinode=[]
for x in f: 
    input+=x.strip()
    length = len(x.strip())
antennas = list(set(input))
antennas.remove(".")

for x in antennas:
    positions = [i for i, y in enumerate(input) if y==x]
    pairs = [x for x in itertools.combinations(positions, 2)]
    for p in pairs: 
        dist_x = p[1]//length-p[0]//length
        dist_y = p[1]%length-p[0]%length
        higher_point = p[1]+dist_x*length + dist_y
        lower_point = p[0]-dist_x*length - dist_y
        # print (p,dist_x,dist_y,higher_point,lower_point)
        if higher_point<len(input) and (p[1]//length+ dist_x)==higher_point//length:
            antinode.append(higher_point)
        if lower_point>0 and (p[0]//length- dist_x)==lower_point//length:
            antinode.append(lower_point)
print (len(set(antinode)))

## PART 2
antinode2=[]
for x in antennas:
    positions = [i for i, y in enumerate(input) if y==x]
    pairs = [x for x in itertools.combinations(positions, 2)]
    # print (pairs)
    for p in pairs: 
        dist_x = p[1]//length-p[0]//length
        dist_y = p[1]%length-p[0]%length
        # print (dist_x,dist_y)
        for r in range(int(length/min(abs(dist_x),abs(dist_y)))):

            higher_point = p[1]+dist_x*r*length + dist_y*r
            lower_point = p[0]-dist_x*r*length - dist_y*r
            # print (higher_point,lower_point)
            if higher_point<len(input) and (p[1]//length+ dist_x*r)==higher_point//length:
                antinode2.append(higher_point)
            if lower_point>=0 and (p[0]//length- dist_x*r)==lower_point//length:
                antinode2.append(lower_point)
# print (antinode2)
print (len(set(antinode2)))
