import random
import thread
import time

from numpy import *
import pylab
import scipy
import scipy.misc

from functions import *


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

def Erosion_Water_2( amatrix, its = 10, d = 0.8, maxrat = 0.4, evap = 0.2, sed = 0.7, waterinc = 20 ):

    size = int( amatrix.size ** ( 0.5 ) )

    # the water sitting on top of everything
    water = zeros((size,size))

    # sediment to be added to amatrix only at the very end of the algorithm
    sediment = zeros((size,size))

    watercap = 0;
    
    sumsediment = 0
    sumwater = 0


    for z in range( its ):

        #add water to the map
        water += waterinc
        sumwater += size * size * waterinc

        #have each unit of water draw up d rock into the sediment layer
        sediment += water * d
        sumsediment += sumwater * d
        amatrix -= water * d

        # now the magical part: moving sediment and water around
        for x in range( 1, size - 1 ):
            
            for y in range( 1, size - 1 ):


                x1 = amatrix[x-1][y]+sediment[x-1][y]-amatrix[x][y]-sediment[x][y]
                x2 = amatrix[x+1][y]+sediment[x+1][y]-amatrix[x][y]-sediment[x][y]
                y1 = amatrix[x][y-1]+sediment[x][y-1]-amatrix[x][y]-sediment[x][y]
                y2 = amatrix[x][y+1]+sediment[x][y+1]-amatrix[x][y]-sediment[x][y]
                maxi = max(x1,x2,y1,y2)
                
                if(maxi == x1):
                    sediment[x-1][y] -= maxi * maxrat
                    sediment[x][y] += maxi * maxrat
                elif(maxi == x2):
                    sediment[x+1][y] -= maxi * maxrat
                    sediment[x][y] += maxi * maxrat
                elif(maxi == y1):
                    sediment[x][y-1] -= maxi * maxrat
                    sediment[x][y] += maxi * maxrat
                elif(maxi == y2):
                    sediment[x][y+1] -= maxi * maxrat
                    sediment[x][y] += maxi * maxrat


                x1 = amatrix[x-1][y-1]+sediment[x-1][y-1]-amatrix[x][y]-sediment[x][y]
                x2 = amatrix[x+1][y-1]+sediment[x+1][y-1]-amatrix[x][y]-sediment[x][y]
                x3 = amatrix[x-1][y+1]+sediment[x-1][y+1]-amatrix[x][y]-sediment[x][y]
                x4 = amatrix[x+1][y+1]+sediment[x+1][y+1]-amatrix[x][y]-sediment[x][y]

                xw1 = x1 + water[x-1][y-1] - water[x][y]
                xw2 = x1 + water[x+1][y-1] - water[x][y]
                xw3 = x1 + water[x-1][y+1] - water[x][y]
                xw4 = x1 + water[x+1][y+1] - water[x][y]
                
                maxi = max(xw1,xw2,xw3,xw4)
                moveWater = maxi * maxrat
                
                if(maxi == xw1):
                    water[x-1][y-1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == xw2):
                    water[x+1][y-1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == xw3):
                    water[x-1][y+1] -= moveWater
                    water[x][y] += moveWater
                elif(maxi == xw4):
                    water[x+1][y+1] -= moveWater
                    water[x][y] += moveWater


        print "Sediment Per Square:",sumsediment/size/size,", Water Per Square",sumwater/size/size


        water *= evap
        sumwater *= evap

        amatrix += sediment * sed
        sediment *= ( 1 - sed )
        sumsediment *= ( 1 - sed )

        scipy.misc.imsave("water_terrain_%d.png" % z, amatrix )
        scipy.misc.imsave("water_water_%d.png" % z, water )
        scipy.misc.imsave("water_sediment_%d.png" % z, sediment )
        scipy.misc.imsave("water_net_%d.png" % z, amatrix + water + sediment )
        print "Max Water Transferred:", watercap
        print "Terrain:",Stats_Range(amatrix)
        print "Water:",Stats_Range(water)
        print "Sediment:",Stats_Range(sediment)

    return amatrix


def main1():
    wall = time.clock()

    a =Gaussian_Blur(-Voronoi(zeros((1024,1024)),64,8),5)
    a = Matrix_Crop(Matrix_Scale(Matrix_Half(a),0,100),20,70)
    scipy.misc.imsave( 'Early.png', a )

    save("a.npy",a)
    print "Done Early",(time.clock()-wall)

def main2():
    wall = time.clock()
    
    a = load("a.npy")

    #print Stats_Percentile(Slope_Field(a))

    # amatrix is the matrix to work on
    # its is the number of iterations the algorithm runs through
    # d is the amount of rock water pulls up
    # maxrat is the amount of sediment and water to move, 0.5 creates flatness
    # evap is the rate of evaporation of the water
    # sed is the rate of converting sediment into rock each round
    # at the end of the algorithm, remaining sediment is removed from existance
    # waterinc is the amount of water to add each round

    a = Erosion_Water_2(a,5,0.8,0.6,0.2,0.7,30)
    #print Stats_Percentile(Slope_Field(a))
    scipy.misc.imsave( 'HeavilyEroded.png', a )

    print "Done Heavy Erosion",(time.clock()-wall)

main1()
main2()
