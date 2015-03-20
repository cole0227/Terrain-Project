import time
import random

from numpy import *
import scipy

import sprite
from functions import *


wall = time.clock()
wall2 = time.clock()

tileSize = 20
reader = sprite.SpriteSheetReader("BasicTiles.png", tileSize)

regionMap = Gaussian_Blur(Matrix_Double(Matrix_Double(Matrix_Double(Matrix_Crop(load('.map_region.npy'), -8, 10)))),3)
scipy.misc.imsave( 'blurryregion.png', regionMap )
stockRegion = load('.map_region.npy')
#print Stats_Percentile(stockRegion)
varMap = load( '.map_var.npy' )
vegMap = Gaussian_Blur(Matrix_Double(Matrix_Double(Matrix_Double(load('.map_veg.npy')))),5)
heightMap = load('.map_complete.npy')
Smallsize = int( varMap.size ** ( 0.5 ) )
size = int( heightMap.size ** ( 0.5 ) )
ratio = Smallsize / size

typeMap = zeros((size,size))
tileMap = zeros((size-1,size-1,2))
realTileMap = zeros((size-1,size-1,2))+5
realTileMap2 = zeros((size-1,size-1,2))+5
edgeMap = zeros((size,size))


#terrain types:
# -20 deep ocean
# -10 less deep ocean
# -1 shallow ocean
# 0 grass
# 10 mud
# 20 sandy beach
# 21 swampy land
# 30 forest
# 31 jungle
# 40 mountains
# 41 lava


def Edge(tileMap2, tileType = 10,tileOffset = 3):

    for x in range(size-1):
        
        for y in range(size-1):

            if(typeMap[x][y] == tileType):#top left

                edgeMap[x][y]=1
                tileMap2[x][y][0]=2
                tileMap2[x][y][1]=2+tileOffset

                if(typeMap[x+1][y] == tileType):#both left
                    if(typeMap[x][y+1] == tileType):#all but bottom right

                        if(typeMap[x+1][y+1] == tileType):#all 4

                            tileMap2[x][y][0]=1
                            tileMap2[x][y][1]=1+tileOffset
                            edgeMap[x][y]=0

                        else:

                            tileMap2[x][y][0]=4
                            tileMap2[x][y][1]=1+tileOffset

                    elif(typeMap[x+1][y+1] == tileType):#all but top right

                        tileMap2[x][y][0]=4
                        tileMap2[x][y][1]=0+tileOffset

                    else:#both left only

                        tileMap2[x][y][0]=2
                        tileMap2[x][y][1]=1+tileOffset
                        
                else:
                    if(typeMap[x][y+1] == tileType):#both top, no bottom left
                        if(typeMap[x+1][y+1] == tileType): # all but bottom left

                            tileMap2[x][y][0]=3
                            tileMap2[x][y][1]=1+tileOffset

                        else: # all top
                            tileMap2[x][y][0]=1
                            tileMap2[x][y][1]=2+tileOffset

                    else:
                        if(typeMap[x+1][y+1] == tileType):#cross only

                            tileMap2[x][y][0]=4
                            tileMap2[x][y][1]=2+tileOffset

            elif(typeMap[x+1][y] == tileType):#bottom left, no top left
                edgeMap[x][y]=1
                if(typeMap[x][y+1] == tileType):#bottom left and top right, no top left
                    if(typeMap[x+1][y+1] == tileType):#all but top left

                        tileMap2[x][y][0]=3
                        tileMap2[x][y][1]=0+tileOffset
                        
                    else:#bottom left and top right only

                        tileMap2[x][y][0]=3
                        tileMap2[x][y][1]=2+tileOffset

                else:#bottom left, no top

                    if(typeMap[x+1][y+1] == tileType):#bottom only

                        tileMap2[x][y][0]=1
                        tileMap2[x][y][1]=0+tileOffset
                        
                    else:#bottom left only

                        tileMap2[x][y][0]=2
                        tileMap2[x][y][1]=0+tileOffset

            elif(typeMap[x][y+1] == tileType):#top right, no left
                edgeMap[x][y]=1

                if(typeMap[x+1][y+1] == tileType):# right only

                    tileMap2[x][y][0]=0
                    tileMap2[x][y][1]=1+tileOffset

                else: # top right only

                    tileMap2[x][y][0]=0
                    tileMap2[x][y][1]=2+tileOffset

            elif(typeMap[x+1][y+1] == tileType):# bottom right only
                edgeMap[x][y]=1

                tileMap2[x][y][0]=0
                tileMap2[x][y][1]=0+tileOffset


    return 0


def writeLayer(aRealTileMap,name):
    f = open(name, 'w')
    for x in range(size-1):
        a = ""
        #a += str(x)+" : "
        for y in range(size-1):
            a += str(int(aRealTileMap[x][y][0]+6*aRealTileMap[x][y][1]))+" , "
        
        f.write(a+"\n")
    f.close()

#Main begins here

for x in range(size):
    
    for y in range(size):

        xs = x * ratio
        ys = y * ratio
        
        if(heightMap[x][y]< 8): # water

            typeMap[x][y] = -20

        elif(heightMap[x][y]< 18):

            typeMap[x][y] = -10

        elif(heightMap[x][y]< 26):

            typeMap[x][y] = -1

        elif(heightMap[x][y] > 82): # mountains

            typeMap[x][y] = 49
            
        elif(heightMap[x][y] > 70):

            typeMap[x][y] = 42
            
        elif(heightMap[x][y] > 65 and random.rand() > 0.6):

            typeMap[x][y] = 44
            
        elif(heightMap[x][y] > 58):

            typeMap[x][y] = 45
            
        elif(heightMap[x][y] > 52):

            typeMap[x][y] = 40

        elif(vegMap[x][y] > 3.0): # woods

            typeMap[x][y] = 32

        elif(vegMap[x][y] > 2.2 and random.rand() > 0.05):

            typeMap[x][y] = 31

        elif(vegMap[x][y] > 2.05 and random.rand() > 0.5):

            typeMap[x][y] = 31

        elif(vegMap[x][y] > 1.5 and random.rand() > 0.1):

            typeMap[x][y] = 30

        elif(vegMap[x][y] > 1.45 and random.rand() > 0.5):

            typeMap[x][y] = 30

        elif(heightMap[x][y] > 47): # grass, sand and dirt

            typeMap[x][y] = 15

        elif(heightMap[x][y]> 33):

            typeMap[x][y] = 0
            
        elif(regionMap[x][y] < -0.5): 

            typeMap[x][y] = 20

        elif(regionMap[x][y] < -0.35):

            typeMap[x][y] = 21

        elif(regionMap[x][y] < -0.2 and random.rand() > 0.5):

            typeMap[x][y] = 22

        else:
            typeMap[x][y] = 10

print "Loop 1",(time.clock()-wall),'s'
wall = time.clock()

for x in range(size-1):
    
    for y in range(size-1):

        if(typeMap[x][y] == 0):
            tileMap[x][y][0]=3
            tileMap[x][y][1]=0
            
        elif(typeMap[x][y] == 10):
            tileMap[x][y][0]=1
            tileMap[x][y][1]=0
            
        elif(typeMap[x][y] == 20):
            tileMap[x][y][0]=2
            tileMap[x][y][1]=0

        elif(typeMap[x][y] == 31):
            tileMap[x][y][0]=4
            tileMap[x][y][1]=1

        elif(typeMap[x][y] == 30):
            tileMap[x][y][0]=2
            tileMap[x][y][1]=1

        elif(typeMap[x][y] == -20):
            tileMap[x][y][0]=1
            tileMap[x][y][1]=1

        elif(typeMap[x][y] == -10):
            tileMap[x][y][0]=0
            tileMap[x][y][1]=1

        elif(typeMap[x][y] == -1):
            tileMap[x][y][0]=0
            tileMap[x][y][1]=0

        elif(typeMap[x][y] == 49):
            tileMap[x][y][0]=5
            tileMap[x][y][1]=0
            
        elif(typeMap[x][y] == 42):
            tileMap[x][y][0]=3
            tileMap[x][y][1]=1
            
        elif(typeMap[x][y] == 44):
            tileMap[x][y][0]=1
            tileMap[x][y][1]=2
            
        elif(typeMap[x][y] == 45):
            tileMap[x][y][0]=0
            tileMap[x][y][1]=2
            
        elif(typeMap[x][y] == 40):
            tileMap[x][y][0]=4
            tileMap[x][y][1]=0

        elif(typeMap[x][y] == 32):
            tileMap[x][y][0]=5
            tileMap[x][y][1]=1

        elif(typeMap[x][y] == 15):
            tileMap[x][y][0]=3
            tileMap[x][y][1]=2

        elif(typeMap[x][y] == 21):
            tileMap[x][y][0]=2
            tileMap[x][y][1]=2

        elif(typeMap[x][y] == 22):
            tileMap[x][y][0]=2
            tileMap[x][y][1]=2


print "Loop 2",(time.clock()-wall),'s'
wall = time.clock()

Edge(realTileMap,10,3)
Edge(realTileMap2,30,6)
Edge(realTileMap2,20,9)
Edge(tileMap,-10,15)
Edge(tileMap,-20,12)

print "Edging",(time.clock()-wall),'s'
wall = time.clock()


writeLayer(tileMap,"0.dat")
writeLayer(realTileMap,"1.dat")
writeLayer(realTileMap2,"2.dat")
        
print "Writing .dat files",(time.clock()-wall),'s'
wall = time.clock()

writer = sprite.SpriteSheetWriter(tileSize, (size-1)*tileSize)
for x in range(size-1):
    
    for y in range(size-1):

        writer.addImage(reader.getTile(int(tileMap[x][y][0]),int(tileMap[x][y][1])))

writer.save('rough.png')
writer = 0
print "Writing 1",(time.clock()-wall),'s'
wall = time.clock()

writer2 = sprite.SpriteSheetWriter(tileSize, (size-1)*tileSize)
for x in range(size-1):
    
    for y in range(size-1):

        writer2.addImage(reader.getTile(int(realTileMap[x][y][0]),int(realTileMap[x][y][1])))

writer2.save('rough2.png')
writer2 = 0
print "Writing 2",(time.clock()-wall),'s'
wall = time.clock()

writer3 = sprite.SpriteSheetWriter(tileSize, (size-1)*tileSize)
for x in range(size-1):
    
    for y in range(size-1):

        writer3.addImage(reader.getTile(int(realTileMap2[x][y][0]),int(realTileMap2[x][y][1])))

writer3.save('rough3.png')
writer3 = 0
print "Writing 3",(time.clock()-wall),'s'
        
scipy.misc.imsave( 'TypeMap.png', typeMap )
scipy.misc.imsave( 'TypeEdgeMap.png', edgeMap )
print 'Finished Everything:',(time.clock()-wall2),'s'
