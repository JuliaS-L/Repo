f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()

print (input[:10])
food =0
snack =0
for x in range(1,len(input)):
    if input[x]=='':
        if food<snack:
            food=snack
        snack=0
    else:
        snack += int(input [x])

print (food)

print ("### PART 2 ####")
food=[]
snack =0
for x in range(1,len(input)):
    if input[x]=='':
        food.append(snack)
        snack=0
    else:
        snack += int(input [x])

print (sum(sorted(food)[-3:]))