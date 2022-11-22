#Store SOP terms in list
str=input('Enter expression ')
#space
str.strip()
termslist=str.split('+')

#Count number of variables
termlen = len(termslist[0])
comma = termslist[0].count("'")
var = termlen-comma

#Convert literal expression to binary
def convertbinary(term):
    binary = []
    term = term.strip()
    count = 0
    for literal in term:
        if literal == "'":
            count = count +1
            continue
        if count < len(term)-1 and term [count + 1] == "'":
            binary.append('0')
            count=count+1
        else:
            binary.append('1')
            count = count +1
    count1=0
    for digit in binary:
        digit = int(digit)
        binary[count1]=digit
        count1+=1
    return binary

#List of all terms converted to binary
binarylist=[]
for term in termslist:
    binarylist.append(convertbinary(term))

#Binary to decimal
def convertdecimal(binary):
    decimal =0
    count=0
    for bit in binary:
        decimal = decimal + bit*(2**(len(binary)-count-1))
        count+=1
    return decimal

#List of all terms converted to decimal
decimallist=[]
for binary in binarylist:
    decimallist.append(convertdecimal(binary))

#Define kmap
kmap=[['0','0','0','0'],['0','0','0','0']]

#Decimal to position of  1 in kmap
def position(decimal):
    lst = int(decimal/4)
    elt = decimal-4*lst
    if elt==3:
        elt=2
    elif elt==2:
        elt=3
    return (lst,elt)

#Positionlist
positionlist=[]
for decimal in decimallist:
    positionlist.append(position(decimal))
#BC HORIZONTAL, A VERTICAL
#Position to decimal
def postodec(x,y):
    if x==0:
            if y==0:
                return 0
            if y==1:
                return 1
            if y==2:
                return 3
            if y==3:
                return 2
    if x==1:
            if y==0:
                return 4
            if y==1:
                return 5
            if y==2:
                return 7
            if y==3:
                return 6

#Fill the kmap with 1s
def fillkmap(decimal,kmap):
    elt=position(decimal)[1]
    lst=position(decimal)[0]
    kmap[lst][elt]='1'
#Fill the minterms
for term in termslist:
    binary = convertbinary(term)
    decimal = convertdecimal(binary)
    fillkmap(decimal,kmap)

print(kmap[0])
print(kmap[1])
stringlist=[]
#Check group of 8
if kmap == [['1','1','1','1'],['1','1','1','1']]:
    print('1')
else:
    usedup=[]
    #Check for 1s in top row
    y=3
    while y>-1:
        if kmap[0][y]=='0':
            break
        y=y-1
        if y==-1:
            stringlist.append("A'")
            usedup.append(0)
            usedup.append(1)
            usedup.append(2)
            usedup.append(3)
            break

    #Check for 1s in bottom row
    y=3
    while y>-1:
        if kmap[1][y]=='0':
            break
        y=y-1
        if y==-1:
            stringlist.append('A')
            usedup.append(4)
            usedup.append(5)
            usedup.append(6)
            usedup.append(7)
            break

    #Other groups of 4
    for x in range(4):
        if kmap[0][x]=='1':
            if kmap[0][x-1]=='1' and kmap[1][x-1]=='1' and kmap[1][x]=='1':
                if(x==0):
                    stringlist.append("C'")
                if(x==1):
                    stringlist.append("B'")
                if(x==2):
                    stringlist.append("C")
                if(x==3):
                    stringlist.append('B')
                usedup.append(postodec(0,x-1))
                usedup.append(postodec(1,x-1))
                usedup.append(postodec(0,x))
                usedup.append(postodec(1,x))
    print('usedup=',usedup)
    print('decimallist=',decimallist)
    leftpositions=[]
    for i in decimallist:
        if i not in usedup:
            leftpositions.append(position(i))
    print('leftpositions=',leftpositions)
    #Group of 2
    def left(kmap,position):
        if(kmap[position[0]][position[1]-1]==kmap[position[0]][position[1]]):
            return 1
        return 0

        #Check if 1 above current 1
    def up(kmap,position):
            if(kmap[position[0]-1][position[1]]==kmap[position[0]][position[1]]):
                return 1
            return 0

        #Check if 1 right to the current 1
    def right(kmap,position):
            if(position[1]==3):
                if(kmap[position[0]][0]==kmap[position[0]][position[1]]):
                    return 1
                else:
                    return 0
            if(kmap[position[0]][position[1]+1]==kmap[position[0]][position[1]]):
                    return 1
            return 0

    group2list=[]
    for position in leftpositions:
        if left(kmap,position)==1 and up(kmap,position)==0 and right(kmap,position)==0:
            if position[1]!=0:
                group2list.append([postodec(position[0],position[1]),postodec(position[0],position[1]-1)])
                usedup.append(postodec(position[0],position[1]))
                usedup.append(postodec(position[0],position[1]-1))
            else:
                group2list.append([postodec(position[0],position[1]),postodec(position[0],3)])
                usedup.append(postodec(position[0],position[1]))
                usedup.append(postodec(position[0],3))

        if left(kmap,position)==0 and up(kmap,position)==0 and right(kmap,position)==1:  
            if(position[1]==3):
                 group2list.append([postodec(position[0],position[1]),postodec(position[0],0)]) 
                 usedup.append(postodec(position[0],position[1]))
                 usedup.append(postodec(position[0],0))       
            else:
                group2list.append([postodec(position[0],position[1]),postodec(position[0],position[1]+1)])
                usedup.append(postodec(position[0],position[1]))
                usedup.append(postodec(position[0],position[1]+1))
        if left(kmap,position)==0 and up(kmap,position)==1 and right(kmap,position)==0:
            group2list.append([postodec(position[0],position[1]),postodec(position[0]-1,position[1])])
            usedup.append(postodec(position[0],position[1]))
            usedup.append(postodec(position[0]-1,position[1]))
    print("usedup=",usedup)
    print("group2list=",group2list)
    for group2 in group2list:
        if group2 == [0,4] and "B'C'" not in stringlist:
            stringlist.append("B'C'")
        if group2 == [0,1] and "A'B'" not in stringlist:
            stringlist.append("A'B'")
        if group2 == [0,2] and "A'C'" not in stringlist:
            stringlist.append("A'C'")

        if group2 == [4,0] and "B'C'" not in stringlist:
            stringlist.append("B'C'")
        if group2 == [4,5] and "AB''" not in stringlist:
            stringlist.append("AB'")
        if group2 == [4,6] and "AC'" not in stringlist:
            stringlist.append("AC'")

        if group2 == [1,0] and "A'B'" not in stringlist:
            stringlist.append("A'B'")
        if group2 == [1,3] and "A'C''" not in stringlist:
            stringlist.append("A'C")
        if group2 == [1,5] and "B'C" not in stringlist:
            stringlist.append("B'C")

        if group2 == [5,4] and "AB'" not in stringlist:
            stringlist.append("AB'")
        if group2 == [5,1] and "B'C" not in stringlist:
            stringlist.append("B'C")
        if group2 == [5,7] and "AC" not in stringlist:
            stringlist.append("AC")

        if group2 == [3,1] and "A'C'" not in stringlist:
            stringlist.append("A'C'")
        if group2 == [3,2] and "A'B" not in stringlist:
            stringlist.append("A'B")
        if group2 == [3,7] and "BC" not in stringlist:
            stringlist.append("BC")

        if group2 == [7,5] and "AC" not in stringlist:
            stringlist.append("AC")
        if group2 == [7,3] and "BC" not in stringlist:
            stringlist.append("BC")
        if group2 == [7,6] and "AB" not in stringlist:
            stringlist.append("AB")
            
        if group2 == [2,3] and "A'B" not in stringlist:
            stringlist.append("A'B")
        if group2 == [2,6] and "BC'" not in stringlist:
            stringlist.append("BC'")
        if group2 == [2,0] and "A'C'" not in stringlist:
            stringlist.append("A'C'")

        if group2 == [6,7] and "AB" not in stringlist:
            stringlist.append("AB")
        if group2 == [6,4] and "AC'" not in stringlist:
            stringlist.append("AC'")
        if group2 == [6,2] and "BC'" not in stringlist:
            stringlist.append("BC'")
        
    

    leftovers=[]
    for i in decimallist:
        if i not in usedup:
            leftovers.append(i)

    for dec in leftovers:
        if dec == 0:
            stringlist.append("A'B'C'")
        if dec == 4:
            stringlist.append("AB'C'")
        if dec == 1:
            stringlist.append("A'B'C")
        if dec == 5:
            stringlist.append("AB'C")
        if dec == 3:
            stringlist.append("A'BC")
        if dec ==7:
            stringlist.append("ABC")
        if dec == 2:
            stringlist.append("A'BC'")
        if dec == 6:
            stringlist.append("ABC'")
    
    for i in stringlist:
        if i!= stringlist[-1]:
            print(i,'+')
        else:
            print(i)
    


