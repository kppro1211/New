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

#Swap a tuple
def swap(atuple):
    alist=[atuple[1],atuple[0]]
    btuple=tuple(alist)
    return btuple

#Define kmap
kmap=[['0','0','0','0'],['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]

    #Decimal to position of  1 in kmap
def position(decimal):
        lst = int(decimal/4)
        elt = decimal-4*lst
        if lst == 2:
            lst =3
        elif lst == 3:
            lst=2
        if elt==3:
            elt=2
        elif elt==2:
            elt=3
        return (lst,elt)

    #Positionlist
positionlist=[]
for decimal in decimallist:
        positionlist.append(position(decimal))

    #Fill the kmap with 1s
"""IN THE KMAP, AB IS VERTICAL AND CD IS HORIZONTAL"""
def fillkmap(decimal,kmap):
        elt=position(decimal)[1]
        lst=position(decimal)[0]
        kmap[lst][elt]='1'

    #Fill the minterms
for term in termslist:
        binary = convertbinary(term)
        decimal = convertdecimal(binary)
        fillkmap(decimal,kmap)

    #A couple of functions
    #Check if 1 left to the current 1 

def left(kmap,position):
        if(kmap[position[0]][position[1]-1]==kmap[position[0]][position[1]]):
            return 1
        return 0

    #Check if 1 below the current 1
def down(kmap,position):
        if(position[0]==3):
            if(kmap[0][position[1]]==kmap[position[0]][position[1]]):
                return 1
            else:
                return 0
        if(kmap[position[0]+1][position[1]]==kmap[position[0]][position[1]]):
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
primeimplicants=[]
def primeimplicant(kmap, positionlist):
    for position in positionlist:
        if(down(kmap,position)==0 and up(kmap,position)==0 and left(kmap,position)==0 and right(kmap,position)==0):
            primeimplicants.append(position)
    return
primeimplicant(kmap,positionlist)

#Position to decimal
def position_to_decimal(position):
    coordinates = list(swap(position))
    if coordinates[0] == 2:
        coordinates[0] = 3
    elif coordinates[0] == 3:
        coordinates[0] = 2
    if coordinates[1] == 2:
        coordinates[1] = 3
    elif coordinates[1] == 3:
        coordinates[1] = 2
    decimal = 4*coordinates[0] + coordinates[1]
    return decimal

#Decimal values of prime implicants
pidecimal=[]
for coordinate in primeimplicants:
    pidecimal.append(position_to_decimal(coordinate))

#Binary values of prime implicants
pibinary=[]
i=0
for decimal in pidecimal:
    pibinary.append(bin(decimal)[2:])
    pibinary[i]='0'*(var - len(pibinary[i]))+pibinary[i]
    i+=1

#Converting the binaries to actual expression
stringlist=[]
i=0
for binary in pibinary:
    if var == 4:
        stringlist.append('ABCD')
    if var == 3:
        stringlist.append('ABC')
    if var == 2:
        stringlist.append('AB')
    j=0
    k=0#Number of ticks
    for bit in binary:
        if bit == '0':
            stringlist[i]=stringlist[i][0:j+k+1]+"'"+stringlist[i][j+k+1:]
            print(j)
            print(stringlist[i])
            k+=1
        j+=1
    i+=1
instringlist=i+1
print(stringlist)
