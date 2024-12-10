import os
import re
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
input = ""
for x in f:
    input += x
print(input)
solution=0
start = input.find("mul(")
while start>0:
    comma = input.find(",",start)
    end = input.find(")",comma)
    if input[start+4:comma].isdigit() and input[comma+1:end].isdigit():
        solution+=int(input[start+4:comma])*int(input[comma+1:end])
    start = input.find("mul(",start+1)
# re.findall( r'mul( (^[0-9]*$) ,', input)
print (solution)


ssolution=0
nogo = input.find("don't()")
while nogo>1:
    restart = input.find("do()",nogo)
    if restart==-1:
        input= input[:nogo]
    else:
        input= input[:nogo] + input[restart+4:]
    nogo = input.find("don't()")
    # print (nogo,len(input))
print (input)

start = input.find("mul(")
while start>0:
    comma = input.find(",",start)
    end = input.find(")",comma)
    if input[start+4:comma].isdigit() and input[comma+1:end].isdigit():
        ssolution+=int(input[start+4:comma])*int(input[comma+1:end])
    start = input.find("mul(",start+1)
# re.findall( r'mul( (^[0-9]*$) ,', input)
print (ssolution)
