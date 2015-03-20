from numpy import *
from math import log

import pylab
import scipy
import scipy.spatial
import random
import time

from functions import *


# Main Map levels:
# -8 through -6 is deep water
# -4 through -3 is shallows
# -2 is swamps
# -1 is beaches
# 
# 0 is meadows and scattered trees
# 
# 1 through 3 is hills
# 4 through 5 is mountianous
# 6 through 7 is massive mountains


# Globals

waterEdgeVariance = 9
waterRatio        = 0.22
waterDistance     = 4
waterCluster      = 100
ratio             = 0.7
mapBorder         = 6
mountainDistance  = 3
mountainCluster   = 10
ratioTree         = 0.25
forestCluster     = 25


def main( size, water, mountains, jungles, forests ):
        
    wall = time.clock()
    wall2 = time.clock()
    mainMap = zeros(( size,size ))
    occupiedMap =  zeros(( size,size ))
    vegetationMap =  zeros(( size,size ))
    attempts = 0
    
    wateredgex = []
    wateredgey = []
    waterx = []
    watery = []
    shallowx = []
    shallowy = []
    shallowx2 = []
    shallowy2 = []
    
    # First, we edge the map in water    
    
    for x2 in range (0, size, waterDistance):
        
        offset = random.randint( 0, waterEdgeVariance )
        mainMap[x2][0 + offset] = -8
        waterx[:0] = [x2]
        watery[:0] = [0 + offset]
        wateredgex[:0] = [x2]
        wateredgey[:0] = [0 + offset]
        
        offset = random.randint( 0, waterEdgeVariance )
        mainMap[x2][size - 1 - offset] = -8
        waterx[:0] = [x2]
        watery[:0] = [size - 1 - offset]
        wateredgex[:0] = [x2]
        wateredgey[:0] = [size - 1 - offset]
        
        mainMap[x2][0] = -8
        waterx[:0] = [x2]
        watery[:0] = [0]
        wateredgex[:0] = [x2]
        wateredgey[:0] = [0]
        
        mainMap[x2][size - 1] = -8
        waterx[:0] = [x2]
        watery[:0] = [size - 1]
        wateredgex[:0] = [x2]
        wateredgey[:0] = [size - 1]

    for y2 in range (0, size, 4):
        
        offset = random.randint( 0, waterEdgeVariance )
        mainMap[0 + offset][y2] = -8
        waterx[:0] = [0 + offset]
        watery[:0] = [y2]
        wateredgex[:0] = [0 + offset]
        wateredgey[:0] = [y2]

        offset = random.randint( 0, waterEdgeVariance )
        mainMap[size - 1 - offset][y2] = -8
        waterx[:0] = [size - 1 - offset]
        watery[:0] = [y2]
        wateredgex[:0] = [size - 1 - offset]
        wateredgey[:0] = [y2]

        mainMap[0][y2] = -8
        waterx[:0] = [0]
        watery[:0] = [y2]
        wateredgex[:0] = [0]
        wateredgey[:0] = [y2]

        mainMap[size - 1][y2] = -8
        waterx[:0] = [size - 1]
        watery[:0] = [y2]
        wateredgex[:0] = [size - 1]
        wateredgey[:0] = [y2]

    # and then we ensure that this fills the occupied map too

    while len(wateredgex) > 0:
        x2 = wateredgex.pop()
        y2 = wateredgey.pop()
        for x1 in range (x2-mapBorder-6, x2+mapBorder+7):
    
            for y1 in range (y2-mapBorder-6, y2+mapBorder+7):
    
                if( x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (waterDistance-2)**2 + 2 ):
                    
                    occupiedMap[x1][y1] = - 13

                if( x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (mapBorder + 3 )**2 - 2 and ( occupiedMap[x1][y1] == -5 or occupiedMap[x1][y1] == 0 ) ):
                    
                    occupiedMap[x1][y1] = - 10

                elif( x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (mapBorder+6)**2 + 5 and occupiedMap[x1][y1] == 0 ):
                    
                    occupiedMap[x1][y1] = - 5

    # then we randomly place more deep water around the map
    
    x2 = random.randint( mapBorder, size - mapBorder - 1 )
    y2 = random.randint( mapBorder, size - mapBorder - 1 )
    quadrant = 0
    quadx = 0
    quady = 0

    for z in range (0, water):
        
        x2 = max( min( x2 + random.randint( -waterDistance, waterDistance + 1 ), size - mapBorder - 1 ), mapBorder )
        y2 = max( min( y2 + random.randint( -waterDistance, waterDistance + 1 ), size - mapBorder - 1 ), mapBorder )
        #print x2,',',y2,',',z

        if( z % waterCluster == 0 ):
        
            while( 
                not( occupiedMap[x2][y2] == 0 ) 
                and quadx < x2  and quady < y2 ):
            
                x2 = random.randint( mapBorder, size - mapBorder - 1 )
                y2 = random.randint( mapBorder, size - mapBorder - 1 )
                attempts += 1
                quadx = quadrant % 2 * (size - 1) / 2 
                quady = quadrant / 2 % 2 * (size - 1) / 2 
                #print quadx,quady
                
            quadrant += 1
            
        
        
        if( mainMap[x2][y2] == 0 and not (occupiedMap[x2][y2] == -13) ):
        
            mainMap[x2][y2] = -8
            waterx[:0] = [x2]
            watery[:0] = [y2]
            
            for x1 in range (x2-mapBorder-6, x2+mapBorder+7):
        
                for y1 in range (y2-mapBorder-6, y2+mapBorder+7):
        
                    if( x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (waterDistance-2)**2 + 2 ):
                        
                        occupiedMap[x1][y1] = - 13

                    if( x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (mapBorder + 3 )**2 - 2 and ( occupiedMap[x1][y1] == -5 or occupiedMap[x1][y1] == 0 ) ):
                        
                        occupiedMap[x1][y1] = - 10

                    elif( x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (mapBorder+6)**2 + 5 and occupiedMap[x1][y1] == 0 ):
                        
                        occupiedMap[x1][y1] = - 5

    
    #print waterx
    #print watery
    
    while len(waterx) > 0:
        x = waterx.pop()
        y = watery.pop()
        shallowx[:0] = [x]
        shallowy[:0] = [y]
        for x1 in range (x-1, x+2):
    
            for y1 in range (y-1, y+2):
            
                #print mainMap[x1][y1],':',x1,',',y1
                
                if( random.random() >= waterRatio * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and mainMap[x1][y1] == 0 ):
            
                    mainMap[x1][y1] = - 9
                    shallowx[:0] = [x1]
                    shallowy[:0] = [y1]
    
    for z in range( 0, 2 ):
    
        #print shallowx
        #print shallowy

        while len(shallowx) > 0:
            
            x = shallowx.pop()
            y = shallowy.pop()
            shallowx2[:0] = [x]
            shallowy2[:0] = [y]
        
            for x1 in range (x-1, x+2):
        
                for y1 in range (y-1, y+2):
            
                    if( random.random() >= waterRatio * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and mainMap[x1][y1] == 0 ):
                
                        mainMap[x1][y1] = - 6 + z * 2
                        shallowx2[:0] = [x1]
                        shallowy2[:0] = [y1]
        
        #print shallowx2
        #print shallowy2
        
        while len(shallowx2) > 0:
            
            x = shallowx2.pop()
            y = shallowy2.pop()
            shallowx[:0] = [x]
            shallowy[:0] = [y]
            
            for x1 in range (x-1, x+2):
        
                for y1 in range (y-1, y+2):
            
                    if( random.random() >= waterRatio * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and mainMap[x1][y1] == 0 ):
                
                        mainMap[x1][y1] = - 5 + z * 2
                        shallowx[:0] = [x1]
                        shallowy[:0] = [y1]

    #Swamps and Beaches
    swampy = 1
    while len(shallowx) > 0:
        
        x = shallowx.pop()
        y = shallowy.pop()
    
        for x1 in range (x-1, x+2):
    
            for y1 in range (y-1, y+2):
        
                if( random.random() >= waterRatio * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and mainMap[x1][y1] == 0 ):
                    
                    # Swampy and beachy shallows have a 70% chance of being followed by the same
                    if( swampy == 1 and random.random() >= 0.2 ):
                        mainMap[x1][y1] = - 2
                    elif( swampy == 0 and random.random() >= 0.8 ):
                        mainMap[x1][y1] = - 2
                        swampy = 1
                    else:
                        mainMap[x1][y1] = - 1
                        swampy = 0
                        
                    shallowx2[:0] = [x1]
                    shallowy2[:0] = [y1]


    print 'Oceans:',(time.clock()-wall),'s'
    wall = time.clock()

    #Mountains

    mountainx = []
    mountainy = []
    hillx = []
    hilly = []
    hillx2 = []
    hilly2 = []
    
    x2 = random.randint( mapBorder, size - mapBorder - 1 )
    y2 = random.randint( mapBorder, size - mapBorder - 1 )

    for z in range (0, mountains):
        
        x2 = max( min( x2 + random.randint( -mountainDistance, mountainDistance + 1 ), size - mapBorder - 1 ), mapBorder )
        y2 = max( min( y2 + random.randint( -mountainDistance, mountainDistance + 1 ), size - mapBorder - 1 ), mapBorder )
        #print x2,',',y2,',',z

        if( z % mountainCluster == 0 ):
            while( not( occupiedMap[x2][y2] == 0 ) ):
                x2 = random.randint( mapBorder, size - mapBorder - 1 )
                y2 = random.randint( mapBorder, size - mapBorder - 1 )
                attempts += 1
        
        
        if( mainMap[x2][y2] == 0 and occupiedMap[x2][y2] == 0 ):
        
            mainMap[x2][y2] = 7
            hillx[:0] = [x2]
            hilly[:0] = [y2]
            
            for x1 in range (x2-mapBorder+1, x2+mapBorder):
        
                for y1 in range (y2-mapBorder+1, y2+mapBorder):
        
                    if( ( occupiedMap[x1][y1]==0 or occupiedMap[x1][y1]==8 or occupiedMap[x1][y1]==-5 ) and ( x2 - x1 )**2 + ( y2 - y1 )**2 - 1 <= (mapBorder-3)**2 ):
                        
                        occupiedMap[x1][y1]=10
    
                    if( occupiedMap[x1][y1]==0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (mapBorder)**2 - 3 ):
                        
                        occupiedMap[x1][y1]=8
    
    #print mountainx
    #print mountainy
    
    for z in range( 0, 3 ):
    
        #print hillx
        #print hilly

        while len(hillx) > 0:
            
            x = hillx.pop()
            y = hilly.pop()
            hillx2[:0] = [x]
            hilly2[:0] = [y]
        
            for x1 in range (x-1, x+2):
        
                for y1 in range (y-1, y+2):
            
                    if( random.random() >= ratio and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and mainMap[x1][y1] == 0 ):
                
                        mainMap[x1][y1] = 6 - z * 2
                        hillx2[:0] = [x1]
                        hilly2[:0] = [y1]
        
        #print hillx2
        #print hilly2
        
        while len(hillx2) > 0:
            
            x = hillx2.pop()
            y = hilly2.pop()
            hillx[:0] = [x]
            hilly[:0] = [y]
        
            for x1 in range (x-1, x+2):
        
                for y1 in range (y-1, y+2):
            
                    if( random.random() >= ratio and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and mainMap[x1][y1] == 0 ):
                
                        mainMap[x1][y1] = 5 - z * 2
                        hillx[:0] = [x1]
                        hilly[:0] = [y1]
                        
    print 'Mountains:',(time.clock()-wall),'s'
    wall = time.clock()

    #Now tree time
    
    x2 = random.randint( mapBorder, size - mapBorder - 1 )
    y2 = random.randint( mapBorder, size - mapBorder - 1 )
    
    
    treex = []
    treey = []
    treex2 = []
    treey2 = [] 
    treex3 = []
    treey3 = []
    
    for z in range ( 0, forests ):

        x2 = max( min( x2 + random.randint( -2, 2 + 1 ), size - mapBorder/3 - 1 ), mapBorder/3 )
        y2 = max( min( y2 + random.randint( -2, 2 + 1 ), size - mapBorder/3 - 1 ), mapBorder/3 )
        #print x2,',',y2,',',z

        if( z % forestCluster == 0 ):

            while( not( occupiedMap[x2][y2] == 0 or occupiedMap[x2][y2] == - 5  ) ):
                x2 = random.randint( mapBorder/3, size - mapBorder/3 - 1 )
                y2 = random.randint( mapBorder/3, size - mapBorder/3 - 1 )
                attempts += 1

        if( vegetationMap[x2][y2] == 0 and  ( occupiedMap[x2][y2] == 0 or occupiedMap[x2][y2] == 8 or occupiedMap[x2][y2] == -5 ) ):

            vegetationMap[x2][y2] = 3
            treex[:0] = [x2]
            treey[:0] = [y2]
            for x1 in range (x2-mapBorder/3+1, x2+mapBorder/3):
        
                for y1 in range (y2-mapBorder/3+1, y2+mapBorder/3):
        
                    if( occupiedMap[x1][y1]==0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (mapBorder/3-1)**2 ):
                        
                        occupiedMap[x1][y1]=5

    while len(treex) > 0:
        x = treex.pop()
        y = treey.pop()
        treex2[:0] = [x2]
        treey2[:0] = [y2]
        for x1 in range (x-1, x+2):
    
            for y1 in range (y-1, y+2):
            
                #print vegetationMap[x1][y1],':',x1,',',y1
                
                if( random.random() >= ratioTree * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and vegetationMap[x1][y1] == 0 ):
            
                    vegetationMap[x1][y1] = 2
                    treex2[:0] = [x1]
                    treey2[:0] = [y1]

    while len(treex2) > 0:
        x = treex2.pop()
        y = treey2.pop()
        for x1 in range (x-1, x+2):
    
            for y1 in range (y-1, y+2):
            
                #print vegetationMap[x1][y1],':',x1,',',y1
                
                if( random.random() >= ratioTree * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and vegetationMap[x1][y1] == 0 ):
            
                    vegetationMap[x1][y1] = 1


    print 'Forests:',(time.clock()-wall),'s'
    wall = time.clock()
    
    mainMap = Matrix_Crop(mainMap + vegetationMap/2.5 , -5, 10)
    #mainMap = Matrix_Double( Matrix_Double( Matrix_Double( Matrix_Double( mainMap ) ) ) )
    #occupiedMap = Matrix_Double( Matrix_Double( Matrix_Double( Matrix_Double( occupiedMap ) ) ) )
    #mainMap = Matrix_Double( mainMap) 
    #occupiedMap = Matrix_Double( occupiedMap )
    #vegetationMap = Matrix_Double( vegetationMap )
    
    scipy.misc.imsave('region_%d.png' % forests, mainMap)
    #pltt('region_%d_colour.png' % forests, mainMap )
    #scipy.misc.imsave('region_%d_occupied.png' % forests, occupiedMap)
    #scipy.misc.imsave('region_%d_vegetation.png' % forests, vegetationMap)

    print 'Export:',(time.clock()-wall),'s'
    wall = time.clock()

    print 'Took',(time.clock()-wall2),'s. Made', attempts,'Excess Attempts.'
    wall = time.clock()


for x in range( 0, 5 ):
    #main( 512, 3600, 2500, 20, 30000+x)
    main( 256, 900, 500, 5, 7000+x)
    #main( 128, 100, 125, 1, 1750+x)
    #main( 64, 0, 20, 1, 300+x)


