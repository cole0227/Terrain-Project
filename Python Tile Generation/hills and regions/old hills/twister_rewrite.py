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

    mymatrix = amatrix.reshape(-1)
    sort = mymatrix.argsort()
    final = [mymatrix[sort[0]], mymatrix[sort[amatrix.size-1]]]
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
    effect = 0;
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
            amatrix[x][y] += 3 / max( min( distance, 0.40 ), 0.25 )
            amatrix[x][y] += 3 / max( min( distance, 0.35 ), 0.20 )
            effect += amatrix[x][y]
    
    print effect/size/size
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
    print Stats_Range(d)
    d = Matrix_Scale( d, 0, 150 )
    Matrix_Crop(d,0,100)


    print "Done Adding Hills", ( time.clock() - wall )
    wall = time.clock()


    #
    # Doming and Blurring
    #
    k = 3 * a + 2 * b + c + 2 * d
    k = Dome(k)
    Matrix_Crop(k,15,85)
    k = Gaussian_Blur( k, 3 )

    print "Done Blurring and Doming", ( time.clock() - wall )
    wall = time.clock()
    
    
    #
    # Finishing Up
    #
    fig = plt.figure()    
    plt.imshow( k )
    fig.set_size_inches( scale * 5.1615 , scale * 5.1615 )
    fig.savefig(
        'map_%d_colour.png' % scale, 
        bbox_inches='tight', 
        pad_inches=0,
        dpi=4)

    scipy.misc.imsave( 'map_%d_mono.png' % scale, k )
    print "Done Everything",( time.clock() - wall2 )
    print "-------------------------"


main(16)
main(32)

