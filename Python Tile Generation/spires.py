import random
import thread
import time

from numpy import *
import pylab
import scipy
import scipy.misc

from functions import *


def Sparse_Mount( amatrix, x, y, height = 100 ):

    amatrix[x][y] = height
    e = 4
    x += random.randint( -e , e )
    y += random.randint( -e , e )
    amatrix[x][y] = height * 0.7
    e /= 2
    x += random.randint( -e , e )
    y += random.randint( -e , e )
    amatrix[x][y] = height * 0.5
    x += random.randint( -e , e )
    y += random.randint( -e , e )
    amatrix[x][y] = height * 0.3
        
    return amatrix

def main1(size):
    wall = time.clock()

    a = zeros((size,size))
    
    #a = clouds(size/16)
    
    Sparse_Hills(a, size*size/1000, 50)

    #a =+ Gaussian_Blur( a, 2 ) * 2

    print Stats_Range(Slope_Field(a))
    scipy.misc.imsave("Spires%d.png" % size, a )

    print "Done Random Spires",(time.clock()-wall)
    wall = time.clock()

    a = Erosion_Thermal( a, 3, 1 )
    scipy.misc.imsave("Spires%d_eroded.png" % size, a )

    print "Done Erosion",(time.clock()-wall)

def main2(size):
    wall = time.clock()

    a = zeros((size,size))
    b = zeros((size,size))    
    
    #a = clouds(size/16)
    
    for z in range (150):
        
        x = random.randint( 52, size - 52 )
        y = random.randint( 52, size - 52 )
        Spider_Mountain_Wrapper( b, x, y, 40)
        #Sparse_Mount( a, x, y, 100)
        
    #a =+ Gaussian_Blur( a, 2 ) * 2

    print Stats_Range(Slope_Field(a))
    scipy.misc.imsave("Spires%d.png" % size, a )

    print "Done Random Spires",(time.clock()-wall)
    wall = time.clock()

    a = Erosion_Thermal( a, 3, 5 )
    scipy.misc.imsave("Spires%d_eroded.png" % size, a )

    print "Done Erosion",(time.clock()-wall)

main2(384)
