import pandas as pd

pd.set_option('display.max_rows', 500)
print ("2022-09")
f=open(r'inpt_2022.txt', "r")
input =f.read().splitlines()
df = pd.DataFrame (input, columns = ['input'])
df['direction'] = df['input'].apply(lambda s: s.split(' ')[0])
df['steps'] = df['input'].apply(lambda s: int(s.split(' ')[1]))
df = df.drop(['input'], axis=1)
print (df)
postitions = ["0,0"]
Hx,Hy,Tx,Ty = 0,0,0,0
# x moves left & right
# y moves up and down
for x in range(len(input)):
    for y in range(df['steps'][x]):
        if df['direction'][x]=='L':
            Hx-=1
        elif df['direction'][x] == 'R':
            Hx+=1
        elif df['direction'][x]=='U':
            Hy+=1
        elif df['direction'][x] == 'D':
            Hy-=1
        if abs(Hx-Tx)+abs(Hy-Ty)==2:
            if df['direction'][x] == 'L':
                Tx = Hx+1
            elif df['direction'][x] == 'R':
                Tx = Hx-1
            elif df['direction'][x] == 'U':
                Ty = Hy-1
            elif df['direction'][x] == 'D':
                Ty = Hy+1
        if abs(Hx - Tx) + abs(Hy - Ty) == 3:
            if df['direction'][x] == 'L':
                Tx = Hx+1
                Ty=Hy
            elif df['direction'][x] == 'R':
                Tx = Hx-1
                Ty=Hy
            elif df['direction'][x] == 'U':
                Ty = Hy-1
                Tx=Hx
            elif df['direction'][x] == 'D':
                Ty = Hy+1
                Tx=Hx
        # print (x,y,df['direction'][x],Hx,Hy,Tx,Ty)

        if postitions.count(str(Tx)+","+str(Ty))!=1:
            postitions.append(str(Tx)+","+str(Ty))
print ('#### PART 1 ####')
print (len(postitions))


print ('#### PART 2 ####')
postitions = ["0,0"]
Hx,Hy,H1x,H1y,H2x,H2y,H3x,H3y,H4x,H4y,H5x,H5y,H6x,H6y,H7x,H7y,H8x,H8y,Tx,Ty = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
def move(X2,Y2,X1,Y1):
    if abs(X2 - X1) + abs(Y2 - Y1) == 2 and (X2==X1 or Y2==Y1):
        if X2==X1:
            Y1+=(Y2-Y1)/2
        else:
            X1+=(X2-X1)/2
    elif abs(X2 - X1) + abs(Y2 - Y1) > 2:
        if X1!=X2 and Y1!=Y2:
            sign = (X2-X1)/abs(X2-X1)
            X1+=1*sign
            sign = (Y2-Y1)/abs(Y2-Y1)
            Y1+=1*sign

    return (int(X1),int(Y1))

for x in range(len(input)):
    for y in range(df['steps'][x]):
        #### HEAD MOVING
        if df['direction'][x]=='L':
            Hx-=1
        elif df['direction'][x] == 'R':
            Hx+=1
        elif df['direction'][x]=='U':
            Hy+=1
        elif df['direction'][x] == 'D':
            Hy-=1

        H1x,H1y=move(Hx,Hy,H1x,H1y)
        H2x,H2y=move(H1x,H1y,H2x,H2y)
        H3x,H3y=move(H2x,H2y,H3x,H3y)
        H4x,H4y=move(H3x,H3y,H4x,H4y)
        H5x,H5y=move(H4x,H4y,H5x,H5y)
        H6x,H6y=move(H5x,H5y,H6x,H6y)
        H7x,H7y=move(H6x,H6y,H7x,H7y)
        H8x,H8y=move(H7x,H7y,H8x,H8y)
        Tx,Ty=move(H8x,H8y,Tx,Ty)

        if postitions.count(str(Tx)+","+str(Ty))!=1:
            postitions.append(str(Tx)+","+str(Ty))
print (len(postitions))