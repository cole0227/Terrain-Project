from numpy import *
from math import log

import pylab
import scipy
import scipy.spatial
import random
import time

from functions import *

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



def main( size ):
    wall = time.clock()
    
    a = zeros(( size, size ))
    a = Sparse_Hills( a, size * size / 512, 32 )
    ##print "1"
    
    a = Gaussian_Blur( a, 9 )
    a = Matrix_Scale( a, 0, 700 )
    a = Generate( a, 0 )
    
    ##print "2"
    
    #scipy.misc.imsave( 'earliest.png', a)
    a=Matrix_Scale(a,0,40)
    
    # Enabling rivers here creates a frightening and disturbing effect of 'swiss-cheese'
    
    #b = Rivers( a, ( size / 2 )**2 )
    #b += Gaussian_Blur( b, 5 ) * 11.0
    #a += b / 10.0
    #Matrix_Crop( a, 0, 40 )
    ##print "3"
    
    #scipy.misc.imsave( 'early.png', a)
    a = Terrain_Dome( a )
    ##print "Done in", ( time.clock() - wall )
    
    #scipy.misc.imsave( '%d_final.png' % size, a )
    #pltt( '%d_final_mask.png' % size, a )
    a = Matrix_Scale( a, 0, 100 )            
    return a

#
# Terrain Strength works well between 1.8 and 2.2, can vary from 1.2 to 4.0
# It affects how rolling the terrain will be
# 
# size determines the size of the resulting matrix. 1024 takes 19 seconds
#
def new(terrain_strength, size):
    wall = time.clock()

    a = zeros(( 4, 4 ))
    a = Generate( a, 0 )
    for z in range( 0, int( math.log( size, 2 ) - 2 ) ):

        #print z
        a = Matrix_Double(a) * terrain_strength
        a = Generate( a, 0 )
        if ( z%3 == 1 ):

            a = Gaussian_Blur( a, 7 )

    a = Matrix_Scale( a, 0, 100 )            
    return a


def comp1():
    #a = Matrix_Double(new( 2.1, 1024 )) * 1.3
    a = zeros(( 2048, 2048 ))
    c = main(256)
    d = main(256)
    e = main(256)
    f = main(256)
    g = main(256)
    print 0

    inc = 182
    inc2 = 0

    for x in range( 255, 1537, inc - inc2 ):
        
        inc2 = 0
        print x
        for y in range( 255, 1537, inc ):
        
            x += 25
            inc2 += 25
            
            #print x,",",y
            a = Matrix_Merge( a, c, x, y )
            c = rot90(c)
            h = c
            c = d
            d = e
            e = f
            f = g
            g = h
    

    
    b = a [ 512: 1536, 512 : 1536 ]
    b = Matrix_Scale( b, 0, 40 )
    scipy.misc.imsave( 'earliest.png', b)
    save( 'b.npy', b )
    print 2000


def comp2():
    b = load( 'b.npy' )
    b += (Elevation_Selection( b, 20, 40, 0, 40 ) - 20) * 0.1
    b += (Elevation_Selection( b, 30, 45, 0, 45 ) - 30) * 0.1
    b += (Elevation_Selection( b, 35, 50, 0, 50 ) - 35) * 0.15
    b = Matrix_Scale( b, 0, 40 )
    scipy.misc.imsave( 'early.png', b)
    c = Elevation_Selection( b, -7, 14, 0, 0 )
    c = Gaussian_Blur( c, 5 )
    b -= c * 0.3
    c = Elevation_Selection( b, -7, 8, 0, 0 )
    c = Gaussian_Blur( c, 5 )
    b -= c * 0.3
    save( 'b2.npy', b )
    print 2500


def comp3():
    b = load( 'b2.npy' )
    b = Matrix_Scale( b, 0, 40 )
    #print Stats_Percentile( b )
    c = Elevation_Selection( b, -7, 3, 0, 0 )
    c = Gaussian_Blur( c, 5 )
    b -= c * 0.3
    b = Matrix_Scale( b, 0, 50 )             # Playing with this. 110 is normal, 50 is weird
    scipy.misc.imsave( 'fatal.png', b)
    b += Gaussian_Blur( Matrix_Double(Matrix_Double(new( 2.1, 256 ))), 5 )
    b = Matrix_Scale( b, 0, 40 )
    scipy.misc.imsave( 'fin.png', b)
    save( 'b3.npy', b )
    print 3000


def comp4():
    b = load( 'b3.npy' )
    
    scipy.misc.imsave( 'final.png', b)
    pltt( 'final_mask.png', b )

#main(64)
#main(128)
#main(256)
#main(512)
comp1()
comp2()
comp3()
comp4()
