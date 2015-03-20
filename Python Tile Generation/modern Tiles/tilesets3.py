# This file takes tilesets and elevation data in, then it produces a map
# the array size is 32*25
#import twister3
import sprite
from functions import *
import random
from numpy import *
import scipy


#twister3.heightmap()

reader = sprite.SpriteSheetReader("tiles.png", 16)

size = 256
mymap = zeros((2,size,size))

# Occupied Map details:
# 
# 0 = unoccupied space
# 1-99 = normal ground level
# 100-199 = water-based 
# 200-299 = cliff level 1
# 300-399 = cliff level 2
# ...
# 1 = dirt
# 2 = dirt path
# 3 = little trees
# 
occupied = zeros((size,size))

def rectangle(x1,y1,dx,dy,value):
    for x in range( x1, x1 + dx ):
        for y in range( y1, y1 + dy ):
            if( value != 300 and not (occupied[x][y] == 0 or occupied[x][y] == value) ):
                return 1
    for x in range( x1, x1 + dx ):
        for y in range( y1, y1 + dy ):
            occupied[x][y] = value
    return 0
            
def drop(x,y,mat):
    if( mat % 100 == 2 ):
        if(random.rand() > 0.90):
            Tree_Pine( x, y, 2 )
    if( mat % 100 == 3 ):
        if(random.rand() > 0.8):
            mymap[0][x][y] = 7
            mymap[1][x][y] = 2
    elif( mat % 100 == 1 ):
        if(occupied[x-1][y]!=mat and occupied[x][y-1]!=mat):
            mymap[0][x][y] = 1
            mymap[1][x][y] = 0
        elif(occupied[x-1][y]!=mat and occupied[x][y+1]!=mat):
            mymap[0][x][y] = 3
            mymap[1][x][y] = 0
        elif(occupied[x+1][y]!=mat and occupied[x][y+1]!=mat):
            mymap[0][x][y] = 3
            mymap[1][x][y] = 2
        elif(occupied[x+1][y]!=mat and occupied[x][y-1]!=mat):
            mymap[0][x][y] = 1
            mymap[1][x][y] = 2
        elif(occupied[x-1][y]!=mat):
            mymap[0][x][y] = 2
            mymap[1][x][y] = 0
        elif(occupied[x+1][y]!=mat):
            mymap[0][x][y] = 2
            mymap[1][x][y] = 2
        elif(occupied[x][y-1]!=mat):
            mymap[0][x][y] = 1
            mymap[1][x][y] = 1
        elif(occupied[x][y+1]!=mat):
            mymap[0][x][y] = 3
            mymap[1][x][y] = 1
        elif(occupied[x-1][y-1]!=mat):
            mymap[0][x][y] = 7
            mymap[1][x][y] = 1
        elif(occupied[x-1][y+1]!=mat):
            mymap[0][x][y] = 6
            mymap[1][x][y] = 1
        elif(occupied[x+1][y+1]!=mat):
            mymap[0][x][y] = 6
            mymap[1][x][y] = 0
        elif(occupied[x+1][y-1]!=mat):
            mymap[0][x][y] = 7
            mymap[1][x][y] = 0
        else:
            mymap[0][x][y] = 2
            mymap[1][x][y] = 1
            if(random.rand() > 0.98):
                Tree_Palm(x,y)
            elif(random.rand() > 0.95):
                mymap[0][x][y] = 6
                mymap[1][x][y] = 3
    elif( mat == 100 ):
        occupied[x][y]=120
        if(occupied[x-1][y]!=mat and occupied[x][y-1]!=mat and occupied[x-1][y]!=mat+20 and occupied[x][y-1]!=mat+20):
            mymap[0][x][y] = 10
            mymap[1][x][y] = 0
        elif(occupied[x-1][y]!=mat and occupied[x][y+1]!=mat and occupied[x-1][y]!=mat+20 and occupied[x][y+1]!=mat+20):
            mymap[0][x][y] = 11
            mymap[1][x][y] = 0
        elif(occupied[x+1][y]!=mat and occupied[x][y+1]!=mat and occupied[x+1][y]!=mat+20 and occupied[x][y+1]!=mat+20):
            mymap[0][x][y] = 11
            mymap[1][x][y] = 1
        elif(occupied[x+1][y]!=mat and occupied[x][y-1]!=mat and occupied[x+1][y]!=mat+20 and occupied[x][y-1]!=mat+20):
            mymap[0][x][y] = 10
            mymap[1][x][y] = 1
        elif(occupied[x-1][y]!=mat and occupied[x-1][y]!=mat+20):
            mymap[0][x][y] = 8
            mymap[1][x][y] = 3
        elif(occupied[x+1][y]!=mat and occupied[x+1][y]!=mat+20):
            mymap[0][x][y] = 9
            mymap[1][x][y] = 3
        elif(occupied[x][y-1]!=mat and occupied[x][y-1]!=mat+20):
            mymap[0][x][y] = 8
            mymap[1][x][y] = 2
        elif(occupied[x][y+1]!=mat and occupied[x][y+1]!=mat+20):
            mymap[0][x][y] = 9
            mymap[1][x][y] = 2
        elif(occupied[x-1][y-1]!=mat and occupied[x-1][y-1]!=mat+20):
            mymap[0][x][y] = 9
            mymap[1][x][y] = 1
        elif(occupied[x-1][y+1]!=mat and occupied[x-1][y+1]!=mat+20):
            mymap[0][x][y] = 8
            mymap[1][x][y] = 1
        elif(occupied[x+1][y+1]!=mat and occupied[x+1][y+1]!=mat+20):
            mymap[0][x][y] = 8
            mymap[1][x][y] = 0
        elif(occupied[x+1][y-1]!=mat and occupied[x+1][y-1]!=mat+20):
            mymap[0][x][y] = 9
            mymap[1][x][y] = 0
        else:
            occupied[x][y] = 100
            if(random.rand() > 0.965):
                mymap[0][x][y] = 12
                mymap[1][x][y] = 1
            else:
                mymap[0][x][y] = 12
                mymap[1][x][y] = 0
    elif( mat == 200 ):
        if(occupied[x-1][y]<mat and occupied[x][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 0
        elif(occupied[x-1][y]<mat and occupied[x][y+1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 0
        elif(occupied[x+1][y]<mat and occupied[x][y+1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 2
        elif(occupied[x+1][y]<mat and occupied[x][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 2
        elif(occupied[x-1][y]<mat):
            mymap[0][x][y] = 14
            mymap[1][x][y] = 0
        elif(occupied[x+1][y]<mat):
            if(random.rand() > 0.95 and occupied[x+1][y]<100):
                mymap[0][x][y] = 14
                mymap[1][x][y] = 1
            elif(random.rand() > 0.9 and occupied[x+1][y]<100):
                mymap[0][x][y] = 12
                mymap[1][x][y] = 2
            else:
                mymap[0][x][y] = 14
                mymap[1][x][y] = 2
        elif(occupied[x][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 1
        elif(occupied[x][y+1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 1
        elif(occupied[x+1][y+1]<mat):
            mymap[0][x][y] = 14
            mymap[1][x][y] = 3
        elif(occupied[x+1][y-1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 3
        elif(occupied[x-1][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 3
        elif(occupied[x-1][y+1]<mat):
            mymap[0][x][y] = 12
            mymap[1][x][y] = 3
        else:
            if(random.rand() > 0.95):
                Tree_Pine( x, y, 200 )
            elif(random.rand() > 0.85):
                mymap[0][x][y] = 7
                mymap[1][x][y] = 2
            else:
                mymap[0][x][y] = 0
                mymap[1][x][y] = 0
    elif( mat == 300 ):
        if(occupied[x-1][y]<mat and occupied[x][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 0
        elif(occupied[x-1][y]<mat and occupied[x][y+1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 0
        elif(occupied[x+1][y]<mat and occupied[x][y+1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 2
        elif(occupied[x+1][y]<mat and occupied[x][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 2
        elif(occupied[x-1][y]<mat):
            mymap[0][x][y] = 14
            mymap[1][x][y] = 0
        elif(occupied[x+1][y]<mat):
            if(random.rand() > 0.6 and occupied[x+1][y] < 225):
                mymap[0][x][y] = 14
                mymap[1][x][y] = 1
            else:
                mymap[0][x][y] = 14
                mymap[1][x][y] = 2
        elif(occupied[x][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 1
        elif(occupied[x][y+1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 1
        elif(occupied[x+1][y+1]<mat):
            mymap[0][x][y] = 14
            mymap[1][x][y] = 3
        elif(occupied[x+1][y-1]<mat):
            mymap[0][x][y] = 15
            mymap[1][x][y] = 3
        elif(occupied[x-1][y-1]<mat):
            mymap[0][x][y] = 13
            mymap[1][x][y] = 3
        elif(occupied[x-1][y+1]<mat):
            mymap[0][x][y] = 12
            mymap[1][x][y] = 3
        else:
            if(random.rand() > 0.9):
                mymap[0][x][y] = 7
                mymap[1][x][y] = 3
            else:
                mymap[0][x][y] = 0
                mymap[1][x][y] = 0
                

def Tree_Pine( x1, y1, mat ):

    test = 1
    for x in range( x1 - 2, x1 + 1 ):

        for y in range( y1 - 1, y1 + 1 ):
            #print x,y
            if( mymap[0][x][y] != 0 or mymap[1][x][y] != 0 or occupied[x][y] != mat ):

                test = 0
                #print mymap[0][x][y], ',', mymap[1][x][y], ',', occupied[x][y]

    if( test == 1 ):
        #print 'Success:',mymap[0][x][y], ',', mymap[1][x][y], ',', occupied[x][y]
        mymap[0][x1-2][y1-1] = 0
        mymap[1][x1-2][y1-1] = 4
        occupied[x1-2][y1-1] = 25 + mat
        mymap[0][x1-1][y1-1] = 0
        mymap[1][x1-1][y1-1] = 5
        occupied[x1-1][y1-1] = 25 + mat
        mymap[0][x1  ][y1-1] = 0
        mymap[1][x1  ][y1-1] = 6
        occupied[x1  ][y1-1] = 25 + mat
        mymap[0][x1-2][y1  ] = 1
        mymap[1][x1-2][y1  ] = 4
        occupied[x1-2][y1  ] = 25 + mat
        mymap[0][x1-1][y1  ] = 1
        mymap[1][x1-1][y1  ] = 5
        occupied[x1-1][y1  ] = 25 + mat
        mymap[0][x1  ][y1  ] = 1
        mymap[1][x1  ][y1  ] = 6
        occupied[x1  ][y1  ] = 25 + mat

def Tree_Palm( x1, y1 ):

    test = 1
    for x in range( x1 - 2, x1 + 1 ):

        for y in range( y1 - 1, y1 + 1 ):
        
            #print mymap[0][x][y], ',', mymap[1][x][y], ',', occupied[x][y]
            if( mymap[0][x][y] != 2 or mymap[1][x][y] != 1 or occupied[x][y] != 1 ):

                #print 'fail'
                test = 0
                #break

    if( test == 1 ):
        #print 'Success:',mymap[0][x1][y1], ',', mymap[1][x1][y1], ',', occupied[x1][y1]
        mymap[0][x1-2][y1-1] = 2
        mymap[1][x1-2][y1-1] = 4
        mymap[0][x1-1][y1-1] = 2
        mymap[1][x1-1][y1-1] = 5
        mymap[0][x1  ][y1-1] = 2
        mymap[1][x1  ][y1-1] = 6
        mymap[0][x1-2][y1  ] = 3
        mymap[1][x1-2][y1  ] = 4
        mymap[0][x1-1][y1  ] = 3
        mymap[1][x1-1][y1  ] = 5
        mymap[0][x1  ][y1  ] = 3
        mymap[1][x1  ][y1  ] = 6

def polish(x,y):

    if(occupied[x][y]==120):
        if(occupied[x-1][y]==120 and occupied[x+1][y]==120 and occupied[x][y-1]==120 and occupied[x][y+1]!=120 and occupied[x][y+1]!=100):
            if( occupied[x-1][y-1]!=120 and occupied[x-1][y-1]!=100 ):
                mymap[0][x][y] = 11
                mymap[1][x][y] = 0
            elif( occupied[x+1][y-1]!=120 and occupied[x+1][y-1]!=100 ):
                mymap[0][x][y] = 11
                mymap[1][x][y] = 1
        elif(occupied[x-1][y]==120 and occupied[x+1][y]==120 and occupied[x][y-1]!=120 and occupied[x][y-1]!=100 and occupied[x][y+1]==120 ):
            if( occupied[x+1][y+1]!=120 and occupied[x+1][y+1]!=100 ):
                mymap[0][x][y] = 10
                mymap[1][x][y] = 1
            elif( occupied[x-1][y+1]!=120 and occupied[x-1][y+1]!=100 ):
                mymap[0][x][y] = 10
                mymap[1][x][y] = 0
        elif(occupied[x-1][y]==120 and occupied[x+1][y]!=120 and occupied[x+1][y]!=100 and occupied[x][y-1]==120 and occupied[x][y+1]==120):
            if( occupied[x-1][y+1]!=120 and occupied[x-1][y+1]!=100 ):
                mymap[0][x][y] = 11
                mymap[1][x][y] = 1
            elif( occupied[x-1][y-1]!=120 and occupied[x-1][y-1]!=100 ):
                mymap[0][x][y] = 10
                mymap[1][x][y] = 1
        elif(occupied[x-1][y]!=120 and occupied[x-1][y]!=100 and occupied[x+1][y]==120 and occupied[x][y-1]==120 and occupied[x][y+1]==120 ):
            if( occupied[x+1][y-1]!=120 and occupied[x+1][y-1]!=100 ):
                mymap[0][x][y] = 10
                mymap[1][x][y] = 0
            elif( occupied[x+1][y+1]!=120 and occupied[x+1][y+1]!=100 ):
                mymap[0][x][y] = 11
                mymap[1][x][y] = 0

def main():

    #random.seed(3)
    hillsx = []
    hillsy = []
    for x in range( 0, ( size / 4 ) ** 2 ):

        large = 9
        small = 5
        
        a = random.randint(1,size-large-2)
        b = random.randint(1,size-large-2)
        c = random.randint(3,large)
        d = random.randint(3,large)
        e = rectangle(a,b,c,d,200)
        rectangle(random.randint(1,size-large-2),random.randint(1,size-large-2),random.randint(3,large),random.randint(3,large),1)
        rectangle(random.randint(1,size-large-2),random.randint(1,size-large-2),random.randint(3,large),random.randint(3,large),100)
        if (e == 0 and c > 6 and d > 6):
        
            hillsx[:0] = [a]
            hillsy[:0] = [b]
            
        if(x % 3 == 0):

            rectangle(random.randint(1,size-small-2),random.randint(1,size-small-2),random.randint(3,small),random.randint(3,small),2)

        if(x % 2 == 0):

            rectangle(random.randint(1,size-small-2),random.randint(1,size-small-2),random.randint(3,small),random.randint(3,small),3)

    print len(hillsx)
    while(len(hillsx) > 0):
        rectangle(hillsx.pop()+random.randint(1,2),hillsy.pop()+random.randint(1,2),random.randint(2,5),random.randint(2,5),300)
    
    for y in range( 1, size - 1 ):

        for x in range( 1, size - 1 ):
            
            drop(x,y,occupied[x][y])

    for y in range( 1, size - 1 ):

        for x in range( 1, size - 1 ):
            
            polish(x,y)

    scipy.misc.imsave('occupied.png', Matrix_Fromto(occupied,1,50))
    writer = sprite.SpriteSheetWriter(16, size*16)
    for x in range( 0, size):
        for y in range( 0, size):
            writer.addImage(reader.getTile(int(mymap[0][x][y]),int(mymap[1][x][y])))
    writer.save('map.png')

main()
