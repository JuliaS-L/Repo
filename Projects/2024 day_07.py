import os
import re
import itertools
import sympy
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
solution = 0

def find_all_results(input,result):
    # print (input)
    if result in [sum(s) for s in input]:
        # print ("yay found it")
        return result
    elif  max([len(i) for i in input])==1:
        # print("end of road")
        return 0
    else:
        # print ([i for i in input])
        input_new = []
        for z in [i for i in input]:
            # print("z",z)
            if len(z)>1:
                sums= z[0]+z[1]
                product= z[0]*z[1]
                z[0]=sums
                del z[1]
                z_2 = z.copy()
                z_2[0]=product
                if sum(z_2)<=result +10:
                    input_new.append(z_2)
                if sum(z)<=result +10 :
                    input_new.append(z)
                else:
                    input_new.append([0])
        # print ("now we start again")
        return find_all_results(input_new,result)
    


def find_all_results_part2(input,result):
    # print (input)
    if result in [sum(s) for s in input]:
        return result
    elif  max([len(i) for i in input])==1:
        return 0
    else:
        # print ([i for i in input])
        input_new = []
        for z in [i for i in input]:
            # print("z",z)
            if len(z)>1:
                sums= z[0]+z[1]
                product= z[0]*z[1]
                append= int(str(z[0])+str(z[1]))
                # print (append)
                z[0]=sums
                del z[1]
                z_2 = z.copy()
                z_3 = z.copy()
                z_2[0]=product
                z_3[0]=append
                if sum(z_2)<=result +10:
                    input_new.append(z_2)
                if sum(z)<=result +10 :
                    input_new.append(z)
                if sum(z_3)<=result +10 :
                    input_new.append(z_3)
                else:
                    input_new.append([0])
        # print ("now we start again")
        return find_all_results_part2(input_new,result)


solution2 = 0
for x in f: 
    results =[]
    result = int(x.split(":")[0])
    values = [int(y) for y in x.split(":")[1].strip().split()]
    results.append(values)
    solution+=find_all_results(results,result)

print (solution)    
f = open(os.path.join(__location__, 'day1_input.txt'))
for x in open(os.path.join(__location__, 'day1_input.txt')):
    results =[]
    result = int(x.split(":")[0])
    values = [int(y) for y in x.split(":")[1].strip().split()]
    results.append(values)
    partial_solution = find_all_results_part2(results,result)
    # print (partial_solution)
    solution2+=partial_solution


print (solution2)    
