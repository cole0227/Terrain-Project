from math import log
import sys
import random
import time

from numpy import *
import pylab
import scipy
import scipy.spatial

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
forestCluster     = 5

def region_based_variance(region):
    
    size = int( region.size ** ( 0.5 ) )
    variance = zeros((size,size))
    
    for x in range( 0, size ):

        for y in range( 0, size ):
        
            if(   region[x][y] <= -6 ):
                variance[x][y]  = 3
                
            elif( region[x][y] <= -3 ):
                variance[x][y]  = 8
                
            elif( region[x][y] <= -1 ):
                variance[x][y]  = 3

            elif( region[x][y] <= 0 ):
                variance[x][y]  = 10
                
            elif( region[x][y] <= 3 ):
                variance[x][y]  = 15
                
            elif( region[x][y] <= 5 ):
                variance[x][y]  = 20
                
            elif( region[x][y] <= 8 ):
                variance[x][y]  = 25
    
    save( '.map_var.npy', variance )
    return variance

def variance_main():

    regionMap = Matrix_Double( Matrix_Crop( load('.map_region.npy'), -8, 10 ) )
    stockRegion = load('.map_region.npy')
    
    varMap = Matrix_Double( load( '.map_var.npy' ) )
    size = int( varMap.size ** ( 0.5 ) )
    
    mountainMap = zeros((size/4,size/4))
    mount = 0
    
    mainMap = load('.b3.npy') # it varies from 0 to 40, with a strong preference for the high-end.
    #print "main:",Stats_Percentile(mainMap)
    mainMap = Matrix_Half(mainMap) * 1.5
    #print "main:",Stats_Percentile(mainMap)
    scaleMain = int( mainMap.size ** ( 0.5 ) ) / size
    
    #print "region:",Stats_Range( regionMap )
    #print "varmap:",Stats_Range( varMap )
    #print "region:",Stats_Range( Gaussian_Blur( regionMap, 3.0 ))
    #print "varmap:",Stats_Range( Gaussian_Blur( varMap, 3.0 ))
    varMap = Matrix_Scale( Gaussian_Blur( varMap, 3.0 ), 3, 40 )
    regionMap = Matrix_Scale( Gaussian_Blur( regionMap, 3.0 ), -8, 7)
    
    for x in range( 0, size ):

        if( x % 16 == 0 ):
            print '.',
            sys.stdout.flush()

        for y in range( 0, size ):
        
            for x1 in range( x * scaleMain, scaleMain + x * scaleMain ):

                for y1 in range( y * scaleMain, scaleMain + y * scaleMain ):
                            
                    mainMap[x1][y1] *= varMap[x][y]

                    if(regionMap[x][y] < -1):
                    
                        mainMap[x1][y1] += (regionMap[x][y] + 1 ) * 100
                        #print 'tick'

    print
    
    for x in range( 2, size, 2 ):

        print '.',
        sys.stdout.flush()

        for y in range( 2, size, 2 ):
        
            if( mountainMap[x/4][y/4] == 0 and 
                varMap[x][y] > 19 and 
                regionMap[x][y] > 5 ):

                 mount += 1
                 Spider_Mountain_Wrapper( mainMap,
                     x * scaleMain + scaleMain / 2, 
                     y * scaleMain + scaleMain / 2,
                     250 )

                 for a in range( -1, 2 ):

                     for b in range( -1, 2 ):

                         mountainMap[x/4+b][y/4+a] = 1

    print mount
    print "main:",Stats_Percentile(mainMap)
    mainMap = Matrix_Crop( mainMap, -400, 2000 )
    imsave('regionVarianced.png', mainMap)
    imsave('regionMountains.png', Matrix_Double(Matrix_Double(mountainMap)))
    return mainMap
    

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
                    
                    # Swampy and beachy shallows have a 80% chance of being followed by the same
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
    
    # deep jungle
    for z in range ( 0, jungles ):

        x2 = max( min( x2 + random.randint( -2, 2 + 1 ), size - mapBorder/3 - 1 ), mapBorder/3 )
        y2 = max( min( y2 + random.randint( -2, 2 + 1 ), size - mapBorder/3 - 1 ), mapBorder/3 )
        #print x2,',',y2,',',z

        if( z % forestCluster == 0 ):

            while( not( occupiedMap[x2][y2] == 0 or occupiedMap[x2][y2] == - 5  ) ):
                x2 = random.randint( mapBorder/3, size - mapBorder/3 - 1 )
                y2 = random.randint( mapBorder/3, size - mapBorder/3 - 1 )
                attempts += 1

        if( vegetationMap[x2][y2] == 0 and  ( occupiedMap[x2][y2] == 0 or occupiedMap[x2][y2] == 8 or occupiedMap[x2][y2] == -5 ) ):

            vegetationMap[x2][y2] = 5
            treex[:0] = [x2]
            treey[:0] = [y2]
            for x1 in range (x2-mapBorder/3+1, x2+mapBorder/3):
        
                for y1 in range (y2-mapBorder/3+1, y2+mapBorder/3):
        
                    if( occupiedMap[x1][y1]==0 and ( x2 - x1 )**2 + ( y2 - y1 )**2 <= (mapBorder/3-1)**2 ):
                        
                        occupiedMap[x1][y1]=6

    # less deep jungle
    while len(treex) > 0:
        x = treex.pop()
        y = treey.pop()
        treex2[:0] = [x2]
        treey2[:0] = [y2]
        for x1 in range (x-1, x+2):
    
            for y1 in range (y-1, y+2):
            
                #print vegetationMap[x1][y1],':',x1,',',y1
                
                if( random.random() >= ratioTree * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and vegetationMap[x1][y1] == 0 ):
            
                    vegetationMap[x1][y1] = 4
                    treex2[:0] = [x1]
                    treey2[:0] = [y1]


    # random forest
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

    while len(treex2) > 0:
        x = treex2.pop()
        y = treey2.pop()
        for x1 in range (x-1, x+2):
    
            for y1 in range (y-1, y+2):
            
                #print vegetationMap[x1][y1],':',x1,',',y1
                
                if( random.random() >= ratioTree * ( ( x - x1 )**2 + ( y - y1 )**2 )**(0.5) and x1 < size and x1 >= 0 and y1 < size and y1 >= 0 and vegetationMap[x1][y1] == 0 ):
            
                    vegetationMap[x1][y1] = 3
                    treex[:0] = [x1]
                    treey[:0] = [y1]


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
    
    save( '.map_region.npy', mainMap )
    save( '.map_veg.npy', vegetationMap )
    
    #mainMap = Matrix_Crop(mainMap + vegetationMap/2.5 , -5, 10)
    
    
    #mainMap = Matrix_Double( Matrix_Double( Matrix_Double( Matrix_Double( mainMap ) ) ) )
    #occupiedMap = Matrix_Double( Matrix_Double( Matrix_Double( Matrix_Double( occupiedMap ) ) ) )
    #mainMap = Matrix_Double( mainMap) 
    #occupiedMap = Matrix_Double( occupiedMap )
    #vegetationMap = Matrix_Double( vegetationMap )
    
    imsave('region_%d.png' % forests, mainMap)
    pltt('region_%d_colour.png' % forests, mainMap )
    imsave('region_%d_occupied.png' % forests, occupiedMap)
    imsave('region_%d_vegetation.png' % forests, vegetationMap)

    print 'Export:',(time.clock()-wall),'s'
    wall = time.clock()

    print 'Region Making Took',(time.clock()-wall2),'s. Made', attempts,'Excess Attempts.'
    wall = time.clock()
    
    return mainMap


#
# Combines Random heightmaps with regional data
#
def generateWinning():

    wall = time.clock()

    mainMap = load('.map_region.npy')
    #mainMap = Matrix_Half( mainMap )
    mainMapSize = int( mainMap.size ** ( 0.5 ) )    
    #mainMap = mainMap[( mainMapSize * 3/8 ):( mainMapSize * 5/8 ),( mainMapSize * 3/8 ): ( mainMapSize * 5/8 )]
    mainMapSize = int( mainMap.size ** ( 0.5 ) )
    imsave('region_overview.png', mainMap)


    heightMap = zeros(( mainMapSize, mainMapSize ))
    heightMapSize = int( heightMap.size ** ( 0.5 ) )    
    
    print 'Init:',(time.clock()-wall),'s'
    wall = time.clock()
    
    heightMap += (mainMap + 8) ** 2
    heightMap = Matrix_Double( heightMap )
    heightMap = Matrix_Double( heightMap )
    heightMap = Gaussian_Blur( heightMap, 3 )
    heightMap = Matrix_Double( heightMap )

    print 'One Step:',(time.clock()-wall),'s'
    wall = time.clock()

    heightMap = Matrix_Double( heightMap )
    heightMapSize = int( heightMap.size ** ( 0.5 ) )    

    print 'Two Step:',(time.clock()-wall),'s'
    wall = time.clock()

    heightMap = Gaussian_Blur( heightMap, 2 )

    print 'Three Step:',(time.clock()-wall),'s'
    wall = time.clock()
    
    imsave('regionHeight.png', heightMap)
    heightMap = Matrix_Scale(heightMap, 70, 100)
    noiseMap = Matrix_Scale( load( '.b3.npy' ), 0.9, 1 ) 
    heightMap *= Generate(zeros(( 2048, 2048 )), 0, 0.25 )/ 100 + 150

    print 'Four Step:',(time.clock()-wall),'s'
    wall = time.clock()
    
    for x in range( 0, heightMapSize ):

        print '\r',int(1000.0*x/heightMapSize)/10.0,'%',
        sys.stdout.flush()
        for y in range( 0, heightMapSize ):

            if(heightMap[x][y] > 96):
            
                heightMap[x][y] *= noiseMap[x][y] * ( heightMap[x][y] / 15 - 5.07777777778 )
                
            elif(heightMap[x][y] > 93):
            
                heightMap[x][y] *= noiseMap[x][y] * ( heightMap[x][y] / 18 - 4.01111111111 )
                
            elif(heightMap[x][y] > 90):
            
                heightMap[x][y] *= noiseMap[x][y] * ( heightMap[x][y] / 20 - 3.5 )
                
            elif(heightMap[x][y] < 80):
            
                heightMap[x][y] *= noiseMap[x][y] * ( heightMap[x][y] / 20 - 3 )
                
            elif(heightMap[x][y] < 75):
            
                heightMap[x][y] *= noiseMap[x][y] * ( heightMap[x][y] / 23 - 2.510869565 )
                
            else:
            
                heightMap[x][y] *= noiseMap[x][y]


    print '\rMain Loop:',(time.clock()-wall),'s'
    wall = time.clock()
    x = int( time.clock() * 100 )
    imsave('regionHeight_%d.png' % x, heightMap)
    
    heightMap = Gaussian_Blur( heightMap, 3 )
    #heightMap = Matrix_Half( heightMap )
    heightMap = Matrix_Scale( heightMap, 0, 40 )
    b = Rivers( heightMap, ( heightMapSize / 32 )**2 )
    b += Gaussian_Blur( b, 5 ) * 1.5
    b = Matrix_Crop( b, -26, -1 ) + 1
    heightMap += b / 20.0
    heightMap = Matrix_Crop( heightMap, 0, 40 )

    imsave('regionHeight_%d_.png' % x, heightMap)
    #heightMap = Matrix_Half( heightMap )
    print 'Final Leg:',(time.clock()-wall),'s'
    print 'Called Image:', x


if __name__ == '__main__':

    wall = time.clock()

    #Comment out if .b3.npy exists
    a=Rolling_Hills()
    #a = main( 256, 900, 500, 200, 7000)
    a = main( 128, 225, 125, 50, 1750)
    a = region_based_variance(a)
    imsave('region_7000_variance.png', a)

    #generateWinning()

    a = variance_main()
    #a = Matrix_Half(a)
    print 'Finished Variance:',(time.clock()-wall),'s'
    a = Matrix_Scale(a,0,100)
    save('.variance.npy',a)
    a = load('.variance.npy')
    b = load('.variance.npy')
    #a = Erosion_Water( a, 5, 0.95, 0.5, 0.80, 0.95, 5 )
    print "Slope:",Stats_Percentile(Slope_Field(a))
    print "Value:",Stats_Percentile(a)
    b = Erosion_Thermal(a, 3, 0.8)
    print "Slope:",Stats_Percentile(Slope_Field(a))
    print "Value:",Stats_Percentile(a)
    save( '.map_complete.npy', a )
    imsave( 'regionVarianced_Eroded.png', a )

    a = (Matrix_Scale(a,0,100)-b)*2 + b
    imsave( 'regionVarianced_HeavilyEroded.png', a )

    print 'Finished Everything:',(time.clock()-wall),'s'


