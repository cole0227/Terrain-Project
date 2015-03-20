import matplotlib.pyplot as plt
from numpy import *

import pylab
import scipy
import scipy.spatial
import random
import time

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

            amatrix[x][y] = random.triangular( 0.0, 100.0, 5.0 )


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
# Lowers points far from the middle
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
            for z in range(44,61,4):
                amatrix[x][y] /= max( distance, z / 100.0 )
            
            #amatrix[x][y] += 2 / max( min( distance, 0.45 ), 0.25 )
            #amatrix[x][y] += 2 / max( min( distance, 0.35 ), 0.20 )
            #if( amatrix[x][y] < 55 and distance < 0.3 ):
            #    amatrix[x][y] = 55
            #    effect += 1
            
            effect += amatrix[x][y]
    
    #print 1.0 * effect/size/size
    print "Done Doming", ( time.clock() - wall )
    return Matrix_Scale( amatrix, 0, 100 )
    

#
# Adds sparse dots to a matrix
#
def Sparse_Hills( amatrix, number, edge ):

    size = int( amatrix.size ** ( 0.5 ) )
    for num in range( 0, number ):
        
        x = random.randint( edge, size - edge )
        y = random.randint( edge, size - edge )
        amatrix[x][y]=132
        x += random.randint( -20 , 20 )
        y += random.randint( -20 , 20 )
        amatrix[x][y]=66
        x += random.randint( -10 , 10 )
        y += random.randint( -10 , 10 )
        amatrix[x][y]=44
        x += random.randint( -5 , 5 )
        y += random.randint( -5 , 5 )
        amatrix[x][y]=33


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
# Water-based Erosion takes place in four phases
# 1. Adding new water
# 2. Water eroding the rock
# 3. Water transporting itself and the sediment
# 4. Water evaporates
# 5. depositing sediment
#
def Erosion_Water( amatrix, its, r, s, e, m):

    size = int( amatrix.size ** ( 0.5 ) )
    water = zeros((size,size))
    
    sumsediment = 0
    sumwater = 0

    for z in range( 0, its ):
    
        sumwater += size * size * r
        water += r
        amatrix -= s * water
        #scipy.misc.imsave( 'erode_%d.png' % (z), amatrix )
        count = 0
        for x in range( 0, size ):
        
            #print z, x, sumsediment
            for y in range( 0, size ):
            
                sumsediment += s * water[x][y]
                x1 = ( x - 1 ) % size
                x2 = ( x + 1 ) % size
                y1 = ( y - 1 ) % size
                y2 = ( y + 1 ) % size
                
                
                diff11 = amatrix[x][y] + water[x][y] - amatrix[x1][y1] - water[x1][y1]
                diff12 = amatrix[x][y] + water[x][y] - amatrix[x1][y2] - water[x1][y2]
                diff22 = amatrix[x][y] + water[x][y] - amatrix[x2][y2] - water[x2][y2]
                diff21 = amatrix[x][y] + water[x][y] - amatrix[x2][y1] - water[x2][y1]
                diffmax = max( diff11, diff12, diff21, diff22, m )
                if(m==diffmax):

                    count-=1
                
                elif(diff11==diffmax):
                    
                    water[x][y]-=diffmax/2
                    water[x1][y1]+=diffmax/2

                elif(diff12==diffmax):
                    
                    water[x][y]-=diffmax/2
                    water[x1][y2]+=diffmax/2

                elif(diff21==diffmax):
                    
                    water[x][y]-=diffmax/2
                    water[x2][y1]+=diffmax/2

                else:
                    
                    water[x][y]-=diffmax/2
                    water[x2][y2]+=diffmax/2
                    
                count+=1


        amatrix += water * sumsediment / sumwater
        #print "actions:",count
        #print "sediment:",sumsediment
        sumsediment = 0
        sumwater *= (1-e)
        water *= (1-e)
        #print "water:",sumwater
        
    #scipy.misc.imsave( 'water.png', water )


#
# Generates p Varonoi rivers
#
def Rivers(amatrix,p):
    
    points=zeros((p,2))
    size = int( amatrix.size ** ( 0.5 ) )
    rivers=zeros((size,size))
    for z in range( 0, p ):

        width = size / ( p ** 0.5 )
        x =  (z) * width
        y =  (z) / int( p ** 0.5 ) * width
        points[z][0] = int( random.uniform( x, x + width ) % size )
        points[z][1] = int( random.uniform( y, y + width ) % size )
    
    for z in range( 0, p ):
        
        river=zeros((size,size))
        x = points[z][0]
        y = points[z][1]
        for w in range( -51, 51 ):
                    
            x1 = ( x - 1 ) % size
            x2 = ( x + 1 ) % size
            y1 = ( y - 1 ) % size
            y2 = ( y + 1 ) % size
            
            d1 = ( amatrix[x][y] - amatrix[x1][y ] ) * 1.37
            d2 = ( amatrix[x][y] - amatrix[x2][y ] ) * 1.37
            d3 = ( amatrix[x][y] - amatrix[x ][y1] ) * 1.37
            d4 = ( amatrix[x][y] - amatrix[x ][y2] ) * 1.37
            d5 = ( amatrix[x][y] - amatrix[x1][y2] )
            d6 = ( amatrix[x][y] - amatrix[x2][y1] )
            d7 = ( amatrix[x][y] - amatrix[x1][y1] )
            d8 = ( amatrix[x][y] - amatrix[x2][y2] )
            
            dmax = max( d1, d2, d3, d4, d5, d6, d7, d8, 0 )
            
            rivers[x][y] += ( abs(w)-51 ) * dmax *  amatrix[x][y]
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
                #rivers[x1][y2] = -50
                #rivers[x2][y1] = -50
                #rivers[x1][y1] = -50
                #rivers[x2][y2] = -50
                if ( w > -40 ):
                    rivers+=river
                break
    rivers = rivers/15 + Gaussian_Blur(rivers,3)
    amatrix+= rivers / 80.0
    #scipy.misc.imsave( 'final_rivers_%d.png' % (z**(1.0/2)), rivers )


#
# First Step of the new main setup
#
def Terrain_Basic(size):
    
    wall = time.clock()
    a = zeros((size+1,size+1))
    Midpoint_Displacement(a)
    a = a[0:size,0:size]

    print "Done Basic Noise", ( time.clock() - wall )
    wall = time.clock()

    b = zeros((size,size))
    Voronoi(b,size/4,size/128)
    b=Gaussian_Blur(b,size/32)
    b=Matrix_Scale(b,0,100)
    a = Matrix_Scale(a,-20,100)
    Matrix_Crop(a,0,100)
    c = a - b * 2
    c=Matrix_Scale(c,0,100)

    print "Done Voronoi Noise", ( time.clock() - wall )
    wall = time.clock()
    
    return c


#
# Third step, where we make the terrain more suitable for use
#
def Terrain_Mod(amatrix):

    wall = time.clock()

    c = amatrix    
    c = Matrix_Scale( c, 0, 20 )
    d = Elevation_Selection( c, 15, 20, 15, 20) - 15
    c += d * 0.7
    d = Elevation_Selection( c, 11, 20, 11, 20) - 11
    c += d * 0.7
    d = Elevation_Selection( c, 3.3, 9, 3.3, 3.3 ) - 3.3
    d = Gaussian_Blur( d, 4)
    c += d * 0.2
    d = Elevation_Selection( c, 9, 13, 9, 9 ) - 9
    d = Gaussian_Blur( d, 7)
    c -= d * 0.4

    print "Done Mountains and valleys", ( time.clock() - wall )
    wall = time.clock()
    
    return c


def Terrain_Erode(a):

    wall = time.clock()
    size = int( a.size ** ( 0.5 ) )
    a = Matrix_Scale( a, 0, 50 )
    #Erosion_Water( a, 20, 3, 1, 0, 0 ) # tweaked for 0-7
    a = Erosion_Thermal( a, 17, 0.5, 50.0 / size )
    #a = Gaussian_Blur( a, 2 )
    print "Done Erosion", ( time.clock() - wall )
    return a


def Terrain_Erode_More(a):

    wall = time.clock()
    size = int( a.size ** ( 0.5 ) )
    a=Matrix_Scale(a,0,50)
    maximum = min( size / 10 + 10, size / 15 + 14, size / 23 + 26 )
    for x in range( 10, maximum):
        Rivers( a, x**2 )
    Matrix_Crop(a,1,50)
    print "Done More Erosion", ( time.clock() - wall )
    return a    


def Terrain_Flattening(a):

    wall = time.clock()
    size = int( a.size ** ( 0.5 ) )
    a = Matrix_Scale(a,0,50)
    b = Elevation_Selection( a, 0, 6, 0, 0 )
    b = Gaussian_Blur( b, 11)
    a -= b * 0.5
    b = Elevation_Selection( a, 6, 16, 6, 6 ) - 6
    b = Gaussian_Blur( b, 13)
    a += b * 0.8
    b = Elevation_Selection( a, 14, 18, 14, 14 ) - 14
    b = Gaussian_Blur( b, 7)
    a += b * 0.5
    b = Elevation_Selection( a, 20, 26, 20, 20 ) - 20
    b = Gaussian_Blur( b, 5)
    a -= b * 0.8
    b = -Matrix_Crop( Elevation_Selection( a, 6, 15, 16, 16 ), 15, 16 ) + 16
    #a = a + 14 - Elevation_Selection( a, 14, 20, 0, 0 ) a clever trick, but alas, no cigar
    b = Gaussian_Blur( b, 5) 
    c = Voronoi( zeros(( size, size )), size/4, size/128 )
    c = -Gaussian_Blur( c, 5) 
    b *= Matrix_Scale( c, 0, 4 )
    a += b
    #print Stats_Percentile(a)
    c = rot90(fliplr(c))
    low = 18
    high = low+1
    b = -Matrix_Crop( Elevation_Selection( a, 13, low, high, high ), low, high ) + high
    b = Gaussian_Blur( b, 5) 
    b *= Matrix_Scale( c, 0, 4 )
    a += b
    #print Stats_Percentile(a)
    a = Erosion_Thermal( a, 2, 0.5, 40.0 / size )
    print "Terrain_Flattening", ( time.clock() - wall )
    return a    


def main( size):
    a=Terrain_Basic( size )
    scipy.misc.imsave( 'earliest.png', a )
    a=Terrain_Dome( a )
    scipy.misc.imsave( 'early.png', a )
    a=Terrain_Mod( a )
    scipy.misc.imsave( 'edited.png', a )
    save( 'edited.npy', a )
    a = Terrain_Erode( a )
    save('eroded.npy', a )
    scipy.misc.imsave( 'eroded.png', a )
    a = Terrain_Erode_More( a ) + 50
    save( 'erodedmore.npy', a )
    #a = load( 'erodedmore.npy' )
    a += load('eroded.npy') * 0.5
    scipy.misc.imsave( 'erodedmore.png', a )
    a = Terrain_Flattening( a )
    save( 'final_%d.npy' % size, a )
    #a = load( 'final_%d.npy' % size )
    scipy.misc.imsave( 'final_%d.png' % size, a )
    pltt( 'final_%d_mask.png' % size, a )

main(256)

#a = load('final_512.npy')
#a = Matrix_Merge( a, load('final_256.npy'), 128, 128 )
#a = Matrix_Merge( a, rot90(rot90(flipud(load('final_256.npy')))), 200, 10 )
#a = Matrix_Merge( a, fliplr(rot90(load('final_256.npy'))), 30, 230 )
#main(256)
#a = Matrix_Merge( a, load('final_256.npy'), 200, 250 )
#a = Matrix_Merge( a, fliplr(rot90(load('final_256.npy'))), 30, 30 )
#scipy.misc.imsave( 'final_516.png', a )
#pltt( 'finalmask_516.png', a )
