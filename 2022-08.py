import pandas as pd

pd.set_option('display.max_rows', 500)
print ("2022-08")
f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()

import itertools
points = list(itertools.permutations(range(99), r=2))
for x in range (99):
    points.append([x,x])
grid = pd.DataFrame (points, columns = ['x','y'])
grid['height'] = 0
grid['visibility']=0
grid['score']=0
grid['up']=0
grid['down']=0
grid['left']=0
grid['right']=0


for x in range(len(grid)):
    grid.at[x, 'height'] = input[grid['x'][x]][grid['y'][x]]
#### Part 1 commented out to save processing time ####
for x in range(len(grid)):
    if (grid['x'][x]==0) or (grid['y'][x]==0) or (grid['x'][x]==98) or (grid['y'][x]==98):
        grid['visibility'][x]=1
    else:
        height = grid['height'][x]
        up = grid[(grid['x']==grid['x'][x])&(grid['y']<grid['y'][x])]['height'].max()
        down = grid[(grid['x']==grid['x'][x])&(grid['y']>grid['y'][x])]['height'].max()
        left = grid[(grid['x']<grid['x'][x])&(grid['y']==grid['y'][x])]['height'].max()
        right = grid[(grid['x']>grid['x'][x])&(grid['y']==grid['y'][x])]['height'].max()
        if height>up or height > down or height > left or height>right:
            grid['visibility'][x] = 1
print ('#### PART 1 ####')
print (grid['visibility'].sum())
print ('#### PART 2 ####')
final_score=0

for x in range(len(grid)):
    if (grid['y'][x] ==0) or (grid['y'][x] ==98) or (grid['x'][x] ==98) or (grid['x'][x] ==0):
        score=0
    else:
        if len(grid[(grid['x']<grid['x'][x])&(grid['y']==grid['y'][x])&(grid['height']>=grid['height'][x])])==0:
            grid['up'][x]=grid['x'][x]
        else:
            grid['up'][x] = abs(grid['x'][x]-grid[(grid['x']<grid['x'][x])&(grid['y']==grid['y'][x])&(grid['height']>=grid['height'][x])]['x'].max())

        if len(grid[(grid['x']>grid['x'][x])&(grid['y']==grid['y'][x])&(grid['height']>=grid['height'][x])])==0:
            grid['down'][x]=98-grid['x'][x]
        else:
            grid['down'][x] = abs(grid[(grid['x']>grid['x'][x])&(grid['y']==grid['y'][x])&(grid['height']>=grid['height'][x])]['x'].min()-grid['x'][x])

        if len(grid[(grid['y']<grid['y'][x])&(grid['height']>=grid['height'][x])&(grid['x']==grid['x'][x])])==0:
            grid['left'][x] = grid['y'][x]
        else:
            grid['left'][x] = abs(grid['y'][x]-grid[(grid['y']<grid['y'][x])&(grid['height']>=grid['height'][x])&(grid['x']==grid['x'][x])]['y'].max())

        if len(grid[(grid['y']>grid['y'][x])&(grid['height']>=grid['height'][x])&(grid['x']==grid['x'][x])])==0:
            grid['right'][x] = 98-grid['y'][x]
        else:
            grid['right'][x]= abs(grid[(grid['y']>grid['y'][x])&(grid['height']>=grid['height'][x])&(grid['x']==grid['x'][x])]['y'].min()-grid['y'][x])
        score=grid['up'][x]*grid['down'][x]*grid['left'][x]*grid['right'][x]
    grid['score'][x] = score
print (grid['score'].max())