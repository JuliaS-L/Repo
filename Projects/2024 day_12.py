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
    input.append(x.strip())
areas = [(0,0)]
rows = len(input)-1
cols = len(input[0])-1
for x in range(len(input)):
    for y in range(len(input[x])): 
        if y==0 and input[x][y]!= input[max(x-1,0)][y]: # first column, so we just look up
            areas.append((x,y))
        if x==0 and input[x][y]!= input[x][max(y-1,0)]: # first row, so we just look left
            areas.append((x,y))
        elif input[x][y]!= input[x][max(y-1,0)] and input[x][y]!= input[max(x-1,0)][y]:
            areas.append((x,y))
result_part1 = 0
result_part2 = 0
forbidden_list = []
for a in areas: 
    if a not in forbidden_list:
        letter = input[a[0]][a[1]]
        area = [a]
        finding = True
        while finding==True: 
            add_area = []
            for b in area:
                x,y = b[0],b[1]
                if input[min(rows,x+1)][y]==letter: #down
                    add_area.append((min(rows,x+1),y))
                    (min(rows,x+1),y) in areas and forbidden_list.append((min(rows,x+1),y))
                if input[x][min(cols,y+1)]==letter: #right
                    add_area.append((x,min(cols,y+1)))
                    (x,min(cols,y+1)) in areas and forbidden_list.append((x,min(cols,y+1)))
                if input[x][max(y-1,0)]==letter:    #left
                    add_area.append((x,max(0,y-1)))
                    (x,max(0,y-1)) in areas and forbidden_list.append((x,max(0,y-1))) 
                if input[max(x-1,0)][y]==letter:    #UP
                    add_area.append((max(x-1,0),y))
                    (max(x-1,0),y) in areas and forbidden_list.append((max(x-1,0),y)) 

            add_area = list(set(add_area))
            if set(add_area).issubset(area):
                finding=False
            else:
                area=list(set(area+add_area))
        areavalue = len(area)
        perimeter = areavalue*4
        for x in area: 
            if (x[0]+1,x[1]) in area:#down
                perimeter-=1
            if (x[0],x[1]+1) in area:#right
                perimeter-=1
            if (x[0]-1,x[1]) in area:#up
                perimeter-=1
            if (x[0],x[1]-1) in area:#left
                perimeter-=1
        result_part1+=perimeter*areavalue

        sides = 0
        
        if len(area)==1:
            sides=4
        else:
            for x in area: 
                neighbors = [(x[0]-1,x[1]),(x[0]+1,x[1]),(x[0],x[1]-1),(x[0],x[1]+1)]
                diagonals = [(x[0]-1,x[1]-1),(x[0]+1,x[1]+1),(x[0]+1,x[1]-1),(x[0]-1,x[1]+1)]
                ## opposing neighbors, auto 0
                if len(set(neighbors) & set(area))==2 and ((neighbors[0] in area and neighbors[1] in area) or (neighbors[2] in area and neighbors[3] in area)): 
                    sides+=0
                ## 4 neighbors
                elif set(neighbors).issubset(area):
                    sides+=4-len(set(diagonals) & set(area))
                # IF 1 NEIGHBOR ADD 2
                elif len(set(neighbors) & set(area))==1:
                    sides+=2
                # IF 2 L shaped NEIGHBOR
                elif len(set(neighbors) & set(area))==2:
                    
                    two_corners = list(set(neighbors) & set(area))
                    diagonal = (two_corners[0][0]+two_corners[1][0]-x[0],two_corners[0][1]+two_corners[1][1]-x[1])
                    if diagonal in area:
                        sides+=1
                    else:
                        sides+=2
                else: # 3 neighbors
                    missing_neighbor = list(set(neighbors) - set(area))[0]
                    if x[0]==missing_neighbor[0]:
                        diagonals = [(missing_neighbor[0]+1,x[1]+x[1]-missing_neighbor[1]),(missing_neighbor[0]-1,x[1]+x[1]-missing_neighbor[1])]
                    else:
                        diagonals = [(x[0]+x[0]-missing_neighbor[0],missing_neighbor[1]+1),(x[0]+x[0]-missing_neighbor[0],missing_neighbor[1]-1)]
                    sides+=len(set(diagonals)-set(area))
        result_part2+=sides*areavalue



print ( time.time()-start_time)
print (result_part1)
print (result_part2)



