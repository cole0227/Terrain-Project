import matplotlib.pyplot as plt
from numpy import *

import pylab
import scipy
import scipy.spatial
import random
import time

import hills
from functions import *


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
# Second Step: Lowers points far from the middle
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
            for z in range( 44, 61, 4 ):
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
main(512)

a = load('final_512.npy')
a = Matrix_Merge( a, load('final_256.npy'), 128, 128 )
a = Matrix_Merge( a, rot90(rot90(flipud(load('final_256.npy')))), 200, 10 )
a = Matrix_Merge( a, fliplr(rot90(load('final_256.npy'))), 30, 230 )
main(256)
a = Matrix_Merge( a, load('final_256.npy'), 200, 250 )
a = Matrix_Merge( a, fliplr(rot90(load('final_256.npy'))), 30, 30 )
scipy.misc.imsave( 'final_516.png', a )
pltt( 'finalmask_516.png', a )
