import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, 'day1_input.txt'))
safecount = 0
ssafecount = 0



for x in f:
### PART 1
    list = []
    for y in x.split(" "):
        list.append(int(y))
    diff_list = []
    for z in range(len(list)-1):
        diff_list.append(list[z]-list[z+1])
    if min(diff_list)<0 and max(diff_list)<0 and min(diff_list)>-4:
        safecount+=1
    if min(diff_list)>0 and max(diff_list)>0 and max(diff_list)<4:
        safecount+=1
    
### PART 2
    list = []
    for y in x.split(" "):
        list.append(int(y))
    diff_list = []
    for z in range(len(list)-1):
        diff_list.append(list[z]-list[z+1])
    if min(diff_list)<0 and max(diff_list)<0 and min(diff_list)>-4:
        ssafecount+=1
    elif min(diff_list)>0 and max(diff_list)>0 and max(diff_list)<4:
        ssafecount+=1
    else:
        for r in range(len(list)):
            cleaned_list = list.copy()
            cleaned_list.pop(r)
            cleaned_diff_list = []
            for z in range(len(cleaned_list)-1):
                cleaned_diff_list.append(cleaned_list[z]-cleaned_list[z+1])
            if min(cleaned_diff_list)<0 and max(cleaned_diff_list)<0 and min(cleaned_diff_list)>-4:
                ssafecount+=1
                break
            if min(cleaned_diff_list)>0 and max(cleaned_diff_list)>0 and max(cleaned_diff_list)<4:
                ssafecount+=1
                break


print (safecount)
print (ssafecount) 


