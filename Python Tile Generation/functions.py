from multiprocessing import Process, Queue
import random
import time
import sys
from PIL import Image

import matplotlib.pyplot as plt
from numpy import *
import pylab
import scipy
import scipy.spatial
from scipy.misc import imsave

import hills

#
# image saving
#
def imsave(i, a):

    scipy.misc.imsave(i,a)
    

#
# Blurs quickly to the radius specified
#
def Gaussian_Blur( amatrix, radius ):

    size = int( amatrix.size ** ( 0.5 ) )
    kernel = hills.gaussian_kernel( size, size, radius )
    blur = hills.apply_kernel( size, size, amatrix, kernel )
    return blur


#
# Cuts off any elements outside of the min and max
#
def Matrix_Crop(amatrix,minimum,maximum):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( 0, size ):

        for y in range( 0, size ):

            amatrix[x][y] = max( minimum, min( maximum, amatrix[x][y] ) )
    return amatrix


#
# Forces the numbers in a matrix to within set bounds
#
def Matrix_Scale(amatrix,minimum,maximum):
        
    size = int( amatrix.size ** ( 0.5 ) )
    rs = Stats_Range( amatrix )
    factor = ( maximum - minimum ) / ( rs[1] - rs[0] )
    amatrix = ( amatrix - rs[0] ) * factor + minimum
    return amatrix


#
# Merges a small matrix on top of a large one
#
def Matrix_Merge( large, small, offsetx, offsety):
    size = int( small.size ** ( 0.5 ) )
    for x in range( 0, size):

        for y in range( 0, size ):
        
            large[x + offsetx][y + offsety] += small[x][y]
    
    return large


#
# Returns a matrix 1/2 the dimensions of the original
#
def Matrix_Half(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    another = zeros(( size/2, size/2 ))

    for x in range( 0, size, 2 ):
    
        for y in range( 0, size, 2 ):
        
            another[x/2][y/2] = ( amatrix[x][y] + amatrix[x+1][y] + amatrix[x][y+1] + amatrix[x+1][y+1] ) / 4.0
    
    return another

#
# Returns a matrix 1/8 the dimensions of the original
#
def Matrix_Tiny(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    another = zeros(( size/8, size/8 ))

    for x in range( 0, size, 8 ):
    
        for y in range( 0, size, 8 ):
        
            another[x / 8][y / 8] += amatrix[x][y] / 4.0
    
    return another


#
# Doubles the dimensions of a matrix
#
def Matrix_Double(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    b = zeros( ( size * 2, size * 2 ))
    for x in range( 0, size ):
    
        for y in range( 0, size ):
    
            b[2*x  ][2*y  ] = amatrix[x][y]
            b[2*x+1][2*y  ] = amatrix[x][y]
            b[2*x  ][2*y+1] = amatrix[x][y]
            b[2*x+1][2*y+1] = amatrix[x][y]
    
    return b


#
# changes a value in a matrix
#
def Matrix_Fromto( amatrix, start, end ):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( 0, size ):
    
        for y in range( 0, size ):
    
            if( amatrix[x][y] == start ):
                
                amatrix[x][y] = end
            
    
    return amatrix


#
# Slope Field Generator
#
def Slope_Field(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    slopes = zeros(( size, size ))
    for x in range( 1, size-1 ):
    
        for y in range( 1, size-1 ):
        
            slopes[x][y] = max(abs(amatrix[x][y] - amatrix[x][y-1]), abs(amatrix[x][y] - amatrix[x-1][y]))
                
    return slopes


#
# Return values within a certain range
#
def Elevation_Selection( amatrix, low, high, lowfill, highfill ):
    size = int( amatrix.size ** ( 0.5 ) )
    selection = zeros(( size, size )) + lowfill
    for x in range( 0, size ):
    
        for y in range( 0, size ):
        
            if( amatrix[x][y] >=  low and amatrix[x][y] <= high ):
            
                selection[x][y] = amatrix[x][y]
                
            elif( amatrix[x][y] >= high ):
            
                selection[x][y] = highfill
            
    return selection


#
# plt output function, so that we don't have to import this elsewhere
#
def pltt( stri, amatrix ):

    size = int( amatrix.size ** ( 0.5 ) )
    fig = plt.figure()    
    fig.set_size_inches( size * 0.32259375 , size * 0.32259375 )
    plt.imshow( amatrix )
    fig.savefig(
        stri, 
        bbox_inches = 'tight', pad_inches = 0, dpi = 4 )


#########################################################################
#
#  Stats Functions
#
#########################################################################


#
# Finds the Largest and smallest element
#
def Stats_Range(amatrix):

    mymatrix = amatrix.reshape( -1 )
    sort = mymatrix.argsort()
    final = [mymatrix[sort[0]], mymatrix[sort[ amatrix.size - 1 ]]]
    return final


#
# Gives the value for the 9 intermediary 10th-percentile
# elevations, and the highest and lowest points
#
def Stats_Percentile( amatrix ):
    
    mymatrix = amatrix.reshape( -1 )
    sort = mymatrix.argsort()

    #
    # Returns the element for the matching percent
    #
    def Find_Percentile( percent ):
        
        return sort[ min( max( int( ( amatrix.size - 1 ) * percent / 100), 0 ), amatrix.size - 1 ) ]

    final = zeros(( 11 )) 
    for x in range( 0, 11 ):

        final[x] = mymatrix[ Find_Percentile( x * 10 ) ]

    return final




#
# Calculates the Standard Deviation, Devides it by the average height of the matrix
#
def Stats_Erosion_Score( amatrix ):

    standard = 0
    size = int( amatrix.size ** ( 0.5 ) )
    s = sum(amatrix)/size/size
    for x in range( 1, size-1 ):
    
        for y in range( 1, size-1 ):
        
            standard += ( amatrix[x][y] - s ) ** 2.0
    
    standard /= size * size
    standard = standard ** ( 0.5 ) / s
    return s


#############################################################
#
# Thermally erode a map. Erosion_Thermal*
#
# Helper functions provide different algorithms and patterns
#
#############################################################

#
# Squareish Helper
#
def Erosion_Thermal_Helper( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y]
    d2 = amatrix[x][y] - amatrix[x][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y]
    d4 = amatrix[x][y] - amatrix[x][y+1]
    
    dmax = max( d1, d2, d3, d4, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y-1] += tomove
    elif(d3 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y] += tomove
    elif(d4 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y+1] += tomove


#
# Diagonals
#
def Erosion_Thermal_Helper_Diag( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y-1]
    d2 = amatrix[x][y] - amatrix[x+1][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y+1]
    d4 = amatrix[x][y] - amatrix[x-1][y+1]
    
    dmax = max( d1, d2, d3, d4, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y-1] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y-1] += tomove
    elif(d3 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y+1] += tomove
    elif(d4 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y+1] += tomove


#
# Sweeping
#
def Erosion_Thermal_Helper_Sweep( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y-1]
    d2 = amatrix[x][y] - amatrix[x][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y-1]
    d4 = amatrix[x][y] - amatrix[x+1][y]
    
    dmax = max( d1, d2, d3, d4, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove * 0.7
        amatrix[x-1][y-1] += tomove * 0.7
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y-1] += tomove
    elif(d3 == dmax):
        amatrix[x][y] -= tomove * 0.7
        amatrix[x+1][y-1] += tomove * 0.7
    elif(d4 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y] += tomove

    
#
# Verticalish
#
def Erosion_Thermal_Helper_V( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x][y-1]
    d2 = amatrix[x][y] - amatrix[x][y+1]
    
    dmax = max( d1, d2, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y-1] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y+1] += tomove


#
# Horzish
#
def Erosion_Thermal_Helper_H( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y]
    d2 = amatrix[x][y] - amatrix[x+1][y]
    
    dmax = max( d1, d2, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y] += tomove


#
# Wild/stupid
#
def Erosion_Thermal_Helper_Stupid( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y-1]
    d2 = amatrix[x][y] - amatrix[x+1][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y+1]
    d4 = amatrix[x][y] - amatrix[x-1][y+1]
    
    factor = 2.0
    amatrix[x][y] -= d1 / factor
    amatrix[x-1][y-1] += d1 / factor
    amatrix[x][y] -= d2 / factor
    amatrix[x+1][y-1] += d2 / factor
    amatrix[x][y] -= d3 / factor
    amatrix[x+1][y+1] += d3 / factor
    amatrix[x][y] -= d4 / factor
    amatrix[x-1][y+1] += d4 / factor


#
# Erodes thermally
#
def Erosion_Thermal( amatrix, its = 5, minimum = 5 ):

    for z in range( 0, its ):
        
        size = int( amatrix.size ** ( 0.5 ) )
        for x in range( 1, size-1 ):
            
            for y in range( 1, size-1 ):
            
                Erosion_Thermal_Helper( amatrix, x, y, minimum )
                Erosion_Thermal_Helper_Diag( amatrix, x, y, minimum )
        
    return amatrix


#
# Midpoint Displacement Method
#
def Midpoint_Displacement( amatrix ):

    size = int( amatrix.size ** ( 0.5 ) )
    step = size-1
    
    amatrix[0][0] = random.uniform( 0, step * 2 )
    amatrix[step][0] = random.uniform( 0, step * 2 )
    amatrix[0][step] = random.uniform( 0, step * 2 )
    amatrix[step][step] = random.uniform( 0, step * 2 )

    while( step > 1 ):
    
        #imsave( 'map_16_progress_%d.png' % (size/step), amatrix )
        # this section 
        for x in range( 0, size-1, step ):
            
            for y in range( 0, size-1, step ):
                
                #print '(',step,',',x,',',y,')'
                amatrix[x+step/2][y+step/2] = ( 
                    amatrix[x][y] +
                    amatrix[x+step][y] +
                    amatrix[x][y+step] +
                    amatrix[x+step][y+step] ) / 4 + random.uniform( -step, step )

                #The following is a hack for dark edges
                if( x == 0 or y == 0 or x == size-1 or y == size-1):
                    amatrix[x][y] = -size
            
        for x in range( 0, size, step/2 ):
            
            for y in range( ( x + step / 2 ) % step , size, step ):

                #print '(',step,',',x,',',y,')'
                amatrix[x][y] = ( 
                    amatrix[( x - step / 2 ) % ( size - 1 ) ][y] +
                    amatrix[( x + step / 2 ) % ( size - 1 ) ][y] +
                    amatrix[x][( y - step / 2 ) % ( size - 1 ) ] +
                    amatrix[x][( y + step / 2 ) % ( size - 1 ) ] ) / 4

                    
                amatrix[x][y] += random.uniform( -step, step )

                #The following is a hack for dark edges
                if( x == 0 or y == 0 or x == size-1 or y == size-1):
                    amatrix[x][y] = -size
                
                if( x == 0 ):
                    amatrix[size-1][y] = random.uniform( -step, step )

                if( x == 0 ):
                    amatrix[x][size-1] = random.uniform( -step, step )

        step /= 2
    return amatrix


#
# Generates p Varonoi-centered rivers
#
def Rivers(amatrix,p):
    
    points=zeros((p,2))
    size = int( amatrix.size ** ( 0.5 ) )
    rivers=zeros((size,size))
        
    for z in range( 0, p ):

        print '\r',int(1000.0*z/p)/10.0,'%',
        sys.stdout.flush()

        width = size / ( p ** 0.5 )
        x =  (z) * width
        y =  (z) / int( p ** 0.5 ) * width
        points[z][0] = int( random.uniform( x, x + width ) % size )
        points[z][1] = int( random.uniform( y, y + width ) % size )
    
    for z in range( 0, p ):
        
        print '\r',int(1000.0*z/p)/10.0,'%',
        sys.stdout.flush()

        river=zeros((size,size))
        x = points[z][0]
        y = points[z][1]
        for w in range( -51, 51 ):
                    
            x1 = ( x - 1 ) % size
            x2 = ( x + 1 ) % size
            y1 = ( y - 1 ) % size
            y2 = ( y + 1 ) % size
            
            d1 = ( amatrix[x][y] - amatrix[x1][y ] )
            d2 = ( amatrix[x][y] - amatrix[x2][y ] )
            d3 = ( amatrix[x][y] - amatrix[x ][y1] )
            d4 = ( amatrix[x][y] - amatrix[x ][y2] )
            d5 = ( amatrix[x][y] - amatrix[x1][y2] ) / 1.37
            d6 = ( amatrix[x][y] - amatrix[x2][y1] ) / 1.37
            d7 = ( amatrix[x][y] - amatrix[x1][y1] ) / 1.37
            d8 = ( amatrix[x][y] - amatrix[x2][y2] ) / 1.37
            
            dmax = max( d1, d2, d3, d4, d5, d6, d7, d8, 0 )
            
            rivers[x][y] += (abs(w)-51)
            #print x,",",y
            
            if(d1 == dmax):
                x = x1
            elif(d2 == dmax):
                x = x2
            elif(d3 == dmax):
                y = y1
            elif(d4 == dmax):
                y = y2
            elif(d5 == dmax):
                x = x1
                y = y2
            elif(d6 == dmax):
                x = x2
                y = y1
            elif(d7 == dmax):
                x = x1
                y = y1
            elif(d8 == dmax):
                x = x2
                y = y2
            else:
                #print z,",",w
                if ( w > -30 ):
                    rivers+=river
                break

    print '\rRivers Finished'
    #rivers = rivers + Gaussian_Blur(rivers,3) * 15.0
    return rivers


#
# Adds sparse dots to a matrix
#
def Sparse_Hills_Basic( amatrix, number, strength ):

    size = int( amatrix.size ** ( 0.5 ) )
    for num in range( 0, number ):
    
        amatrix[random.randint( size / 8, size * 7 / 8 )][random.randint( size / 8, size * 7 / 8 )]=strength


def Sparse_Hills( amatrix, number, edge ):

    size = int( amatrix.size ** ( 0.5 ) )
    for num in range( 0, number ):
        
        x = random.randint( edge, size - edge )
        y = random.randint( edge, size - edge )
        amatrix[x][y]=100
        e = edge / 2
        x += random.randint( -e , e )
        y += random.randint( -e , e )
        amatrix[x][y]=75
        e /= 2
        x += random.randint( -e , e )
        y += random.randint( -e , e )
        amatrix[x][y]=66
        x += random.randint( -e , e )
        y += random.randint( -e , e )
        amatrix[x][y]=50
        
    return amatrix



#
# Lowers points far from the middle
#
def Dome(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    modified = 0
    rng = Stats_Range(amatrix)
    for x in range( 0, size ):
    
        for y in range( 0, size ):
        
            distance = sqrt( 2.0 ) / size * sqrt(
            
                ( x - ( size - 0.7 ) / 2 ) ** 2 +
                ( y - ( size - 0.7 ) / 2 ) ** 2 )
            
            amatrix[x][y] /= max( distance, 0.40 ) * 50
            amatrix[x][y] /= max( distance, 0.45 ) * 150
            amatrix[x][y] /= max( distance, 0.50 ) * 300
            amatrix[x][y] /= max( distance, 0.55 ) * 300
    
    return Matrix_Scale( amatrix, rng[0], rng[1] )

#
# Better way to lower points far from the middle
#
def Terrain_Dome(amatrix):

    wall = time.clock()
    size = int( amatrix.size ** ( 0.5 ) )
    effect = 0
    for x in range( 0, size ):
    
        for y in range( 0, size ):
        
            distance = sqrt( 2.0 ) / size * sqrt(
            
                ( x - ( size - 0.7 ) / 2 ) ** 2 +
                ( y - ( size - 0.7 ) / 2 ) ** 2 )
            
            effect -= amatrix[x][y]
            for z in range( 48, 65, 4 ):
                amatrix[x][y] /= max( distance, z / 100.0 )
            
            #amatrix[x][y] += 2 / max( min( distance, 0.45 ), 0.25 )
            #amatrix[x][y] += 2 / max( min( distance, 0.35 ), 0.20 )
            #if( amatrix[x][y] < 55 and distance < 0.3 ):
            #    amatrix[x][y] = 55
            #    effect += 1
            
            effect += amatrix[x][y]
    
    #print 1.0 * effect/size/size
    return Matrix_Scale( amatrix, 0, 100 )


#
# produces the Y for spider_mountain
#
def Spider_Y( direction ):
    
    if( direction > 4 ):

        return -1;

    elif( direction > 0 and direction < 4 ):

        return 1;
    
    return 0;


#
# produces the X for spider_mountain
#
def Spider_X( direction ):
    
    if( direction > 2 and direction < 6 ):

        return 1;

    elif( direction > 6 or direction < 2 ):

        return -1;
    
    return 0;


#
# Inner function for doing sppidery mountains
#
# direction is the 8 cardinals, with 0 being up
#
#   701
#   6 2
#   543
#
def Spider_Mountain(amatrix, x, y, height, direction, f, togo):

    b = 0.2

    #change the += to =, and fill the map with them to see the nightmare
    amatrix[x][y] += height

    # adds more bulk and solidity
    left = (direction+7)%8
    right = (direction+1)%8
    amatrix[x+  Spider_X(left )][y+  Spider_Y(left )] += height / 2
    amatrix[x+  Spider_X(right)][y+  Spider_Y(right)] += height / 2
    amatrix[x+2*Spider_X(left )][y+2*Spider_Y(left )] += height / 4
    amatrix[x+2*Spider_X(right)][y+2*Spider_Y(right)] += height / 4
    amatrix[x+3*Spider_X(left )][y+3*Spider_Y(left )] += height / 7
    amatrix[x+3*Spider_X(right)][y+3*Spider_Y(right)] += height / 7

    if( random.random() < 0.10 ):
        direction += random.randint(-1,1)
    
    if( togo == 0 ):
        
        return 0
            
    else:

        if( togo % random.randint(8,15) == 0 ):

            left  = ( direction+7 ) % 8
            right =  ( direction+1 ) % 8
            
            Spider_Mountain(amatrix, x+Spider_X(left ), y+Spider_Y(left ), height*f, left , f, togo-1 )
            Spider_Mountain(amatrix, x+Spider_X(right), y+Spider_Y(right), height*f, right, f, togo-1 )

        elif( random.random() < 0.93):

            Spider_Mountain(amatrix, x+Spider_X(direction  ), y+Spider_Y(direction  ), height*f, direction, f, togo-1 ) 

    return 0


#
# Wrapper for preceding function, calls 4 ridges of length togo to spawn at x and y
#
# Is best followed by adding a gaussian of 3 and 6, each at *10 to show up well against it
#
def Spider_Mountain_Wrapper( amatrix, x, y, height = 100, f = 0.91, togo = 50 ):

    amatrix[x][y] -= height * 3
    Spider_Mountain(amatrix, x, y, height, random.randint(0,1), f, togo)
    Spider_Mountain(amatrix, x, y, height, random.randint(2,3), f, togo)
    Spider_Mountain(amatrix, x, y, height, random.randint(4,5), f, togo)
    Spider_Mountain(amatrix, x, y, height, random.randint(6,7), f, togo)
    return amatrix


#
# Water-based Erosion takes place in four phases
# 1. Adding new water
# 2. Water eroding the rock
# 3. Water transporting itself and the sediment
# 4. Water evaporates
# 5. depositing sediment
#
# amatrix is the matrix to work on
# its is the number of iterations the algorithm runs through
# d is the amount of rock water pulls up
# maxrat is the amount of sediment and water to move, 0.5 creates flatness
# evap is the rate of evaporation of the water
# sed is the rate of converting sediment into rock each round
# at teh end of the algorithm, remaining sediment is removed from existance
# set to 3.5 for unusual results
# waterinc is the amount of water to add each round
#

def Erosion_Water( amatrix, its = 10, d = 0.95, maxrat = 0.5, evap = 0.05, sed = 0.5, waterinc = 10 ):

    size = int( amatrix.size ** ( 0.5 ) )

    # the water sitting on top of everything
    water = zeros((size,size))

    sumsediment = 0
    sumwater = 0

    for z in range( its ):

        watercap = 0;

        #add water to the map
        water += waterinc
        sumwater += size * size * waterinc

        #have each unit of water draw up d rock into the sediment layer
        sumsediment += sumwater * d
        amatrix -= water * d
        
        # are we doing a lot of work this iteration?
        alt = ((z+2) % 3 == its % 3 )
        if( alt ):
            print 'tick'

        # now the magical part: moving sediment and water around
        for x in range( 1, size - 1 ):
            
            for y in range( 1, size - 1 ):
				
                if( alt ):
                    x1 = amatrix[x-1][y]-amatrix[x][y]+water[x-1][y]-water[x][y]
                    x2 = amatrix[x][y-1]-amatrix[x][y]+water[x][y-1]-water[x][y]
                    x3 = amatrix[x][y+1]-amatrix[x][y]+water[x][y+1]-water[x][y]
                    x4 = amatrix[x+1][y]-amatrix[x][y]+water[x+1][y]-water[x][y]
                    
                    maxi = max( x1, x2, x3, x4 )
                    moveWater = maxi * maxrat
                    watercap = max( moveWater, watercap )
                    
                    if(maxi == x1):
                        water[x-1][y] -= moveWater
                        water[x][y] += moveWater
                    elif(maxi == x2):
                        water[x][y-1] -= moveWater
                        water[x][y] += moveWater
                    elif(maxi == x3):
                        water[x][y+1] -= moveWater
                        water[x][y] += moveWater
                    elif(maxi == x4):
                        water[x+1][y] -= moveWater
                        water[x][y] += moveWater

                x1 = amatrix[x-1][y-1]-amatrix[x][y]+water[x-1][y-1]-water[x][y]
                x2 = amatrix[x+1][y-1]-amatrix[x][y]+water[x+1][y-1]-water[x][y]
                x3 = amatrix[x-1][y+1]-amatrix[x][y]+water[x-1][y+1]-water[x][y]
                x4 = amatrix[x+1][y+1]-amatrix[x][y]+water[x+1][y+1]-water[x][y]
                
                maxi = max( x1, x2, x3, x4 )
                moveWater = maxi * maxrat
                watercap = max( moveWater, watercap )
                
                if(maxi == x1):
                    water[x-1][y-1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == x2):
                    water[x+1][y-1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == x3):
                    water[x-1][y+1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == x4):
                    water[x+1][y+1] -= moveWater
                    water[x][y] += moveWater


        print "Sediment Per Square:",sumsediment/size/size,", Water Per Square",sumwater/size/size

        water *= ( 1 - evap )
        sumwater *= ( 1 - evap )

        amatrix += water / sumwater * sumsediment * sed
        sumsediment *= ( 1 - sed )

        #scipy.misc.imsave("water_terrain_%d.png" % z, amatrix )
        #scipy.misc.imsave("water_water_%d.png" % z, water )
        #print "Max Water Transferred:", watercap
        #print "Terrain:",Stats_Range(amatrix)
        #print "Water:",Stats_Range(water)
        
    return amatrix



############################################################################
#
#  Map Filling Functions
#
############################################################################

#
# Generates p Varonoi cells
#
# must be followed immediatly with a blur
#
def Voronoi(amatrix,p,edge, step=4):
    
    points=zeros((p,2))
    size = int( amatrix.size ** ( 0.5 ) )
    for z in range( 0, p ):

        width = size / ( p ** 0.5 )
        x =  (z) * width
        y =  (z) / int( p ** 0.5 ) * width
        points[z][0] = int( random.uniform( x + edge, x + width - edge ) % size )
        points[z][1] = int( random.uniform( y + edge, y + width - edge ) % size )
        
        #print points[z][0],',',points[z][1]
        #amatrix[points[z][0]][points[z][1]]=10
    
    kd = scipy.spatial.KDTree(points)
    
    for x in range( 0, size, step ): # change step to 1 for accuracy
    
        #print 'row',x
        for y in range( 0, size, step ): # change step to 1 for accuracy
            
            close=kd.query([x,y],1)
            amatrix[x][y] = close[0]
            
    return amatrix


#
# Fills a matrix with random numbers
#

def Generate( amatrix, edge, average = 0.5 ):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( edge, size-edge ):

        for y in range( edge, size-edge ):

            amatrix[x][y] += random.triangular( 0.0, average * 100, 100.0 )
            #windows above, linux below. I have no idea why...
            #amatrix[x][y] += random.triangular( 0.0, 100.0, average * 100 )
    
    return amatrix


#
# Generate_New makes classy, rolling terrain, but has a really slow runtime
#
# Terrain Strength works well between 1.5 and 2.0, can vary from 1.2 to 4.0
# It affects how rolling the terrain will be
# 
# size determines the size of the resulting matrix. 1024 takes 11 seconds
#
def Generate_New(terrain_strength = 2.0, size = 1024, average = 0.2 ):

    a = zeros(( 4, 4 ))
    a = Generate( a, 0, average )
    gauss = int( math.log( size, 2 ) + 1 ) % 4
    
    for z in range( 0, int( math.log( size, 2 ) - 2 ) ):

        terrain_strength -= (terrain_strength-1)/3
        a = Matrix_Double(a) * terrain_strength
        a = Generate( a, 0, average )
        if ( z%4 == gauss ):

            a = Gaussian_Blur( a, 6 )

        #print 2 ** (z + 3)

    a = Matrix_Scale( a, 0, 100 )            
    return a


#
# Produces Cloud-looking maps at scale * 16 a side
#
def clouds(scale):

    #
    # Timekeeping
    #           
    wall = time.clock()
    wall2 = wall

    #
    # Large Boring Hills
    #
    a = zeros(( scale , scale ))
    Generate( a, 0, 0.05 )
    a = Matrix_Double( a )
    a = Matrix_Double( a )
    a = Gaussian_Blur( a, 2 )
    a = Matrix_Double( a )
    a = Matrix_Double( a )

    #print "Done Large Boring Hills",(time.clock()-wall)
    wall = time.clock()

    #
    # Little Boring Hills
    #
    b = zeros(( scale*4 , scale*4 ))
    Generate( b, 0, 0.05 )
    b = Matrix_Double( b )
    b = Gaussian_Blur( b, 2 )
    b = Matrix_Double( b )

    #print "Done Little Boring Hills",(time.clock()-wall)
    wall = time.clock()

    #
    # Extra Noise
    #
    c = zeros(( scale*16 , scale*16 ))
    Generate( c, 0, 0.05 )

    #print "Done Adding Noise",(time.clock()-wall)
    wall = time.clock()

    #
    # More Hills
    #
    d = zeros(( scale*16 , scale*16 ))
    Sparse_Hills_Basic(d , scale/2 , 20 )
    d = Gaussian_Blur( d, 32 )
    d = Matrix_Scale( d, 0, 100 )

    #print "Done Adding Hills",(time.clock()-wall)
    wall = time.clock()

    #
    # Finishing Up
    #
    k = 3 * a + 2 * b + c + 5 * d
    #scipy.misc.imsave( 'example1.png', Gaussian_Blur( k , 3 ) )
    
    Dome(k)
    k = Gaussian_Blur( k, 2 )
    k = Matrix_Scale( k, 0, 100 )

    #print "Done Blurring and Doming",(time.clock()-wall)
    wall = time.clock()

    imsave('terrain_section_%d.png' % (time.clock() * 100 ),k)
    print "Done Cloud",(time.clock()-wall2),'s'
    
    return k


#
# Uses a Queue to generate terrain thread-safely
# feeds into Rolling hills below
#
def Simple_Threaded_Terrain( size, q, average = 0.5 ):
    wall = time.clock()
    
    a = zeros(( size, size ))
    a = Sparse_Hills( a, size * size / 512, 32 )
    ##print "1"
    
    a = Gaussian_Blur( a, 9 )
    a = Matrix_Scale( a, 0, 700 )
    a = Generate( a, 0, average )
    
    ##print "2"
    
    #imsave( 'earliest.png', a)
    a=Matrix_Scale(a,0,40)
    
    # Enabling rivers here creates a frightening and disturbing effect of 'swiss-cheese'
    
    #b = Rivers( a, ( size / 2 )**2 )
    #b += Gaussian_Blur( b, 5 ) * 11.0
    #a += b / 10.0
    #Matrix_Crop( a, 0, 40 )
    ##print "3"
    
    #imsave( 'early.png', a)
    a = Terrain_Dome( a )
    ##print "Done in", ( time.clock() - wall )
    
    #imsave( '%d_final.png' % size, a )
    #pltt( '%d_final_mask.png' % size, a )
    #a = Matrix_Scale( a, 0, 100 )
    
    q.put(a)
    return a


#
# Rolling_Hills creates .b3.npy, and returns the same data. 
# it runs very slowly, but makes very nice terrain.
# do not screw with.
#
def Rolling_Hills():

    a = zeros(( 4096, 4096 ))
    
    q = Queue()
    jobs = []
    
    print 0
    
    for i in range(5):
        p = Process(target=Simple_Threaded_Terrain,args=(512,q,0.05,))
        jobs.append(p)
        p.start()
        print 10*i+5

    print "Length:",q
    c = q.get()
    print 50
    d = q.get()
    print 100
    e = q.get()
    print 150
    f = q.get()
    print 200
    g = q.get()

    for z in jobs:
        z.join()
    
    #c=Simple_Threaded_Terrain(512,q)
    #d=Simple_Threaded_Terrain(512,q)
    #e=Simple_Threaded_Terrain(512,q)
    #f=Simple_Threaded_Terrain(512,q)
    #g=Simple_Threaded_Terrain(512,q)
    print 250

    inc = 386
    # the size of the uncontested space in the center of each grid is inc**2
     
    inc2 = 0
    # gradually growing incrementer which causes a rhomboid shape

    for x in range( 511, 3073, inc - inc2 ):
        
        inc2 = 0
        print x
        for y in range( 511, 3073, inc ):
        
            x += 25
            inc2 += 30
            
            #print x,",",y
            a = Matrix_Merge( a, c, x, y )
            
            c = rot90(c)
            h = c
            c = d
            d = e
            e = f
            f = g
            g = h
    

    
    b = a [ 1024: 3072, 1024 : 3072 ]
    b = Matrix_Scale( b, 0, 40 )
    print 3000

    b += 10 * Gaussian_Blur( Matrix_Double(Matrix_Double(Matrix_Double(Generate_New( 2.0, 256, 0.05 )))), 5 )
    b = Matrix_Scale( b, 0, 40 )
    print 4000

    save( '.b3.npy', b )
    return b


