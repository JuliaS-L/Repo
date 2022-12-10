import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
print ("2022-10")
f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()
cycles = []
sprite = []
row = []
c=1
for x in range(len(input)):
    if input[x] == "noop":
        cycles.append(c)
    else:
        cycles.append(c)
        cycles.append(c+int(input[x].split(' ')[1]))
        c+=int(input[x].split(' ')[1])
for x in range(40):
    sprite.append(x)
    row.append(1)
print (cycles[18]*20+
       cycles[58]*60+
       cycles[98]*100+
       cycles[138]*140+
       cycles[178]*180+
       cycles[218]*220) #9860 is too low # not 13940

# x in cycles is howing the middle of 3 wide position
cycles.insert(0,1)

df = pd.DataFrame (sprite, columns = ['input'])
# df['row'] = 1
df2 = pd.DataFrame (sprite, columns = ['input'])
# df2['row'] = 2
df = df.append(df2)
df2 = pd.DataFrame (sprite, columns = ['input'])
# df2['row'] = 3
df = df.append(df2)
df2 = pd.DataFrame (sprite, columns = ['input'])
# df2['row'] = 4
df = df.append(df2)
df2 = pd.DataFrame (sprite, columns = ['input'])
# df2['row'] = 5
df = df.append(df2)
df2 = pd.DataFrame (sprite, columns = ['input'])
# df2['row'] = 6
df = df.append(df2)
# print (len(df),len(cycles))
df['position'] = cycles[:-1]
# df['draw']=0
print (df.head(10))
df['draw'] = np.where(((df['position'] >= df['input']-1)&(df['position'] <= df['input']+1)), '.',' ' )
drawing = df['draw'].values.tolist()
drawing = ''.join(drawing)
# print (drawing)
print (drawing[:40])
print (drawing[40:80])
print (drawing[80:120])
print (drawing[120:160])
print (drawing[160:200])
print (drawing[200:240])
