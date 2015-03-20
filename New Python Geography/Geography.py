from math import log
import sys
import random
import time
import profile

from numpy import *
import pylab
import scipy
import scipy.spatial
from scipy.misc import imsave

execfile("hills.py")

#
# image saving
#
def imsave(i, a):

    scipy.misc.imsave(i,a)


#
# Blurs quickly to the radius specified
#
def gaussian_blur( amatrix, radius ):

    size = int( amatrix.size ** ( 0.5 ) )
    kernel = gaussian_kernel( size, size, radius )
    blur = apply_kernel( size, size, amatrix, kernel )
    return blur


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
def spider_mountain(amatrix, x, y, height, direction, f, togo):

    b = 0.2

    #change the += to =, and fill the map with them to see the nightmare
    amatrix[x][y] += height

    # adds more bulk and solidity
    left = (direction+7)%8
    right = (direction+1)%8
    amatrix[x+  Spider_X(left )][y+  Spider_Y(left )] += height / 2
    amatrix[x+  Spider_X(right)][y+  Spider_Y(right)] += height / 2
    amatrix[x+2*Spider_X(left )][y+2*Spider_Y(left )] += height / 4
    amatrix[x+2*Spider_X(right)][y+2*Spider_Y(right)] += height / 4
    amatrix[x+3*Spider_X(left )][y+3*Spider_Y(left )] += height / 7
    amatrix[x+3*Spider_X(right)][y+3*Spider_Y(right)] += height / 7

    if( random.random() < 0.10 ):
        direction += random.randint(-1,1)
    
    if( togo == 0 ):
        
        return 0
            
    else:

        if( togo % random.randint(8,15) == 0 ):

            left  = ( direction+7 ) % 8
            right =  ( direction+1 ) % 8
            
            spider_mountain(amatrix, x+Spider_X(left ), y+Spider_Y(left ), height*f, left , f, togo-1 )
            spider_mountain(amatrix, x+Spider_X(right), y+Spider_Y(right), height*f, right, f, togo-1 )

        elif( random.random() < 0.93):

            spider_mountain(amatrix, x+Spider_X(direction  ), y+Spider_Y(direction  ), height*f, direction, f, togo-1 ) 

    return 0


#
# Wrapper for preceding function, calls 4 ridges of length togo to spawn at x and y
#
# Is best followed by adding a gaussian of 3 and 6, each at *10 to show up well against it
#
def spider_mountain_wrapper( amatrix, x, y, height = 100, f = 0.91, togo = 50 ):

    amatrix[x][y] -= height * 3
    spider_mountain(amatrix, x, y, height, random.randint(0,1), f, togo)
    spider_mountain(amatrix, x, y, height, random.randint(2,3), f, togo)
    spider_mountain(amatrix, x, y, height, random.randint(4,5), f, togo)
    spider_mountain(amatrix, x, y, height, random.randint(6,7), f, togo)
    return amatrix


#
# Water-based Erosion takes place in four phases
# 1. Adding new water
# 2. Water eroding the rock
# 3. Water transporting itself and the sediment
# 4. Water evaporates
# 5. depositing sediment
#
# amatrix is the matrix to work on
# its is the number of iterations the algorithm runs through
# d is the amount of rock water pulls up
# maxrat is the amount of sediment and water to move, 0.5 creates flatness
# evap is the rate of evaporation of the water
# sed is the rate of converting sediment into rock each round
# at teh end of the algorithm, remaining sediment is removed from existance
# set to 3.5 for unusual results
# waterinc is the amount of water to add each round
#

def erosion_water( amatrix, its = 10, d = 0.95, maxrat = 0.5, evap = 0.05, sed = 0.5, waterinc = 10 ):

    size = int( amatrix.size ** ( 0.5 ) )

    # the water sitting on top of everything
    water = zeros((size,size))

    sumsediment = 0
    sumwater = 0

    for z in range( its ):

        watercap = 0;

        #add water to the map
        water += waterinc
        sumwater += size * size * waterinc

        #have each unit of water draw up d rock into the sediment layer
        sumsediment += sumwater * d
        amatrix -= water * d
        
        # are we doing a lot of work this iteration?
        alt = ((z+2) % 3 == its % 3 )
        if( alt ):
            print 'tick:',z

        # now the magical part: moving sediment and water around
        for x in range( 1, size - 1 ):
            
            for y in range( 1, size - 1 ):
				
                if( alt ):
                    x1 = amatrix[x-1][y]-amatrix[x][y]+water[x-1][y]-water[x][y]
                    x2 = amatrix[x][y-1]-amatrix[x][y]+water[x][y-1]-water[x][y]
                    x3 = amatrix[x][y+1]-amatrix[x][y]+water[x][y+1]-water[x][y]
                    x4 = amatrix[x+1][y]-amatrix[x][y]+water[x+1][y]-water[x][y]
                    
                    maxi = max( x1, x2, x3, x4 )
                    moveWater = maxi * maxrat
                    watercap = max( moveWater, watercap )
                    
                    if(maxi == x1):
                        water[x-1][y] -= moveWater
                        water[x][y] += moveWater
                    elif(maxi == x2):
                        water[x][y-1] -= moveWater
                        water[x][y] += moveWater
                    elif(maxi == x3):
                        water[x][y+1] -= moveWater
                        water[x][y] += moveWater
                    elif(maxi == x4):
                        water[x+1][y] -= moveWater
                        water[x][y] += moveWater

                x1 = amatrix[x-1][y-1]-amatrix[x][y]+water[x-1][y-1]-water[x][y]
                x2 = amatrix[x+1][y-1]-amatrix[x][y]+water[x+1][y-1]-water[x][y]
                x3 = amatrix[x-1][y+1]-amatrix[x][y]+water[x-1][y+1]-water[x][y]
                x4 = amatrix[x+1][y+1]-amatrix[x][y]+water[x+1][y+1]-water[x][y]
                
                maxi = max( x1, x2, x3, x4 )
                moveWater = maxi * maxrat
                watercap = max( moveWater, watercap )
                
                if(maxi == x1):
                    water[x-1][y-1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == x2):
                    water[x+1][y-1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == x3):
                    water[x-1][y+1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == x4):
                    water[x+1][y+1] -= moveWater
                    water[x][y] += moveWater


        print "Sediment Per Square:",sumsediment/size/size,", Water Per Square",sumwater/size/size

        water *= ( 1 - evap )
        sumwater *= ( 1 - evap )

        amatrix += water / sumwater * sumsediment * sed
        sumsediment *= ( 1 - sed )

        #scipy.misc.imsave("water_terrain_%d.png" % z, amatrix )
        #scipy.misc.imsave("water_water_%d.png" % z, water )
        #print "Max Water Transferred:", watercap
        #print "Terrain:",Stats_Range(amatrix)
        #print "Water:",Stats_Range(water)
        
    return amatrix

#########################################################################
#
#  Stats Functions
#
#########################################################################


#
# Finds the Largest and smallest element
#
def stats_range(amatrix):

    mymatrix = amatrix.reshape( -1 )
    sort = mymatrix.argsort()
    final = [mymatrix[sort[0]], mymatrix[sort[ amatrix.size - 1 ]]]
    return final


#
# Gives the value for the 9 intermediary 10th-percentile
# elevations, and the highest and lowest points
#
def stats_percentile( amatrix ):
    
    mymatrix = amatrix.reshape( -1 )
    sort = mymatrix.argsort()

    #
    # Returns the element for the matching percent
    #
    def find_percentile( percent ):
        
        return sort[ min( max( int( ( amatrix.size - 1 ) * percent / 100), 0 ), amatrix.size - 1 ) ]

    final = zeros(( 11 )) 
    for x in range( 0, 11 ):

        final[x] = mymatrix[ find_percentile( x * 10 ) ]

    return final


#########################################################################
#
#  Main Classes
#
#########################################################################


class layer(object):

    def __init__(self,size,height,height_variance,hardness):

        self.map = zeros((size,size)) + height
        self.total = 0;
        self.hardness = hardness

        for x in range(0, size):
            for y in range(0, size):
                self.map[x][y] += random.uniform(0.0,height_variance)-height_variance/2.0
                self.total += self.map[x][y]

    def reconstitute(self):

        size = int( self.map.size ** ( 0.5 ) )
        newtotal = 0
        
        for x in range(0, size):
            
            for y in range(0, size):
            
                newtotal += self.map[x][y]

        self.map *= self.total/newtotal

class map_data(object):

    def __init__(self,layers):
        self.layers=layers

    def total_height(self,pos):
        total = 0;
        
        for layer in self.layers:

            total += layer.map[pos[0]][pos[1]]

    def reconstitute(self):

        for layer in self.layers:

            layer.reconstitute()

    def heightmap(self):
    
        size = int( self.layers[0].map.size ** ( 0.5 ) )

        new_map = zeros((size,size))
        
        for layer in self.layers:

            new_map += layer.map

        return new_map
    
    def blur(self,radius, layer_index = None):
        
        if(layer_index == None):
            
            for layer in self.layers:
                
                layer.map = gaussian_blur(layer.map,radius)
                
            self.reconstitute()
            
        else:
            
            self.layers[layer_index].map = gaussian_blur(self.layers[layer_index].map,radius)
            self.layers[layer_index].reconstitute()

    def spider_mountain(self,layer_index,count,height=100,f=0.91,togo=25):

        size = int( self.layers[layer_index].map.size ** ( 0.5 ) )
        for i in range(0,count):

            self.layers[layer_index].map = spider_mountain_wrapper(
                self.layers[layer_index].map,
                random.randint(togo+2,size-togo-3),
                random.randint(togo+2,size-togo-3),
                height,f,togo)

        self.layers[layer_index].reconstitute()
        
    def erode(self,layer_index,pos,amount):

        to_skip = layer_index
        amount_left = amount

        for layer in reversed(self.layers):
            
            if(to_skip > 0):
                
                to_skip -= 1
                
            else:
            
                if(layer.map[pos[0]][pos[1]] > amount_left/layer.hardness):
                    
                    layer.map[pos[0]][pos[1]] -= amount_left/layer.hardness
                    #print "2:",amount_left/layer.hardness
                    break
                
                amount_left -= layer.map[pos[0]][pos[1]]
                #print "1:",layer.map[pos[0]][pos[1]]
                layer.map[pos[0]][pos[1]] = 0

def main():

    size = 256
    layers = (layer(size,5,3,0.3),
              layer(size,10,3,0.6),
              layer(size,3,3,0.95))
    main = map_data(layers)
    imsave("1.png",main.heightmap())
    main.blur(3)
    main.spider_mountain(2,100)
    imsave("2.png",main.heightmap())
    print "0:", stats_range(main.layers[0].map)
    print "1:", stats_range(main.layers[1].map)
    print "2:", stats_range(main.layers[2].map)

    x = size/2
    y = size/2
    for j in range (0,300):

      x = random.randint(0,size)
      dx = random.randint(-2,3)
      y = random.randint(0,size)
      dy = random.randint(-2,3)
      
      for i in range (0,100):
        main.erode(0,(x,y),2.5)
        if(random.random() < 0.6):
            x += dx
        if(random.random() < 0.6):
            y += dy
        if(dx == 0 or dy == 0 or y < 0 or y > size-1 or x < 0 or x > size-1):
            break

    main.reconstitute()
    imsave( "4.po.png",main.layers[0].map)
    print "0:", stats_range(main.layers[0].map)

    imsave( "4.pp.png",main.layers[1].map)

    main.blur(4,1)
    main.layers[1].total *= 6
    main.reconstitute()
    imsave( "4.ppp.png",main.layers[1].map)

    main.layers[1].map = erosion_water((main.layers[1].map-100)*6,18)
    main.layers[1].map = erosion_water((main.layers[1].map-100)*6,18)
    print "1b:", stats_range(main.layers[1].map)
    main.layers[1].map -= stats_range(main.layers[1].map)[0]
    print "1a:", stats_range(main.layers[1].map)
    main.reconstitute()
    main.layers[2].map *= 1.3

    imsave( "4.pppp.png",main.layers[1].map)
    print "1c:", stats_range(main.layers[1].map)

    imsave( "4.pq.png",main.layers[2].map)
    print "2:", stats_range(main.layers[2].map)
    
    imsave("4.png",main.heightmap())
    print "T:", stats_range(main.heightmap())

    imsave("5.png",erosion_water(main.heightmap(),18))

if(__name__ == '__main__'):

    wall = time()
    #profile.run("main()")
    main()
    print "Time:",time()-wall
