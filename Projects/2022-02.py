import pandas as pd
import numpy as np
f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()

# print (input[:10])
df = pd.DataFrame (input, columns = ['input'])

df['start'] = df['input'].apply(lambda s: s.split(' ')[0])
df['end'] = df['input'].apply(lambda s: s.split(' ')[1])
df['end'] = np.where(((df['end'] == "X")), "A", df['end'] )
df['end'] = np.where(((df['end'] == "Y")), "B", df['end'] )
df['end'] = np.where(((df['end'] == "Z")), "C", df['end'] )
df['start_2'] = np.where(((df['end'] == "A")), 1, df['end'] )
df['start_2'] = np.where(((df['end'] == "B")), 2, df['start_2'] )
df['start_2'] = np.where(((df['end'] == "C")), 3, df['start_2'] )
score=df['start_2'].sum()
for x in range(len(df)):
    if df['start'][x]==df['end'][x]:
        score+=3
    elif df['start'][x]=='A':
        if df['end'][x]=='B':
            score+=6
    elif df['start'][x]=='B':
        if df['end'][x]=='C':
            score+=6
    elif df['start'][x]=='C':
        if df['end'][x]=='A':
            score+=6
print (df.head())
print (score)

# a=Rock=1=x
# b=paper=2=y
# c=scissors=3=z

print ("#### PART 2 ####")
# start changed into numbers as in a draw I will always choose that one
df['start_3'] = np.where(((df['start'] == "A")), 1, df['start'] )
df['start_3'] = np.where(((df['start'] == "B")), 2, df['start_3'] )
df['start_3'] = np.where(((df['start'] == "C")), 3, df['start_3'] )
# knowing the outcome we can sum to get the score
df['end_2'] = np.where(((df['end'] == "A")), 0, df['end'] )
df['end_2'] = np.where(((df['end'] == "B")), 3, df['end_2'] )
df['end_2'] = np.where(((df['end'] == "C")), 6, df['end_2'] )
score=df['end_2'].sum()
for x in range(len(df)):
    if df['end'][x]=='B':
        score+=df['start_3'][x]
    elif df['end'][x] == 'A': #what do we have to choose to lose
        if df['start'][x] == 'A':
            score+=3
        elif df['start'][x]=='B':
            score+=1
        else:
            score+=2
    elif df['end'][x] == 'C': #what do we have to choose to lose
        if df['start'][x] == 'A':
            score+=2
        elif df['start'][x]=='B':
            score+=3
        else:
            score+=1
print (score)


