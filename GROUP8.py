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

#Checks if all elements in the list are the same
    def is_same(lst):
        char = lst[0]
        for i in lst:
            if i != char:
                return 0
        return 1

#Checks for group of 16, works for all 1s and all 0s
def group16(kmap,number):
    ctr = 0
    for i in (kmap):
        if is_same(i) == 1 and int(i[0]) == number:
            ctr += 1
            if ctr == 4:
                return 1
    return 0

#KMap locations of cells forming groups of 8 row-wise, works for 1s and 0s too
def group8_rows(lst,number):
    #Coordinates master is the list of groups of 8 possible
    coordinates_master = []
    kmaplocation = []
    #Checking group of 8 row wise
    for i in range(len(lst)):
        if int(lst[i][0]) == number:
            if (lst[i] == lst[i-1] and is_same(lst[i]) == 1):
                for j in range(len(lst)):
                    if i == 0:
                        kmaplocation.append((3,j))
                    else:
                        kmaplocation.append((i-1,j))
                    kmaplocation.append((i,j))
    ctr = 0
    temp = []
    for i in kmaplocation:
         if ctr == 7:
             temp.append(i)
             coordinates_master.append(temp)
             temp = []
             ctr = 0
         else:
             temp.append(i)
             ctr += 1
    return coordinates_master

def group8(kmap,number):
    """
        This function makes group of 8 in the given Kmap based on the coordinates of 1s or 0s provided as coordinates
        Number signifies what number are we grouping(SOP or POS)
        type of num must be integer.

        The function returns a list containing 2 lists
        the first list is the list of groups made row wise
        the second list is the list of groups made column wise.
   """
    #Row wise
    row_coord = group8_rows(kmap,number)

    #Column wise
    list_of_col = []
    for j in range(len(kmap)):
        temp = []
        for i in range(len(kmap)):
            temp.append(kmap[i][j])

        list_of_col.append(temp)

    col_coord = group8_rows(list_of_col,number)
    #Colcoord consists of swapped position in kmap
    return [row_coord,col_coord]

def swap(atuple):
    alist=[atuple[1],atuple[0]]
    btuple=tuple(alist)
    return btuple


if(var==4):
#   Define kmap
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
    
    #If the entire kmap has 1s then the minimised expression is 1
    stringlist=[]
    if group16(kmap,1)==1:
        stringlist=['1']

    #Handling groups of 8
    #Store row numbers of each group of 8 in tuples
    #alist is the list of rownumbers of each group of 8
    alist=[[],[],[],[]]
    groupsof8 = group8(kmap,1)
    j=0
    for rowgroup in group8(kmap,1)[0]:
        for position in rowgroup:
            if position[0] not in alist[j]:
                alist[j].append(position[0])
        j+=1
    #Store column numbers of each group of 8 in tuples
    #blist is the list of colnumbers of each group of 8
    blist=[[],[],[],[]]
    groupsof8 = group8(kmap,1)
    j=0
    for colgroup in group8(kmap,1)[1]:
        for position in colgroup:
                if position[0] not in blist[j]:
                  blist[j].append(position[0])
        j+=1
    
    #Add the expression for rowgroups to stringlist
    for pair in alist:
        if pair==[0,1]:
            stringlist.append("A'")
        elif pair==[1,2]:
            stringlist.append("B")
        elif pair==[2,3]:
            stringlist.append("A")
        elif pair==[3,0]:
            stringlist.append("B'")

    #Add the expression for colgroups to stringlist
    for pair in blist:
        if pair==[0,1]:
            stringlist.append("C'")
        elif pair==[1,2]:
            stringlist.append("D")
        elif pair==[2,3]:
            stringlist.append("C")
        elif pair==[3,0]:
            stringlist.append("D'")
    print(kmap)
    print(stringlist)

    #Locations used up in group formation
    usedup=[]
    for set in group8(kmap,1)[0]:
        for position in set:
                usedup.append(position)
    for set in group8(kmap,1)[1]:
        for position in set:
                usedup.append(swap(position))

    #Assign -1
    for position in usedup:
        kmap[position[0]][position[1]]='-1'
    print(kmap)
    
    #Group of 4
            
    
    

    
    

