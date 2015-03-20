import matplotlib.pyplot as plt
from numpy import *

import pylab
import scipy
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
            
            #effect -= amatrix[x][y]
            amatrix[x][y] /= max( distance, 0.40 )
            amatrix[x][y] /= max( distance, 0.45 ) * 3
            amatrix[x][y] /= max( distance, 0.50 ) * 6
            amatrix[x][y] /= max( distance, 0.55 ) * 6
            
            amatrix[x][y] += 3 / max( min( distance, 0.45 ), 0.25 )
            amatrix[x][y] += 3 / max( min( distance, 0.35 ), 0.20 )
            
            if( amatrix[x][y] < 55 and distance < 0.3 ):
                amatrix[x][y] = 55
                effect += 1
            
            #effect += amatrix[x][y]
    
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
                abs(amatrix[x][y]-amatrix[x  ][y+1]),
                abs(amatrix[x][y]-amatrix[x  ][y-1]),
                abs(amatrix[x][y]-amatrix[x+1][y  ]),
                abs(amatrix[x][y]-amatrix[x-1][y  ]))
                
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
def Erosion_Thermal_Helper( amatrix, x, y, t ):

    size = int( amatrix.size ** ( 0.5 ) )

    x1 = ( x - 1 ) % size
    x2 = ( x + 1 ) % size
    y1 = ( y - 1 ) % size
    y2 = ( y + 1 ) % size
    
    d1 = ( amatrix[x][y] - amatrix[x1][y1] )
    d2 = ( amatrix[x][y] - amatrix[x2][y2] )
    d3 = ( amatrix[x][y] - amatrix[x2][y1] )
    d4 = ( amatrix[x][y] - amatrix[x1][y2] )
    
    dmax = max( d1, d2, d3, d4, 0 )
    
    if(d1 == dmax):
        amatrix[x][y] -= 0.5 * dmax
        amatrix[x1][y1] += 0.5 * dmax
    elif(d2 == dmax):
        amatrix[x][y] -= 0.5 * dmax
        amatrix[x2][y2] += 0.5 * dmax
    elif(d3 == dmax):
        amatrix[x][y] -= 0.5 * dmax
        amatrix[x2][y1] += 0.5 * dmax
    elif(d4 == dmax):
        amatrix[x][y] -= 0.5 * dmax
        amatrix[x1][y2] += 0.5 * dmax
    

#
# Erodes thermally
#
def Erosion_Thermal( amatrix, t ):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( 0, size ):
        
        #scipy.misc.imsave( 'map_16_mono_erode_%d.png' % x, amatrix )
    
        for y in range( 0, size ):
        
            Erosion_Thermal_Helper( amatrix, x, y, t)
    
    return amatrix


#
# Square Diamond Method
#
def Square( amatrix ):

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
            
        for x in range( 0, size, step/2 ):
            
            for y in range( ( x + step / 2 ) % step , size, step ):

                    
                amatrix[x][y] = ( 
                    amatrix[( x - step / 2 ) % ( size - 1 ) ][y] +
                    amatrix[( x + step / 2 ) % ( size - 1 ) ][y] +
                    amatrix[x][( y - step / 2 ) % ( size - 1 ) ] +
                    amatrix[x][( y + step / 2 ) % ( size - 1 ) ] ) / 4

                    
                amatrix[x][y] += random.uniform( -step, step )
                
                if( x == 0 ):
                    amatrix[size-1][y] = random.uniform( -step, step )

                if( x == 0 ):
                    amatrix[x][size-1] = random.uniform( -step, step )

        step /= 2
        
                
#
# Generates p Varonoi cells
#
def Voronoi(amatrix,p):
    
    points=zeros((p,2))
    size = int( amatrix.size ** ( 0.5 ) )
    for z in range( 0, p ):

        width = size / ( p ** 0.5 )
        x =  (z) * width
        y =  (z) / int( p ** 0.5 ) * width
        points[z][0] = int( random.uniform( x, x + width ) % size )
        points[z][1] = int( random.uniform( y, y + width ) % size )
        
        #print points[z][0],',',points[z][1]
        #amatrix[points[z][0]][points[z][1]]=10
    
    for x in range( 0, size ):
    
        for y in range( 0, size ):
            
            close = size**2
            
            for z in range( 0, p ):
            
                close = min( close, ( points[z][0] - x ) ** 2 + ( points[z][1] - y ) ** 2)
                
            amatrix[x][y] = sqrt(close)



#
# Main function
#
def main(scale):

    #
    # Timekeeping
    #           
    wall = time.clock()
    wall2 = wall


    #
    # Large Boring Hills
    #
    a = zeros(( scale , scale ))
    Generate( a, 1 )
    a = Matrix_Double( a )
    a = Matrix_Double( a )
    a = Gaussian_Blur( a, 2 )
    a = Matrix_Double( a )
    a = Matrix_Double( a )

    print "Done Large Boring Hills", ( time.clock() - wall )
    wall = time.clock()


    #
    # Little Boring Hills
    #
    b = zeros(( scale*4 , scale*4 ))
    Generate( b, 3 )
    b = Matrix_Double( b )
    b = Gaussian_Blur( b, 2 )
    b = Matrix_Double( b )

    print "Done Little Boring Hills", ( time.clock() - wall )
    wall = time.clock()


    #
    # Extra Noise
    #
    c = zeros(( scale * 16 , scale * 16 ))
    Generate( c, 11 )

    print "Done Adding Noise", ( time.clock() - wall )
    wall = time.clock()


    #
    # More Hills
    #
    d = zeros(( scale * 16, scale * 16 ))
    Sparse_Hills(d, scale * scale / 16, 36)
    d = Gaussian_Blur( d, 12 )
    d = Matrix_Scale( d, 0, 150 )
    Matrix_Crop(d,0,100)


    print "Done Adding Hills", ( time.clock() - wall )
    wall = time.clock()


    #
    # Doming and Blurring
    #
    k = 3 * a + 2 * b + c + 2 * d
    k = Dome(k)
    Matrix_Crop(k,20,90)
    #k = Gaussian_Blur( k, 3 )
    #print "k=", Stats_Range(k)
    
    f = Elevation_Selection( k, 30, 48, 30, 30 ) - 30
    f = Gaussian_Blur( f, 5 )

    #print "k=", Stats_Percentile(k)
    #print "f=", Stats_Percentile(f)
    #scipy.misc.imsave( 'map_%d_mono_pre.png' % ( scale ), k )
    #scipy.misc.imsave( 'map_%d_f.png' % ( scale ), f )

    k += f*2/3    
    k = Gaussian_Blur( k, 3 )

    print "Done Blurring and Doming", ( time.clock() - wall )
    wall = time.clock()
    

    #
    # Erosion
    #
    #scipy.misc.imsave( 'map_%d_pre.png' % ( scale ), Gaussian_Blur( k, 2 ) )
    #print "Erosion Score:", Erosion_Score( Slope_Field( Gaussian_Blur( k, 2 ) ) )

    #print "k=", Stats_Range(k)
    #for x in range( 0, 10 ):    

    #    k = Erosion_Thermal( k, 23.0 / scale )

    #k = Gaussian_Blur( k, 3 )

    #print "Done Erosion", ( time.clock() - wall )
    #wall = time.clock()


    #
    # Texture Map Generation
    #
    e = Slope_Field(k)
    #print "Erosion Score:", Erosion_Score( e )
    e += 3 * Slope_Field(e) + ( k - 20 ) / 10
    Matrix_Scale( e, 0, 10 )
    f = Elevation_Selection( e, 2.5, 4.2, 0, 0 )
    f = Gaussian_Blur( f, 7 )
    #scipy.misc.imsave( 'map_%d_f.png' % ( scale ), f )
    e -= f / 2
    
    #print "e=", Stats_Range(e)
    Matrix_Scale( e, 0, 10 )
    f = Elevation_Selection( e, 0, 0.8, 0, 0.8 )
    Matrix_Scale(f, 0, 10 )
    f = 10 - f
    #scipy.misc.imsave( 'map_%d_ff.png' % ( scale ), f )
    #print "e=", Stats_Percentile(e)
    e += f*6
    e = Gaussian_Blur( e, 2 )
    #print "e=", Stats_Percentile(e)
    
    
    print "Done Texture Map", ( time.clock() - wall )
    wall = time.clock()
    
    
    #
    # Finishing Up
    #
    scipy.misc.imsave( 'map_%d_mono.png' % ( scale ), k )
    save( 'map_%d.npy' % ( scale ), k )

    fig = plt.figure()    
    fig.set_size_inches( scale * 5.1615 , scale * 5.1615 )

    #plt.imshow( k )
    #fig.savefig(
    #    'map_%d_color.png' % ( scale ), 
    #    bbox_inches = 'tight', pad_inches = 0, dpi = 4 )

    plt.imshow( e )
    fig.savefig(
        'map_%d_mask.png' % ( scale ), 
        bbox_inches = 'tight', pad_inches = 0, dpi = 4 )
        

    print "Done Everything",( time.clock() - wall2 )
    print "-------------------------"

main(16)
#main(24)
#main(32)

