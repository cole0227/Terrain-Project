from numpy import *
import pylab
import scipy
import scipy.misc

import random
import thread
import time
import multiprocessing

import hills
from functions import *
import simplextextures




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
    amatrix[x+2*Spider_X(left )][y+2*Spider_Y(left )] += height / 3
    amatrix[x+2*Spider_X(right)][y+2*Spider_Y(right)] += height / 3
    amatrix[x+3*Spider_X(left )][y+3*Spider_Y(left )] += height / 5
    amatrix[x+3*Spider_X(right)][y+3*Spider_Y(right)] += height / 5

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
def Spider_Mountain_Wrapper( amatrix, x, y, height = 100, f = 0.91, togo = 45 ):

    amatrix[x][y] -= height * 3
    Spider_Mountain(amatrix, x  , y  , height, random.randint(0,1), f, togo)
    Spider_Mountain(amatrix, x  , y, height, random.randint(2,3), f, togo)
    Spider_Mountain(amatrix, x, y, height, random.randint(4,5), f, togo)
    Spider_Mountain(amatrix, x, y  , height, random.randint(6,7), f, togo)

def Spider_Mountains( amatrix, number, height, f, togo ):

    size = int( amatrix.size ** ( 0.5 ) )
    for num in range( 0, number ):
    
        print num,"of",number
        Spider_Mountain_Wrapper( amatrix, random.randint( size / 8, size * 7 / 8 ),random.randint( size / 8, size * 7 / 8 ), height, f, togo )



wall = time.clock()

a = zeros(( 472, 472 ))
Spider_Mountains( a, 50, 20, 0.91, 45 )
scipy.misc.imsave( "Earliest.png", a )
c = (a + Gaussian_Blur( a,6 ) * 10 + Gaussian_Blur( a,3 ) * 10)


print "Time to Generate:", (time.clock()-wall)
wall = time.clock()

scipy.misc.imsave( "Early.png", c )
d = Erosion_Water( c, 5 )
scipy.misc.imsave( "Fail1.png", d )
e = d + a
scipy.misc.imsave( "Fail2.png", e )


print "Time to erode:", (time.clock()-wall)

