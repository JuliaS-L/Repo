import pandas as pd
import numpy as np
f=open(r'2022 input.csv', "r")
input =f.read().splitlines()

df = pd.DataFrame (input, columns = ['input'])
df['input'] = df['input'].apply(lambda s: s.split(',')[0])
import time
start_time = time.time()

uniques = []
for x in range(len(df)):
    leng = int(len(df['input'][x])/2)
    for y in range(leng):
        if df['input'][x][y] in df['input'][x][leng:]:
            uniques.append(df['input'][x][y])
            break

result=0
for x in range(len(uniques)):
    if ord(uniques[x])>96:
        result+=ord(uniques[x])-96
    else:
        result+=ord(uniques[x])-38
print (result)

print("--- %s seconds Part 1 ---" % (time.time() - start_time))

print ('#### PART 2 ####')
start_time = time.time()

badges = []
for x in range(0,len(df),3):
    for y in range(len(df['input'][x])):
        if df['input'][x][y] in df['input'][x+1]:
            if df['input'][x][y] in df['input'][x+2]:
                badges.append(df['input'][x][y])
                break
print (len(badges))

result2=0
for x in range(len(badges)):
    if ord(badges[x])>96:
        result2+=ord(badges[x])-96
    else:
        result2+=ord(badges[x])-38
print (result2)


print("--- %s seconds Part 1 ---" % (time.time() - start_time))
print ("##### Refactoring #####")
start_time = time.time()

uniques = []
for x in range(len(df)):
    leng = int(len(df['input'][x])/2)
    first = set(df['input'][x][:leng])
    second = set(df['input'][x][leng:])
    uniques.append(list((first.intersection(second)))[0])
result=0
for x in range(len(uniques)):
    if ord(uniques[x])>96:
        result+=ord(uniques[x])-96
    else:
        result+=ord(uniques[x])-38
print (result)
print("--- %s seconds refactored ---" % (time.time() - start_time))

print ("##### Refactoring Part 2 #####")

start_time = time.time()
badges = []
for x in range(0,len(df),3):
    unique = set(df['input'][x]).intersection(set(df['input'][x+1]))
    badges.append(list(set(df['input'][x+2]).intersection(unique))[0])

print (len(badges))

result2=0
for x in range(len(badges)):
    if ord(badges[x])>96:
        result2+=ord(badges[x])-96
    else:
        result2+=ord(badges[x])-38
print (result2)

print("--- %s seconds refactored Part 2 ---" % (time.time() - start_time))
