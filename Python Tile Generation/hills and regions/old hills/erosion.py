from numpy import *
import matplotlib.pyplot as plt

import scipy
import scipy.spatial as spatial
import time
import random

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
# plt output function
#
def pltt( amatrix, stri, scale ):

    fig = plt.figure()    
    fig.set_size_inches( scale * 5.1615 / 16 , scale * 5.1615 / 16 )
    plt.imshow( amatrix )
    fig.savefig(
        stri, 
        bbox_inches = 'tight', pad_inches = 0, dpi = 4 )



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
    
    kd = spatial.KDTree(points)
    
    #Reduce the step for these loops to 1, in order to increase accuracy
    for x in range( 0, size, 2 ):
    
        for y in range( 0, size, 2 ):
            
            close=kd.query([x,y],1)
            amatrix[x][y] = close[0]


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
# Water-based Erosion
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
                
                
                diffmod = (101.0-amatrix[x][y])/101
                diff11 = amatrix[x][y] + water[x][y] - amatrix[x1][y1] - water[x1][y1] * diffmod
                diff12 = amatrix[x][y] + water[x][y] - amatrix[x1][y2] - water[x1][y2] * diffmod
                diff22 = amatrix[x][y] + water[x][y] - amatrix[x2][y2] - water[x2][y2] * diffmod
                diff21 = amatrix[x][y] + water[x][y] - amatrix[x2][y1] - water[x2][y1] * diffmod
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
        # multiply the previous line to use this to add more detailing
        
        #print "actions:",count
        #print "sediment:",sumsediment
        sumsediment = 0
        sumwater *= (1-e)
        water *= (1-e)
        #print "water:",sumwater
        scipy.misc.imsave( 'water%d.png' % z, water )

 

#
# Thermally erode a single tile, aligned with the squares
#
def Erosion_Thermal_Helper( amatrix, x, y, t, m ):

    size = int( amatrix.size ** ( 0.5 ) )

    x1 = ( x - 1 ) % size
    x2 = ( x + 1 ) % size
    y1 = ( y - 1 ) % size
    y2 = ( y + 1 ) % size
    
    factor = (25-amatrix[x][y])/25
    d1 = ( amatrix[x][y] - amatrix[x1][y ] ) * factor
    d2 = ( amatrix[x][y] - amatrix[x2][y ] ) * factor
    d3 = ( amatrix[x][y] - amatrix[x ][y1] ) * factor
    d4 = ( amatrix[x][y] - amatrix[x ][y2] ) * factor
    
    dmax = max( d1, d2, d3, d4, m )
    
    if(d1 == dmax):
        amatrix[x ][y] -= t * dmax / factor
        amatrix[x1][y] += t * dmax / factor
    elif(d2 == dmax):
        amatrix[x ][y] -= t * dmax / factor
        amatrix[x2][y] += t * dmax / factor
    elif(d3 == dmax):
        amatrix[x][y ] -= t * dmax / factor
        amatrix[x][y1] += t * dmax / factor
    elif(d4 == dmax):
        amatrix[x][y ] -= t * dmax / factor
        amatrix[x][y2] += t * dmax / factor
    

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



def Terrain_Mod(amatrix):

    wall = time.clock()

    c = amatrix    
    c = Matrix_Scale( c, 0, 20 )
    d = Elevation_Selection( c, 15, 20, 15, 20) - 15
    c += d * 0.7
    d = Elevation_Selection( c, 11, 20, 11, 20) - 11
    c += d * 0.7

    print "Done Mountains and valleys", ( time.clock() - wall )
    wall = time.clock()
    
    d = Elevation_Selection( c, 3.3, 9, 3.3, 3.3 ) - 3.3
    d = Gaussian_Blur( d, 4)
    c += d * 0.2
    d = Elevation_Selection( c, 9, 13, 9, 9 ) - 9
    d = Gaussian_Blur( d, 7)
    c -= d * 0.4

    print "Done Slopes", ( time.clock() - wall )
    wall = time.clock()
    
    return c




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
            
            d1 = ( amatrix[x][y] - amatrix[x1][y ] ) * 1.34
            d2 = ( amatrix[x][y] - amatrix[x2][y ] ) * 1.34
            d3 = ( amatrix[x][y] - amatrix[x ][y1] ) * 1.34
            d4 = ( amatrix[x][y] - amatrix[x ][y2] ) * 1.34
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
    amatrix+= rivers / 40
    #scipy.misc.imsave( 'final_rivers_%d.png' % (z**(1.0/2)), rivers )

size=256
wall = time.clock()
wall2 = wall

a = zeros((size+1,size+1))
Midpoint_Displacement(a)
a = a[0:size,0:size]
b = zeros((size,size))
Voronoi( b, 9 )
b = -Gaussian_Blur( b, 5 )
a += b*6
Voronoi( b, 64 )
b = -Gaussian_Blur( b, 5 )
a += b*16
a=Matrix_Scale(a,0,100)


print "Done Basic Noise", ( time.clock() - wall )
wall = time.clock()

scipy.misc.imsave( 'basic.png', a )
a = Terrain_Mod(a)

save('basic.npy',a)
# Comment out everything above this, and 
# uncomment line below to use constant input
a = load( 'basic.npy' )
scipy.misc.imsave( 'early.png', a )

#Erosion_Water( a, 3, 10, 1, 0, 0  )
a = Erosion_Thermal( a, 20, 0.5, 0.3)

save('eroded.npy',a)
# Comment out everything above this, and 
# uncomment line below to use constant input
a = load( 'eroded.npy' )
scipy.misc.imsave( 'eroded.png', a )

print "Done Erosion", ( time.clock() - wall )
wall = time.clock()

#print Stats_Percentile(a)
for z in range( 20, 40 ):
    Rivers(a,z**2)
Matrix_Crop(a,2,30)
save('final.npy',a)
# Comment out everything above this, and 
# uncomment line below to use constant input
a = load( 'final.npy' ) * 2 + load( 'eroded.npy' )


scipy.misc.imsave( 'weird9.png', a )
pltt(a,'weird9_mask.png',size)

print "Done Rivers", ( time.clock() - wall )

print "Done Everything", ( time.clock() - wall2 )

