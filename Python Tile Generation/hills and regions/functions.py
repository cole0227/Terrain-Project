import matplotlib.pyplot as plt
from numpy import *

import pylab
import scipy
import scipy.spatial
import random
import time
import sys

import hills

#
# Blurs quickly to the radius specified
#

def Gaussian_Blur( amatrix, radius ):

    size = int( amatrix.size ** ( 0.5 ) )
    kernel = hills.gaussian_kernel( size, size, radius )
    blur = hills.apply_kernel( size, size, amatrix, kernel )
    return blur


#
# Fills a matrix with random numbers
#

def Generate( amatrix, edge ):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( edge, size-edge ):

        for y in range( edge, size-edge ):

            amatrix[x][y] += random.triangular( 0.0, 100.0, 25.0 )
    
    return amatrix


#
# Generate_New makes classy, rolling terrain, but has a really slow runtime
#
# Terrain Strength works well between 1.8 and 2.2, can vary from 1.2 to 4.0
# It affects how rolling the terrain will be
# 
# size determines the size of the resulting matrix. 1024 takes 19 seconds
#
def Generate_New(terrain_strength, size):

    a = zeros(( 4, 4 ))
    a = Generate( a, 0 )
    for z in range( 0, int( math.log( size, 2 ) - 2 ) ):

        #print z
        a = Matrix_Double(a) * terrain_strength
        a = Generate( a, 0 )
        if ( z%3 == 0 ):

            a = Gaussian_Blur( a, 7 )

    a = Matrix_Scale( a, 0, 100 )            
    return a


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
        
            another[x/2][y/2]= amatrix[x][y] / 4.0 + amatrix[x+1][y] / 4.0 + amatrix[x][y+1] / 4.0 + amatrix[x+1][y+1] / 4.0
    
    return another

#
# Returns a matrix 1/8 the dimensions of the original
#
def Matrix_Tiny(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    another = zeros(( size/8, size/8 ))

    for x in range( 0, size, 8 ):
    
        for y in range( 0, size, 8 ):
        
            for x1 in range( 3, 5 ):
            
                for y1 in range( 3, 5 ):
                
                    another[x/8][y/8] += amatrix[x + x1][y + y1] / 4.0
    
    return another



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
def Matrix_Fromto(amatrix,start,end):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( 0, size ):
    
        for y in range( 0, size ):
    
            if(amatrix[x][y]==start):
                
                amatrix[x][y]=end
            
    
    return amatrix


#
# Slope Field Generator
#
def Slope_Field(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    slopes = zeros(( size, size ))
    for x in range( 1, size-1 ):
    
        for y in range( 1, size-1 ):
        
            slopes[x][y] = max(
               abs( amatrix[x][y] - amatrix[x  ][y+1] ),
               abs( amatrix[x][y] - amatrix[x  ][y-1] ),
               abs( amatrix[x][y] - amatrix[x+1][y  ] ),
               abs( amatrix[x][y] - amatrix[x-1][y  ] ) )
                
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
# Calculates the Standard Deviation, Devides it by the average height of the matrix
#
def Erosion_Score( amatrix ):

    standard = 0
    size = int( amatrix.size ** ( 0.5 ) )
    s = sum(amatrix)/size/size
    for x in range( 1, size-1 ):
    
        for y in range( 1, size-1 ):
        
            standard += ( amatrix[x][y] - s ) ** 2.0
    
    standard /= size * size
    standard = standard ** ( 0.5 ) / s
    return s


#
# plt output function
#
def pltt( stri, amatrix ):

    size = int( amatrix.size ** ( 0.5 ) )
    fig = plt.figure()    
    fig.set_size_inches( size * 0.32259375 , size * 0.32259375 )
    plt.imshow( amatrix )
    fig.savefig(
        stri, 
        bbox_inches = 'tight', pad_inches = 0, dpi = 4 )


#
# Thermally erode a single tile, aligned with the squares
#
def Erosion_Thermal_Helper( amatrix, x, y, t, m ):

    size = int( amatrix.size ** ( 0.5 ) )

    x1 = ( x - 1 ) % size
    x2 = ( x + 1 ) % size
    y1 = ( y - 1 ) % size
    y2 = ( y + 1 ) % size
    
    factor = (50-amatrix[x][y])/50
    d1 = ( amatrix[x][y] - amatrix[x1][y ] ) * factor
    d2 = ( amatrix[x][y] - amatrix[x2][y ] ) * factor
    d3 = ( amatrix[x][y] - amatrix[x ][y1] ) * factor
    d4 = ( amatrix[x][y] - amatrix[x ][y2] ) * factor
    
    dmax = max( d1, d2, d3, d4, m )
    
    if(d1 == dmax):
        amatrix[x ][y] -= t * dmax
        amatrix[x1][y] += t * dmax
    elif(d2 == dmax):
        amatrix[x ][y] -= t * dmax
        amatrix[x2][y] += t * dmax
    elif(d3 == dmax):
        amatrix[x][y ] -= t * dmax
        amatrix[x][y1] += t * dmax
    elif(d4 == dmax):
        amatrix[x][y ] -= t * dmax
        amatrix[x][y2] += t * dmax
    

#
# Erodes thermally
#
def Erosion_Thermal( amatrix, its, t, m ):

    for z in range( 0, its ):

        size = int( amatrix.size ** ( 0.5 ) )
        for x in range( 0, size ):
            
            #scipy.misc.imsave( 'map_16_mono_erode_%d.png' % x, amatrix )
        
            for y in range( 0, size ):
            
                if( amatrix[x][y] < 60 ):
                    
                    Erosion_Thermal_Helper( amatrix, x, y, t, m )
        
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
    
        #scipy.misc.imsave( 'map_16_progress_%d.png' % (size/step), amatrix )
        # this section 
        for x in range( 0, size-1, step ):
            
            for y in range( 0, size-1, step ):
                
                #print x,y,step
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
        
                
#
# Generates p Varonoi cells
#
def Voronoi(amatrix,p,edge):
    
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
    
    for x in range( 0, size, 4 ):
    
        #print 'row',x
        for y in range( 0, size, 4 ):
            
            close=kd.query([x,y],1)
            amatrix[x][y] = close[0]
            
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
        amatrix[x][y]=132
        e = edge / 2
        x += random.randint( -e , e )
        y += random.randint( -e , e )
        amatrix[x][y]=66
        e = e / 2
        x += random.randint( -e , e )
        y += random.randint( -e , e )
        amatrix[x][y]=44
        e = e / 2
        x += random.randint( -e , e )
        y += random.randint( -e , e )
        amatrix[x][y]=33
        
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
    

