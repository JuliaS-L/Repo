import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
print ("2022-07")
f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()

# for every row.
# if cd / then full path = "/"
# if cd .. then take away the rightmost part of the path
# if cd  then append this to the path

files = {} # folder, file size
path = ""
for x in input:
    if x=='cd /':
        path='/'
    elif x=='$ cd ..':
        path = path[:path.rfind("_")]
    elif x[:4]=='$ cd':
        path = path+"_"+x[5:]
        files[path] = 0
    elif x[:1]=="$":
        pass
    elif x[:3]=="dir":
        pass
    else:
        if not path in files:
            files[path] = int(x.split(' ')[0])
        else:
            files[path] += int(x.split(' ')[0])


empty = {'path':[],'size':[]}
files_df = pd.DataFrame(empty)
for x in files.keys(): # keys is the folder = x folders[x] is the parent
    new_row = {'path': x, 'size': int(files[x])}
    files_df = files_df.append(new_row, ignore_index=True)
files_df['full_size'] = files_df['size']
# print (files_df.head())


for x in range(len(files_df)):
    for y in range(len(files_df)):
        if files_df['path'][y]==files_df['path'][x]:
            pass
        elif files_df['path'][y].find(files_df['path'][x])>-1:
            files_df.at[x, 'full_size'] += files_df['size'][y]

print ('#### PART 1 ####')
print (files_df[files_df['full_size']<= 100000]['full_size'].sum())
print ('#### PART 2 ####')
free_space=70000000-int(files_df[files_df['path']=='_/']['full_size'])
needed_space=30000000-free_space
print ( files_df[files_df['full_size']>= needed_space]['full_size'].min())
