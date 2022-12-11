import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
print ("2022-10")
f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()
holdings = []
operations = []
tests = []
throw_true = []
throw_false = []
for x in range(0,len(input),7):
    # print (input[x+1])
    holdings.append(input[x+1][18:])
    operations.append(input[x+2][23:])
    tests.append(int(input[x+3][-2:]))
    throw_true.append(int(input[x+4][-1]))
    throw_false.append(int(input[x+5][-1]))
# print('operations',operations)
actions = [0,0,0,0,0,0,0,0]
for x in range(len(holdings)):
    holdings[x]=holdings[x].split(", ")
def round():
    for x in range(len(holdings)):
        for y in range(len(holdings[x])):
            item = int(holdings[x][y])
            if operations[x][-3:]=="old":
                val = item
            else:
                val = int(operations[x][-2:])
            if operations[x][0]=="+":
                item+=val
                item=int(item/3)
            else:
                item = item*val
                item=int(item/3)
            if item%tests[x]==0:
                holdings[throw_true[x]].append(item)
            else:
                holdings[throw_false[x]].append(item)

            # print(holdings)
        actions[x]+=len(holdings[x])
        holdings[x]=[]

    return holdings
for x in range(20):
    round()
print ("#### PART 1 ####")
print (sorted(actions)[-1]*sorted(actions)[-2])


holdings = []
operations = []
tests = []
throw_true = []
throw_false = []
for x in range(0,len(input),7):
    holdings.append(input[x+1][18:])
    operations.append(input[x+2][23:])
    tests.append(int(input[x+3][-2:]))
    throw_true.append(int(input[x+4][-1]))
    throw_false.append(int(input[x+5][-1]))
prod = np.prod(tests)

actions = [0,0,0,0,0,0,0,0]
for x in range(len(holdings)):
    holdings[x]=holdings[x].split(", ")
print(holdings)
print (tests)
def new_round():
    for x in range(len(holdings)):
        for y in range(len(holdings[x])):
            item = int(holdings[x][y])
            if operations[x][-3:]=="old":
                val = item
            else:
                val = int(operations[x][-2:])
            if operations[x][0]=="+":
                item+=val
            else:
                item = item*val
            if item % tests[x]==0:
                holdings[throw_true[x]].append(item % prod)
            else:
                holdings[throw_false[x]].append(item % prod)
        actions[x]+=len(holdings[x])
        holdings[x]=[]

    return holdings


for x in range(10000):
    new_round()
print ("#### PART 2 ####")
print (sorted(actions)[-1]*sorted(actions)[-2])