import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
print ("2015 Day 5")
f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()
df = pd.DataFrame (input, columns = ['input'])
df['elf1'] = df['input'].apply(lambda s: s.split(',')[0])
df['elf2'] = df['input'].apply(lambda s: s.split(',')[1])
df['elf1_start'] = pd.to_numeric(df['elf1'].apply(lambda s: s.split('-')[0]))
df['elf1_end'] = pd.to_numeric(df['elf1'].apply(lambda s: s.split('-')[1]))
df['elf2_start'] = pd.to_numeric(df['elf2'].apply(lambda s: s.split('-')[0]))
df['elf2_end'] = pd.to_numeric(df['elf2'].apply(lambda s: s.split('-')[1]))

df = df.drop(['input','elf1','elf2'], axis=1)

df['full_overlap'] = np.where(((df['elf1_start'] <= df['elf2_start']) & (df['elf1_end'] >= df['elf2_end']))|((df['elf2_start'] <= df['elf1_start']) & (df['elf2_end'] >= df['elf1_end'])) , 1, 0)
print (df['full_overlap'].sum())
#526

df['overlap'] = np.where((((df['elf1_start'] <= df['elf2_end']) & (df['elf1_start'] >= df['elf2_start']))|((df['elf1_end'] <= df['elf2_end']) & (df['elf1_end'] >= df['elf2_start']))|((df['elf2_start'] <= df['elf1_end']) & (df['elf2_start'] >= df['elf1_start']))|((df['elf2_end'] <= df['elf1_end']) & (df['elf2_end'] >= df['elf1_start']))) , 1, 0)
print (df['overlap'].sum())


#886

