import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
left = []
right =[]

for x in f:
    left.append(int(x.split(" ")[0]))
    right.append(int(x.split(" ")[-1]))
left.sort()
right.sort()
#### PART 1 ####
sum=0
for x in range(len(left)):
    sum+=abs(left[x]-right[x])
print (sum)


#### PART 2 ####
ssum=0
for x in range(len(left)):
    ssum+=left[x]*right.count(left[x])
print (ssum)
