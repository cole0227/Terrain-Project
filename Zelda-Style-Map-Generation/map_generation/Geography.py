from math import log
import sys
import random
from time import *
import profile

from numpy import *
import pylab
import scipy
import scipy.spatial
from scipy.misc import imsave

import voronoi
import perlin
from hills import *

global debug
debug = False

#
# Produces coords along or nearby a vector, given an angle, starting posision, and rectangle
#
def blurry_vector(angle=360, posn=(0,0), rect=(0,0,1024,1024), random_offset=0):
    x = posn[0]
    y = posn[1]


#############################################################
#
# Thermally erode a map. Erosion_Thermal*
#
# Helper functions provide different algorithms and patterns
#
#############################################################

#
# Squareish Helper
#
def erosion_thermal_helper( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y]
    d2 = amatrix[x][y] - amatrix[x][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y]
    d4 = amatrix[x][y] - amatrix[x][y+1]
    
    dmax = max( d1, d2, d3, d4, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y-1] += tomove
    elif(d3 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y] += tomove
    elif(d4 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y+1] += tomove


#
# Diagonals
#
def erosion_thermal_helper_diag( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y-1]
    d2 = amatrix[x][y] - amatrix[x+1][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y+1]
    d4 = amatrix[x][y] - amatrix[x-1][y+1]
    
    dmax = max( d1, d2, d3, d4, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y-1] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y-1] += tomove
    elif(d3 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y+1] += tomove
    elif(d4 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y+1] += tomove


#
# Sweeping
#
def erosion_thermal_helper_sweep( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y-1]
    d2 = amatrix[x][y] - amatrix[x][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y-1]
    d4 = amatrix[x][y] - amatrix[x+1][y]
    
    dmax = max( d1, d2, d3, d4, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove * 0.7
        amatrix[x-1][y-1] += tomove * 0.7
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y-1] += tomove
    elif(d3 == dmax):
        amatrix[x][y] -= tomove * 0.7
        amatrix[x+1][y-1] += tomove * 0.7
    elif(d4 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y] += tomove

    
#
# Verticalish
#
def erosion_thermal_helper_v( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x][y-1]
    d2 = amatrix[x][y] - amatrix[x][y+1]
    
    dmax = max( d1, d2, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y-1] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x][y+1] += tomove


#
# Horzish
#
def erosion_thermal_helper_h( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y]
    d2 = amatrix[x][y] - amatrix[x+1][y]
    
    dmax = max( d1, d2, minimum )
    tomove = dmax / 2.0
    
    if(d1 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x-1][y] += tomove
    elif(d2 == dmax):
        amatrix[x][y] -= tomove
        amatrix[x+1][y] += tomove


#
# Wild/stupid
#
def erosion_thermal_helper_stupid( amatrix, x, y, minimum ):

    size = int( amatrix.size ** ( 0.5 ) )

    d1 = amatrix[x][y] - amatrix[x-1][y-1]
    d2 = amatrix[x][y] - amatrix[x+1][y-1]
    d3 = amatrix[x][y] - amatrix[x+1][y+1]
    d4 = amatrix[x][y] - amatrix[x-1][y+1]
    
    factor = 2.0
    amatrix[x][y] -= d1 / factor
    amatrix[x-1][y-1] += d1 / factor
    amatrix[x][y] -= d2 / factor
    amatrix[x+1][y-1] += d2 / factor
    amatrix[x][y] -= d3 / factor
    amatrix[x+1][y+1] += d3 / factor
    amatrix[x][y] -= d4 / factor
    amatrix[x-1][y+1] += d4 / factor


#
# Erodes thermally
#
def erosion_thermal( amatrix, its = 8, minimum = 5 ):

    for z in range( 0, its ):
        
        size = int( amatrix.size ** ( 0.5 ) )
        for x in range( 1, size-1 ):
            
            for y in range( 1, size-1 ):
            
                erosion_thermal_helper( amatrix, x, y, minimum )
                erosion_thermal_helper_diag( amatrix, x, y, minimum )
        
    return amatrix


#
# Generates p Varonoi cells
#
# must be followed immediatly with a blur
#
def voronoi(amatrix,p=100,edge=15, step=4):
    
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
    
    for x in range( 0, size, step ): # change step to 1 for accuracy
    
        #print 'row',x
        for y in range( 0, size, step ): # change step to 1 for accuracy
            
            close=kd.query([x,y],1)
            for x1 in range(0, step):
                for y1 in range(0, step):
                    amatrix[x+x1][y+y1] = close[0]
            
    return amatrix


#
# image saving
#
def imsave(i, a, ovr=False):
    if(ovr or debug):
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
def erosion_water( amatrix, its = 10, d = 1.0, maxrat = 0.51, evap = 0.041, sed = 0.80, waterinc = 11.5 ):

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
                else:
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


        #print "Sediment Per Square:",sumsediment/size/size,", Water Per Square",sumwater/size/size

        water *= ( 1 - evap )
        sumwater *= ( 1 - evap )

        amatrix += water / sumwater * sumsediment * sed
        sumsediment *= ( 1 - sed )

        #imsave("water_terrain_%d.png" % z, amatrix )
        #imsave("water_water_%d.png" % z, water )
        #print "Max Water Transferred:", watercap
        #print "Terrain:",stats_range(amatrix)
        #print "Water:",stats_range(water)
        
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


#
# Cuts off any elements outside of the min and max
#
def matrix_crop(amatrix,minimum,maximum):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( 0, size ):

        for y in range( 0, size ):

            amatrix[x][y] = max( minimum, min( maximum, amatrix[x][y] ) )
    return amatrix


#
# Forces the numbers in a matrix to within set bounds
#
def matrix_scale(amatrix,minimum,maximum):
        
    size = int( amatrix.size ** ( 0.5 ) )
    rs = stats_range( amatrix )
    factor = ( maximum - minimum ) / ( rs[1] - rs[0] )
    amatrix = ( amatrix - rs[0] ) * factor + minimum
    return amatrix

#
# Makes a matrix made of magical perlin noise
#
def Perlin(size, scale=2.0, seed=-42):

    if(seed == -42):
        seed = random.randint(127,65536)
        #seed = random.randint(8,64)
        #seed = 2^seed

    perlinMap = zeros((size,size))
    
    per = perlin.SimplexNoise()
    per.randomize(seed)

    for x in range (0,size):
        for y in range (0,size):
            perlinMap[x][y] = per.noise2(x*scale/size,y*scale/size)

    return perlinMap


#
# Makes a matrix full of *interesting perlin-based noise
#
def GeneratePerlin(size,layers):
    
    a = Perlin(size)
    for i in range(1,layers):

        a*= 2
        a += Perlin(size,8.0*i)

    return a

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

    def calc_total(self):

        size = int( self.map.size ** ( 0.5 ) )
        newtotal = 0
        
        for x in range(0, size):
            
            for y in range(0, size):
            
                newtotal += self.map[x][y]

        return newtotal

    def reassign_total(self):

        self.total = self.calc_total()

    def reconstitute(self):

        newtotal = self.calc_total()
        self.map *= abs(self.total/newtotal)

    def sedimentize(self,prop=1):

        size = int(self.map.size ** (0.5))
        tot = self.calc_total()
        num = 0
        ave = tot/self.map.size*prop

        for x in range(0, size):
            
            for y in range(0, size):

                if(self.map[x][y] < ave):

                    num += self.map[x][y]
                    self.map[x][y] = 0

        print "Rock Removed:",num,"\tTest:",tot/self.map.size*prop

    def cap_b(self,prop=1):

        size = int(self.map.size ** (0.5))
        tot = self.calc_total()
        num = 0
        ave = tot/self.map.size*prop

        for x in range(0, size):
            
            for y in range(0, size):

                if(self.map[x][y] < ave):

                    num += self.map[x][y] - ave
                    self.map[x][y] = ave

        return num

    def cap_t(self,prop=1):

        size = int(self.map.size ** (0.5))
        tot = self.calc_total()
        num = 0
        ave = tot/self.map.size*prop

        for x in range(0, size):
            
            for y in range(0, size):

                if(self.map[x][y] > ave):

                    num += self.map[x][y] - ave
                    self.map[x][y] = ave

        return num

    def slice_min(self):

        size = int(self.map.size ** (0.5))
        tot = self.calc_total()
        num = 0
        mini = stats_range(self.map)[0]

        num += size*size * mini
        self.map -= mini

        return num

class map_data(object):

    def __init__(self,layers):
        self.layers=layers

    def total_height(self,pos):

        total = 0;
        
        for layer in self.layers:

            total += layer.map[pos[0]][pos[1]]

        return total

    def reassign_total(self):

        for layer in self.layers:

            layer.reassign_total()

    def reconstitute(self):

        for layer in self.layers:

            layer.reconstitute()

    def __str__(self):

        stri = "Layers:"+str(len(self.layers))
        i = 0

        for layer in self.layers:

            stri += "\nLayer:"+str(i)
            stri += " \t\tHRD:"+str(int(layer.hardness*100)/100.0)
            stri += " \t\tTTL:"+str(int(layer.total*100)/100.0)
            stri += "\t\tAVG:"+str(int(layer.calc_total()/self.layers[0].map.size*100)/100.0)
            i+=1

        return stri

    def imsave(self, pre=""):

        i=0

        for layer in self.layers:

            imsave(str(pre)+"_Layer_"+str(i)+".png",layer.map)
            
            i+=1

        height = self.heightmap()
        imsave(str(pre)+"_Main.png",height)
        return height
    
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

    def sedimentize(self, prop=1, layer_index = None):
        
        if(layer_index == None):
            
            for layer in self.layers:
                
                layer.sedimentize(prop)
                
            self.reconstitute()
            
        else:
            
            self.layers[layer_index].sedimentize(prop)
            self.layers[layer_index].reconstitute()

    def cap_b(self, prop=1, layer_index = None):
        
        if(layer_index == None):
            
            for layer in self.layers:
                
                layer.cap_b(prop)
                
            self.reassign_total()
            
        else:
            
            self.layers[layer_index].cap_b(prop)
            self.layers[layer_index].reassign_total()

    def cap_t(self, prop=1, layer_index = None):
        
        if(layer_index == None):
            
            for layer in self.layers:
                
                layer.cap_t(prop)
                
            self.reassign_total()
            
        else:
            
            self.layers[layer_index].cap_t(prop)
            self.layers[layer_index].reassign_total()

    def slice_min(self, layer_index = None):
        
        if(layer_index == None):
            
            num = 0

            for layer in self.layers:
                
                num += layer.slice_min()
                
            self.reassign_total()
            print "Rock Removed:",num

        else:
            
            self.layers[layer_index].slice_min()
            self.layers[layer_index].reassign_total()

    def spider_mountain(self,layer_index,count,height=100,f=0.91,togo=25):

        size = int( self.layers[layer_index].map.size ** ( 0.5 ) )
        for i in range(0,count):

            self.layers[layer_index].map = spider_mountain_wrapper(
                self.layers[layer_index].map,
                random.randint(togo+2,size-togo-3),
                random.randint(togo+2,size-togo-3),
                height,f,togo)

        self.layers[layer_index].reconstitute()
    
    def erode_water( self, layer_index=None, its = 10, d = 1.0, maxrat = 0.51, evap = 0.041, sed = 0.80, waterinc = 11.5 ):

        if(layer_index == None):
            
            for layer in self.layers:
                
                layer.map = erosion_water( layer.map, its, d, maxrat, evap, sed, waterinc )
                
            #self.reconstitute()
            self.reassign_total()
            
        else:

            self.layers[layer_index].map = erosion_water( self.layers[layer_index].map, its, d, maxrat, evap, sed, waterinc )
            self.layers[layer_index].reconstitute()

    def erode_thermal( self, its = 8, minimum = 0.1 ):
            

        #
        # Squareish Helper
        #
        def erosion_thermal_helper( kernel, x, y, minimum ):

            d1 = kernel[1][1] - kernel[0][1]
            d2 = kernel[1][1] - kernel[1][0]
            d3 = kernel[1][1] - kernel[2][1]
            d4 = kernel[1][1] - kernel[1][2]

            dmax = max( d1, d2, d3, d4, minimum )
            tomove = dmax / 2.0
            
            if(d1 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x-1,y),-tomove)
            elif(d2 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x,y-1),-tomove)
            elif(d3 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x+1,y),-tomove)
            elif(d4 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x,y+1),-tomove)
            else:
                return 0

            return tomove


        #
        # Diagonals
        #
        def erosion_thermal_helper_diag( kernel, x, y, minimum ):

            d1 = kernel[1][1] - kernel[0][0]
            d2 = kernel[1][1] - kernel[2][0]
            d3 = kernel[1][1] - kernel[0][2]
            d4 = kernel[1][1] - kernel[2][2]
            
            dmax = max( d1, d2, d3, d4, minimum )
            tomove = dmax / 2.0
            
            if(d1 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x-1,y-1),-tomove)
            elif(d2 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x+1,y-1),-tomove)
            elif(d3 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x-1,y+1),-tomove)
            elif(d4 == dmax):
                self.erode2((x,y),tomove)
                self.erode2((x+1,y+1),-tomove)
            else:
                return 0

            return tomove

        #
        # The algorithm proper
        #

        size = int( self.layers[0].map.size ** ( 0.5 ) )

        for z in range( 0, its ):
            
            total=0
            start = 1+z%2*(size-3)
            end = size-2+z%2*(3-size)
            step = 1+z%2*(-2)
            #print start, end, 1+z%2*(-2) 

            for x in range( start, end, step ):
    
                for y in range( end, start, -step ):
                    
                    kernel = zeros((3,3))
                    for x1 in range( 0, 3 ):
                        for y1 in range( 0, 3 ):
                            kernel[x1][y1]=self.total_height((x+x1-1,y+y1-1))
                    #print kernel

                    total+=erosion_thermal_helper( kernel, x, y, minimum )
                    total+=erosion_thermal_helper_diag( kernel, x, y, minimum )
            print "Cycle",z,"=",total
        #self.reconstitute()

    # special case: eroding from the surface
    def erode2(self,pos,amount):

        self.erode(-1,pos,amount)

    def erode(self,layer_index,pos,amount):

        to_skip = layer_index
        amount_left = amount
        
        array = reversed(self.layers)
        if(layer_index == -1):
            array = self.layers

        for layer in array:
            
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

def main(num_layers):

    wall = time()
    wall2 = time()
    size = 512
    layers = (layer(size,5,3,0.3),
              layer(size,10,3,0.6),
              layer(size,3,3,0.95))
    
    for i in range(0,num_layers):
        layers = layers + (layer(size,random.uniform(2,5),random.uniform(0,2),random.uniform(0.05,0.95)),)
        print i
    
    print "All the layers:",time()-wall
    wall = time()
    
    main = map_data(layers)
    main.blur(3)
    main.spider_mountain(2,150)
    for i in range(0,num_layers,3):
        main.spider_mountain(i,50)
        print i

    
    print "Main Init:",time()-wall
    wall = time()
    
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
    main.blur(4,1)
    main.layers[1].total *= 6
    main.reconstitute()
    
    print "Fault Lines:",time()-wall
    wall = time()

    main.layers[1].map = erosion_water((main.layers[1].map-100)*6,20)
    #main.layers[1].map = erosion_water((main.layers[1].map-100)*6,18)
    main.layers[1].map -= stats_range(main.layers[1].map)[0]
    spare = main.layers[2].map
    main.blur(4,2)
    main.layers[2].map += spare * 3
    main.layers[2].total *= 1.7
    main.reconstitute()
    
    print "Erosion:",time()-wall
    wall = time()
    
    rough_peaks = main.heightmap()
    imsave("1.png",spare)
    imsave("2.png",rough_peaks)
    imsave("3.png",main.heightmap())
    print "T:", stats_range(main.heightmap())
    rough_peaks = matrix_scale(rough_peaks,0,100)
    spare = matrix_scale(spare,0,100)
    
    print "Peaks:",time()-wall
    wall = time()
    eros = main.heightmap()
    
    for i in range(0,4):
        q = random.uniform(-0.1,0.1)+1.03
        w = random.uniform(-0.1,0.1)+0.611
        e = random.uniform(-0.005,0.005)+0.0427
        r = random.uniform(-0.2,0.2)+0.677
        t = random.uniform(-1,1)+11.522

        q = random.uniform(-0.1,0.1)+1.00
        w = random.uniform(-0.1,0.1)+0.51
        e = random.uniform(-0.005,0.005)+0.041
        r = random.uniform(-0.2,0.2)+0.84
        t = random.uniform(-1,1)+11.26
        print q,w,e,r,t
        eros = matrix_scale(erosion_water(eros,8, q,w,e,r,t),0,100)
        imsave("rnd_"+str(i)+"_"+str(q)+"_"+str(w)+"_"+str(e)+"_"+str(r)+"_"+str(t)+".png",eros)
        imsave("rnd_"+str(i)+"_"+str(q)+"_"+str(w)+"_"+str(e)+"_"+str(r)+"_"+str(t)+"_broken.png",eros * 2.3 - rough_peaks * 1.1)
        print "Iteration:",time()-wall
        wall = time()

    print "Total Time:",time()-wall2


def clean_main(size, mountains, num_layers, erosion):
    wall = time()
    wall2 = time()

    layers = (layer(size,20,10,8.0),)
    
    for i in range(0,num_layers):
        layers += (layer(size,random.uniform(4,7),random.uniform(2,3),random.uniform(1.5,4.0)),)

    layers += (layer(size,20,10,0.5),)

    print "Step 1:",time()-wall
    wall = time()

    main = map_data(layers)
    imsave("clean_"+str(size)+"_1.png",main.heightmap())
    main.blur(erosion/3)
    main.spider_mountain(0, mountains)
    
    imsave("clean_"+str(size)+"_2.png",main.heightmap())

    print "Step 2:",time()-wall
    wall = time()

    main.reassign_total()
    main.erode_thermal(4,0.1)
    imsave("clean_"+str(size)+"_3.png",main.heightmap())

    print "Step 3:",time()-wall
    wall = time()

    main.sedimentize()
    imsave("clean_"+str(size)+"_4.png",main.heightmap())
    final = erosion_water(main.heightmap(),3)
    imsave("clean_"+str(size)+"_5.png",final)


    print "Step 4:",time()-wall
    wall = time()

    mountians = main.layers[0].map
    main.blur(erosion/2,0)
    main.layers[0].map = erosion/2.0 * main.layers[0].map - mountains
    imsave("clean_"+str(size)+"_6.png",main.heightmap())

    print "Step 5:",time()-wall
    wall = time()

    print "Total Time:",time()-wall2

    return main.heightmap()

def perlin_main(size, mountains, num_layers, erosion):
    wall = time()
    wall2 = time()

    layers = (layer(size,20,10,8.0),)
    
    for i in range(0,num_layers):
        layers += (layer(size,random.uniform(4,7),random.uniform(2,3),random.uniform(1.5,4.0)),)

    layers += (layer(size,20,10,0.5),)

    print "Step 1:",time()-wall
    wall = time()

    main = map_data(layers)
    imsave(str(size)+"_1.png",main.heightmap())
    main.blur(erosion/3)
    main.spider_mountain(0, mountains)
    
    layers[1].map=matrix_scale(GeneratePerlin(size,5),0,50)
    layers[1].reassign_total()
    
    print main
    imsave(str(size)+"_2.png",main.heightmap())

    print "Step 2:",time()-wall
    wall = time()

    main.reassign_total()
    print main
    main.erode_thermal(4,0.1)
    print main
    imsave(str(size)+"_3.png",main.heightmap())

    print "Step 3:",time()-wall
    wall = time()

    #main.layers[1].sedimentize(0.98)
    #imsave("4a.png",main.layers[1].map)
    #main.layers[2].sedimentize(0.99)
    #imsave("4b.png",main.layers[2].map)
    #main.layers[3].sedimentize(1.01)
    #imsave("4c.png",main.layers[3].map)
    #main.layers[4].sedimentize(1.02)
    #imsave("4d.png",main.layers[4].map)
    
    main.cap_b(0.3)
    main.cap_t(3.0)
    main.imsave(str(size)+"_3")
    main.slice_min()
    hills=main.imsave(str(size)+"_4")
    imsave(str(size)+"_4.png",main.heightmap())
    final = erosion_water(main.heightmap(),erosion/2)
    imsave(str(size)+"_5.png",final)


    print "Step 4: basic erosion and slicing",time()-wall
    wall = time()

    mountians = main.layers[0].map+main.layers[1].map
    main.blur(erosion/2,0)
    main.layers[0].map = erosion/2.0 * main.layers[0].map+main.layers[1].map + mountains
    imsave(str(size)+"_6.png",main.heightmap())

    print "Step 5: erosion and raising mountains",time()-wall
    wall = time()

    main.layers[1].map += hills*0.7
    main.sedimentize(1.0,len(main.layers)-1)
    main.sedimentize(1.0,len(main.layers)-2)
    main.sedimentize(1.0,len(main.layers)-3)
    imsave(str(size)+"_7.png",main.heightmap())

    print "Step 6: re-added step 4's hills",time()-wall
    wall = time()

    print "Total Time:",time()-wall2

    return main.heightmap()

if(__name__ == '__main__'):

    

    global debug
    debug = True
    #profile.run("main()")
    #main(50)
    #clean_main(4096, 2000,10,10)
    clean_main(1024, 1000,10,10)
    #clean_main(256, 75, 10, 10)
    #perlin_main(128, 20, 10, 6)
