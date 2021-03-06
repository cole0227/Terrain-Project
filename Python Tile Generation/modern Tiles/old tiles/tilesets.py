# This file takes tilesets and elevation data in, then it produces a map
# the array size is 32*25
#import twister3
import sprite
import random
from numpy import *

#twister3.heightmap()

#adding rocks:
# if the current tile is grass, and all the 4 tiles above and to the left of this one are grass
# then make this one

reader = sprite.SpriteSheetReader("tiles.png", 16)
#
# SMARTER WAY!
# add another dimension to deal with each side individually, and record this both here,
# and add a method for quickly getting this info given tile coords in mymap.
#
# the first number in the quad is for the top, then right, then bottom, then left
#
# 1-grassy
# 2-plain dirt
# 3-top or left dirt edge
# 4-right or bottom dirt edge
# 5-dirt path
# 6-plain water
# 7-top or left plain water edge
# 8-bottom or right plain water edge
# 9-cliff top or left
# 10-cliff right or bottom
tile_bits = [
    [[1, 1, 1, 1], [1, 5, 1, 5], [5, 1, 5, 1], [5, 1, 1, 1], [0, 0, 0, 0]], 
    [[1, 3, 3, 1], [3, 2, 3, 1], [3, 4, 1, 1], [1, 1, 5, 1], [0, 0, 0, 0]], 
    [[1, 3, 2, 3], [2, 2, 2, 2], [2, 4, 1, 4], [1, 5, 1, 1], [0, 0, 0, 0]], 
    [[1, 1, 4, 3], [4, 1, 4, 2], [4, 1, 1, 4], [1, 1, 1, 5], [0, 0, 0, 0]], 

    [[1, 5, 5, 1], [5, 5, 1, 1], [4, 5, 4, 2], [5, 3, 2, 3], [0, 0, 0, 0]], 
    [[1, 1, 5, 5], [5, 1, 1, 5], [3, 2, 3, 5], [2, 4, 5, 4], [0, 0, 0, 0]], 
    [[2, 4, 4, 2], [4, 3, 2, 2], [5, 5, 5, 5], [2, 2, 2, 2], [0, 0, 0, 0]], 
    [[2, 2, 3, 4], [3, 2, 2, 3], [1, 1, 1, 1], [1, 1, 1, 1], [7, 8, 2, 2]], 

    [[6, 8, 8, 6], [8, 7, 6, 6], [7, 6, 7, 5], [5, 7, 6, 7], [6, 8, 2, 8]], 
    [[6, 6, 7, 8], [7, 6, 6, 7], [8, 5, 8, 6], [6, 8, 5, 8], [8, 2, 2, 8]], 

    [[1, 7, 7, 1], [7, 6, 7, 1], [7, 8, 1, 1], [2, 7, 7, 2], [7, 6, 7, 2]], 
    [[1, 7, 6, 7], [6, 6, 6, 6], [6, 8, 1, 8], [2, 7, 6, 7], [6, 6, 6, 6]], 
    [[1, 1, 8, 7], [8, 1, 8, 6], [8, 1, 1, 8], [2, 2, 8, 7], [8, 2, 8, 6]], 

    [[1, 9, 9, 1], [9, 1, 9, 1], [9,10, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]], 
    [[1, 9, 1, 9], [1,10, 1,10], [1,10, 1,10], [1, 9, 8, 1], [8, 8, 1, 1]], 
    [[1, 1, 8, 9], [8, 1, 8, 1], [8,10, 1, 1], [1, 1, 9, 9], [9, 1, 1, 8]]
    ]

def tile_index(index):
    index%=16*5
    loc=[index%16,index/16]

size = 8
count=0
mymap = zeros((2,size,size))
occupied = zeros((size,size))

def check_left(x,y):
    #print tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]
    if(tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]==0):
        print 
        return False
    if(y<=0 or
       tile_bits[int(mymap[0][x][y-1])][int(mymap[1][x][y-1])][1]==
       tile_bits[int(mymap[0][x][y  ])][int(mymap[1][x][y  ])][3]):
        return True
    return False

def check_right(x,y):
    #print tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]
    if(tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]==0):
        return False
    if(y>=size-1 or
       tile_bits[int(mymap[0][x][y+1])][int(mymap[1][x][y+1])][3]==
       tile_bits[int(mymap[0][x][y  ])][int(mymap[1][x][y  ])][1]):
        return True
    return False

def check_top(x,y):
    #print tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]
    if(tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]==0):
        return False
    if(x<=0 or
       tile_bits[int(mymap[0][x-1][y])][int(mymap[1][x-1][y])][2]==
       tile_bits[int(mymap[0][x  ][y])][int(mymap[1][x  ][y])][0]):
        return True
    return False

def check_bottom(x,y):
    #print tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]
    if(tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]==0):
        return False
    if(x>=size-1 or
       tile_bits[int(mymap[0][x+1][y])][int(mymap[1][x+1][y])][0]==
       tile_bits[int(mymap[0][x  ][y])][int(mymap[1][x  ][y])][2]):
        return True
    return False

def sprites_verysimple():
    writer = sprite.SpriteSheetWriter(16, 32)
    tile1 = reader.getTile(2, 1)
    writer.addImage(tile1)
    writer.addImage(tile1)
    writer.addImage(tile1)
    writer.addImage(tile1)
    writer.save('zzz.png')

def sprites_random():
    mymap = zeros((2,size,size))
    for x in range(0,size):
        for y in range(0,size):
            mymap[0][x][y] = random.randint(0,8)
            mymap[1][x][y] = random.randint(0,7)    
    writer = sprite.SpriteSheetWriter(16, size*16)
    for x in range(0,size):
        for y in range(0,size):
            writer.addImage(reader.getTile(int(mymap[0][x][y]),int(mymap[1][x][y])))
    writer.save('zzz.png')

def sprites_random2():
    anint=0
    for x in range(0,size):
        for y in range(0,size):
            thistile=anint
            anint-=1
            while True:
                anint+=1
                if(anint%100000==0):
                    print 'Run count passing',anint
                mymap[0][x][y] = random.randint(0,13)
                mymap[1][x][y] = random.randint(0,4)
                if(check_left(x,y) and check_top(x,y)):
                    break
                if(anint-thistile>200):
                    y=y-2
                    break
    writer = sprite.SpriteSheetWriter(16, size*16)
    for x in range(0,size):
        for y in range(0,size):
            writer.addImage(reader.getTile(int(mymap[0][x][y]),int(mymap[1][x][y])))
    writer.save('zzv.png')
    print 'Inner loop ran ',anint,'extra times'

def fillatile(x,y):
    mymap[0][x][y] = random.randint(0,13)
    mymap[1][x][y] = random.randint(0,5)
    if( tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]==0):
        fillatile(x,y)


def spot_clean(x1,y1):
    #print 'Spot Clean Running at ',x1,',',y1
    for x in range(x1-1,x1):
        for y in range(y1-1,y1):
            mymap[0][x][y]=1
            mymap[1][x][y]=11
    for x in range(x1-1,x1):
        for y in range(y1-1,y1):
            anint=0
            if(x>0 and x<size and y>0 and y<size):
                while True:
                    anint+=1
                    fillatile(x,y)
                    if(x==x1 and check_left(x,y) and check_bottom(x,y) and check_right(x,y)):
                        break
                    if(y==y1 and check_right(x,y) and check_top(x,y) and check_bottom(x,y)):
                        break
                    if(check_left(x,y) and check_top(x,y) and x!=x1 and y!=y1):
                        #print 'Spot:',anint
                        break
                    if(anint>200):
                        y=y1-3
                        x=x1-3
                        #print 'too many spots'
                        break


def sprites_random3():
    numruns=0
    thistile=0
    for x in range(0,size):
        for y in range(0,size):
            thistile=numruns
            while True:
                numruns+=1
                if(numruns%100000==0):
                    print 'Run count passing',numruns
                fillatile(x,y)
                if(check_left(x,y) and check_top(x,y) and tile_bits[int(mymap[0][x][y])][int(mymap[1][x][y])][0]!=0):
                    break
                if(numruns-thistile>400):
                    y=y-2
                    break
    print 'Inner loop ran ',numruns,'times'

    #the naive solution worked better

    #for x in range(0,size):
    #    for y in range(0,size):
    #        if(not(check_left(x,y))):
    #           occupied[x][y]+=2
    #        if(not(check_right(x,y))):
    #           occupied[x][y]+=2
    #        if(not(check_top(x,y))):
    #           occupied[x][y]+=2
    #        if(not(check_bottom(x,y))):
    #           occupied[x][y]+=2

    #for x in range(1,size-1):
    #    for y in range(1,size-1):
    #        if(occupied[x][y]>5):
    #            spot_clean(x,y)
    
    writer = sprite.SpriteSheetWriter(16, size*16)
    for x in range(0,size):
        for y in range(0,size):
            writer.addImage(reader.getTile(int(mymap[0][x][y]),int(mymap[1][x][y])))
    writer.save('zzv.png')


#random.seed(2)
sprites_random3()
#old = 0
#new = 0
#oldsum=sum(occupied)
#for x in range(0,size):
#    for y in range(0,size):
#        if(occupied[x][y]!=0):
#            old+=1
#        if(not(check_left(x,y) and check_right(x,y) and check_top(x,y) and check_bottom(x,y))):
#            new+=1
#            occupied[x][y]=0
#            if(not(check_left(x,y))):
#               occupied[x][y]+=2
#            if(not(check_right(x,y))):
#               occupied[x][y]+=2
#            if(not(check_top(x,y))):
#               occupied[x][y]+=2
#            if(not(check_bottom(x,y))):
#               occupied[x][y]+=2
#newsum=sum(occupied)
#print occupied
#print new,'<',newsum,'> NEW VS OLD',old,'<',oldsum,'>'
