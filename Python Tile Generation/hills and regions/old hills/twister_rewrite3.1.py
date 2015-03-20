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
def Dome(amatrix):

    size = int( amatrix.size ** ( 0.5 ) )
    effect = 0
    for x in range( 0, size ):
    
        for y in range( 0, size ):
        
            distance = sqrt( 2.0 ) / size * sqrt(
            
                ( x - ( size - 0.7 ) / 2 ) ** 2 +
                ( y - ( size - 0.7 ) / 2 ) ** 2 )
            
            effect -= amatrix[x][y]
            amatrix[x][y] /= max( distance, 0.43 )
            amatrix[x][y] /= max( distance, 0.48 ) * 3
            amatrix[x][y] /= max( distance, 0.53 ) * 6
            amatrix[x][y] /= max( distance, 0.58 ) * 6
            
            #amatrix[x][y] += 2 / max( min( distance, 0.45 ), 0.25 )
            #amatrix[x][y] += 2 / max( min( distance, 0.35 ), 0.20 )
            
            #if( amatrix[x][y] < 55 and distance < 0.3 ):
            #    amatrix[x][y] = 55
            #    effect += 1
            
            effect += amatrix[x][y]
    
    #print 1.0 * effect/size/size
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
# Thermally erode a single tile
#
def Erosion_Thermal_Helper( amatrix, x, y, t, cap, mult ):

    size = int( amatrix.size ** ( 0.5 ) )

    x1 = ( x - 1 ) % size
    x2 = ( x + 1 ) % size
    y1 = ( y - 1 ) % size
    y2 = ( y + 1 ) % size
    
    capav = ( ( cap - amatrix[x][y] ) / cap ) ** mult
    d1 = ( amatrix[x][y] - amatrix[x1][y1] ) * capav
    d2 = ( amatrix[x][y] - amatrix[x2][y2] ) * capav
    d3 = ( amatrix[x][y] - amatrix[x2][y1] ) * capav
    d4 = ( amatrix[x][y] - amatrix[x1][y2] ) * capav
    
    dmax = max( d1, d2, d3, d4, 0 )
    
    if(d1 == dmax):
        amatrix[x][y] -= t * dmax
        amatrix[x1][y1] += t * dmax
    elif(d2 == dmax):
        amatrix[x][y] -= t * dmax
        amatrix[x2][y2] += t * dmax
    elif(d3 == dmax):
        amatrix[x][y] -= t * dmax
        amatrix[x2][y1] += t * dmax
    elif(d4 == dmax):
        amatrix[x][y] -= t * dmax
        amatrix[x1][y2] += t * dmax
    

#
# Erodes thermally
#
def Erosion_Thermal( amatrix, t, cap, mult ):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( 0, size ):
        
        #scipy.misc.imsave( 'map_16_mono_erode_%d.png' % x, amatrix )
    
        for y in range( 0, size ):
        
            Erosion_Thermal_Helper( amatrix, x, y, t, cap, mult )
    
    return amatrix
        
                
#
# Square Diamond Method
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
                #if( x == 0 or y == 0 or x == size-1 or y == size-1):
                #    amatrix[x][y] = -size
            
        for x in range( 0, size, step/2 ):
            
            for y in range( ( x + step / 2 ) % step , size, step ):

                    
                amatrix[x][y] = ( 
                    amatrix[( x - step / 2 ) % ( size - 1 ) ][y] +
                    amatrix[( x + step / 2 ) % ( size - 1 ) ][y] +
                    amatrix[x][( y - step / 2 ) % ( size - 1 ) ] +
                    amatrix[x][( y + step / 2 ) % ( size - 1 ) ] ) / 4

                    
                amatrix[x][y] += random.uniform( -step, step )

                #The following is a hack for dark edges
                #if( x == 0 or y == 0 or x == size-1 or y == size-1):
                #    amatrix[x][y] = -size
                
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
    
    for x in range( 0, size, 2 ):
    
        #print 'row',x
        for y in range( 0, size, 2 ):
            
            close=kd.query([x,y],1)
            amatrix[x][y] = close[0]


#
# Water-based Erosion takes place in four phases
# 1. Adding new water
# 2. Water eroding the rock
# 3. Water transporting itself and the sediment
# 4. Water evaporates
# 5. depositing sediment
#
def Erosion_Water( amatrix, its, r, s, e):

    size = int( amatrix.size ** ( 0.5 ) )
    water = zeros((size,size))
    
    sumsediment = 0
    sumwater = 0

    for z in range( 0, its ):
    
        sumwater += size * size * r
        water += r
        amatrix -= s * water
        for x in range( 0, size ):
        
            #print z, x, sumsediment
            #scipy.misc.imsave( 'water_%d_%d.png' % (z,x), water )
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
                diffmax = max( diff11, diff12, diff21, diff22, 0 )
                if(diff11==diffmax):
                    
                    water[x][y]-=diffmax/2
                    water[x1][y1]+=diffmax/2

                elif(diff12==diffmax):
                    
                    water[x][y]-=diffmax/2
                    water[x1][y2]+=diffmax/2

                elif(diff21==diffmax):
                    
                    water[x][y]-=diffmax/2
                    water[x2][y1]+=diffmax/2

                elif(diff22==diffmax):
                    
                    water[x][y]-=diffmax/2
                    water[x2][y2]+=diffmax/2


        amatrix += water * sumsediment / sumwater
        sumsediment = 0
        sumwater /= e
        water /= e
    #scipy.misc.imsave( 'water.png', water )


#
# Main function
#
def main(scale):

    #random.seed(4)

    #
    # Timekeeping
    #           
    wall = time.clock()
    wall2 = wall

    a = zeros((scale+1,scale+1))
    Midpoint_Displacement(a)
    a = a[0:scale,0:scale]

    print "Done Basic Noise", ( time.clock() - wall )
    wall = time.clock()

    b = zeros((scale,scale))
    Voronoi(b,scale/4,scale/128)
    b=Gaussian_Blur(b,scale/32)
    b=Matrix_Scale(b,0,100)

    print "Done Voronoi", ( time.clock() - wall )
    wall = time.clock()
    
    a = Matrix_Scale(a,-20,100)
    Matrix_Crop(a,0,100)
    c = a - b / 2
    c=Matrix_Scale(c,0,100)
    Dome(c)

    print "Done Doming", ( time.clock() - wall )
    wall = time.clock()
    
    c = Matrix_Scale( c, 0, 20 )
    d = Elevation_Selection( c, 15, 20, 15, 20) - 15
    c += d * 0.7
    d = Elevation_Selection( c, 11, 20, 11, 20) - 11
    c += d * 0.7

    print "Done Mountains and valleys", ( time.clock() - wall )
    wall = time.clock()
    
    d = Slope_Field(c)
    d = Slope_Field(d)
    c += d * 1.5
    d = Elevation_Selection( c, 7, 11, 7, 7 ) - 7
    d = Gaussian_Blur( d, 4)
    c -= d * 0.5
    d = Elevation_Selection( c, 3.5, 9, 3.5, 3.5 ) - 3.5
    d = Gaussian_Blur( d, 4)
    c += d * 0.2

    print "Done Slopes", ( time.clock() - wall )
    wall = time.clock()
    
    scipy.misc.imsave( 'map_%d_early1.png' % ( scale ), c )
    c = Matrix_Scale( c, 0, 200 )
    Erosion_Water( c, 3, 10, 0.5, 0.3 )
    c = Matrix_Scale( c, 0, 7 )
    scipy.misc.imsave( 'map_%d_early2.png' % ( scale ), c )
    for x in range(0,3):
        c = Erosion_Thermal(c,0.6,10,2)
    #c = Matrix_Scale( c, 0, 150 )
    #Matrix_Crop(c,0,100)

    
    print "Done Erosion", ( time.clock() - wall )
    wall = time.clock()
    
    scipy.misc.imsave( 'map_%d_final.png' % ( scale ), c )
    #save( 'map_%d.npy' % ( scale ), c )

    fig = plt.figure()    
    fig.set_size_inches( scale * 5.1615 / 16 , scale * 5.1615 / 16 )
    plt.imshow( c )
    fig.savefig(
        'map_%d_mask.png' % ( scale ), 
        bbox_inches = 'tight', pad_inches = 0, dpi = 4 )
        

    print "Done Everything",( time.clock() - wall2 )
    print "-------------------------"
    
    return c

#main(64)
#main(128)
#main(256)
main(512)
main(1024)
#main(2048)
