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
warehouse = []
steps = ""

for x in f: 
    if x[0]=="#":
        warehouse.append(x.strip())
    else:
        steps+=x.strip()
double_warehouse = warehouse.copy()
print (warehouse)

for x in range(len(warehouse)):
    for y in range(len(warehouse[x])):
        if warehouse[x][y]=="@":
            position = [x,y]
            break

double_position = position.copy()
for x in steps:
    if x=="<":
        new_position = [position[0],position[1]-1]
        dir = [0,-1]
    elif x==">":
        new_position = [position[0],position[1]+1]
        dir = [0,1]
    elif x=="v":
        new_position = [position[0]+1,position[1]]
        dir = [1,0]
    elif x=="^":
        new_position = [position[0]-1,position[1]]
        dir = [-1,0]
    if warehouse[new_position[0]][new_position[1]]=="#":
        # print ("nah ah")
        pass
    elif warehouse[new_position[0]][new_position[1]]==".":
        # print ("omw")
        newrow = warehouse[new_position[0]][:new_position[1]]+"@"+warehouse[new_position[0]][new_position[1]+1:]
        warehouse[new_position[0]]=newrow
        oldrow = warehouse[position[0]][:position[1]]+"."+warehouse[position[0]][position[1]+1:]
        warehouse[position[0]]=oldrow
        position = new_position
    else:
        # print ("Oh oh")
        temp_position = new_position.copy()
        while warehouse[temp_position[0]][temp_position[1]]=="O":
            temp_position[0]+=dir[0]
            temp_position[1]+=dir[1]
        if warehouse[temp_position[0]][temp_position[1]]=="#":
            pass
        else:
            newrow = warehouse[new_position[0]][:new_position[1]]+"@"+warehouse[new_position[0]][new_position[1]+1:]
            warehouse[new_position[0]]=newrow
            temprow = warehouse[temp_position[0]][:temp_position[1]]+"O"+warehouse[temp_position[0]][temp_position[1]+1:]
            warehouse[temp_position[0]]=temprow
            oldrow = warehouse[position[0]][:position[1]]+"."+warehouse[position[0]][position[1]+1:]
            warehouse[position[0]]=oldrow
            position = new_position
result = 0
for x in range(len(warehouse)): 
    for y in range(len(warehouse[x])):
        if warehouse[x][y]=="O":
            result+=100*x+y

print (result)

# PART 2
wide_warehouse=[]
for x in range(len(warehouse)): 
    row = ""
    for y in range(len(warehouse[x])):
        if double_warehouse[x][y]=="#":
            row+="##"
        elif double_warehouse[x][y]=="O":
            row+="[]"
        elif double_warehouse[x][y]==".":
            row+=".."
        elif double_warehouse[x][y]=="@":
            row+="@."
    wide_warehouse.append(row)

print (wide_warehouse)
for x in range(len(wide_warehouse)):
    for y in range(len(wide_warehouse[x])):
        if wide_warehouse[x][y]=="@":
            position = [x,y]
            break

for x in steps:
    flagg=''
    # print (x)
    if x=="<":
        new_position = [position[0],position[1]-1]
        dir = [0,-1]
    elif x==">":
        new_position = [position[0],position[1]+1]
        dir = [0,1]
    elif x=="v":
        new_position = [position[0]+1,position[1]]
        dir = [1,0]
    elif x=="^":
        new_position = [position[0]-1,position[1]]
        dir = [-1,0]
    if wide_warehouse[new_position[0]][new_position[1]]=="#":
        pass
    elif wide_warehouse[new_position[0]][new_position[1]]==".":
        newrow = wide_warehouse[new_position[0]][:new_position[1]]+"@"+wide_warehouse[new_position[0]][new_position[1]+1:]
        wide_warehouse[new_position[0]]=newrow
        oldrow = wide_warehouse[position[0]][:position[1]]+"."+wide_warehouse[position[0]][position[1]+1:]
        wide_warehouse[position[0]]=oldrow
        position = new_position
    else:
        print ("Oh oh")
        temp_position = new_position.copy()
        if dir[0]==0:
            while wide_warehouse[temp_position[0]][temp_position[1]]=="]" or wide_warehouse[temp_position[0]][temp_position[1]]=="[":
                temp_position[0]+=dir[0]
                temp_position[1]+=dir[1]
            if wide_warehouse[temp_position[0]][temp_position[1]]=="#":
                pass
            else:
                # print (position, new_position,temp_position)
                shifted = wide_warehouse[position[0]][min(position[1],new_position[1],temp_position[1])+1:max(position[1],new_position[1],temp_position[1])]
                # print (new_position,new_position[1],temp_position[1],shifted)
                if dir[1]==-1:
                    wide_warehouse[position[0]] = wide_warehouse[position[0]][:temp_position[1]]+shifted+"@."+wide_warehouse[position[0]][position[1]+1:]
                elif dir[1]==1:
                    wide_warehouse[position[0]] = wide_warehouse[position[0]][:position[1]]+".@"+shifted+wide_warehouse[position[0]][temp_position[1]+1:]
                position = new_position
        else: # we are moving up and down and are seeing a bracket
            # print ("up and down")
            tocheck = [new_position]
            flag = "ongoing"
            if wide_warehouse[new_position[0]][new_position[1]]=="[":
                tocheck.append([new_position[0],new_position[1]+1])
            else:
                tocheck.append([new_position[0],new_position[1]-1])
            new_tocheck=tocheck.copy()
            # print ("before while", new_tocheck)
            while flag == "ongoing":
                this_turn = new_tocheck.copy()
                # print("this turn",this_turn)
                new_tocheck=[]
                # print ("tocheck",tocheck)
                for c in this_turn:
                    # print (new_tocheck)
                    # print ("c",c)
                    # print (c,c[0]+dir[0],c[1]+dir[1],wide_warehouse[c[0]+dir[0]][c[1]+dir[1]])
                    if wide_warehouse[c[0]][c[1]]==wide_warehouse[c[0]+dir[0]][c[1]+dir[1]]:
                        # print ("its the same",new_tocheck)
                        new_tocheck.append([c[0]+dir[0],c[1]+dir[1]])
                        tocheck.append([c[0]+dir[0],c[1]+dir[1]])
                        # print (new_tocheck)
                    else: # i am going up and am seeing something thats not the same 
                        # print ("up and diff")
                        if wide_warehouse[c[0]+dir[0]][c[1]+dir[1]]=="#":
                            flag = "#"
                            flagg='#'
                            # print ("Nogo")
                        elif wide_warehouse[c[0]+dir[0]][c[1]+dir[1]]=="[":
                            # print ("we found a [",c[0]+dir[0],c[1]+dir[1])
                            # print (new_tocheck)
                            new_tocheck.append([c[0]+dir[0],c[1]+dir[1]])
                            new_tocheck.append([c[0]+dir[0],c[1]+dir[1]+1])
                            tocheck.append([c[0]+dir[0],c[1]+dir[1]])
                            tocheck.append([c[0]+dir[0],c[1]+dir[1]+1])
                            # print (new_tocheck)
                        elif wide_warehouse[c[0]+dir[0]][c[1]+dir[1]]=="]":
                            # print ("we found a ]",c[0]+dir[0],c[1]+dir[1])
                            new_tocheck.append([c[0]+dir[0],c[1]+dir[1]])
                            new_tocheck.append([c[0]+dir[0],c[1]+dir[1]-1])
                            tocheck.append([c[0]+dir[0],c[1]+dir[1]])
                            tocheck.append([c[0]+dir[0],c[1]+dir[1]-1])
                            # print (new_tocheck)
                    # print ("after c is all checked",new_tocheck)
                # print (flag)
                # print (new_tocheck)
                if new_tocheck==[]:
                    flag="go go go"
            # print (flag)
            if flag == "go go go" and flagg!= '#':
                # print ("to move",tocheck,position,new_position)
                new_warehouse = []
                for x in range(len(wide_warehouse)):
                    row = ""
                    for y in range(len(wide_warehouse[x])):
                        if [x-dir[0],y-dir[1]] in tocheck:
                            # x=3,7
                            # 4,7 is in the list
                            # dir = -1,0
                            # so 3,7 needs to receive 
                            row+=wide_warehouse[x-dir[0]][y-dir[1]]
                        elif [x-dir[0],y-dir[1]] ==new_position:
                            row+="@"    
                        elif [x,y] in tocheck:
                            row+="."
                        elif [x,y]==position:
                            row+="."
                        # elif [x,y]==new_position:
                        #     row+="@"    
                        else:
                            row+=wide_warehouse[x][y]
                    new_warehouse.append(row)
                
                wide_warehouse=new_warehouse
                wide_warehouse[new_position[0]] = wide_warehouse[new_position[0]][:new_position[1]]+"@"+wide_warehouse[new_position[0]][new_position[1]+1:]
                position = new_position
for x in wide_warehouse:
    print(x)
result = 0
for x in range(len(wide_warehouse)): 
    for y in range(len(wide_warehouse[x])):
        if wide_warehouse[x][y]=="[":
            result+=100*x+y
print ("part 2",result)