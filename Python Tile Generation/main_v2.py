import random
import thread
import time

from numpy import *
import pylab
import scipy
import scipy.misc

from functions import *


def main1():
    wall = time.clock()

    a =Gaussian_Blur(-Voronoi(zeros((1024,1024)),64,8),5)
    a = Matrix_Crop(Matrix_Scale(Matrix_Half(a),-20,130),0,100)

    save("a.npy",a)
    print "Done Early",(time.clock()-wall)

def main1t():
    a = zeros((512,512))
    
    for x in range( 128, 384 ):
            
        for y in range( 128, 384 ):

            if((256-x)**2+(256-y)**2 < 2500):
                a[x][y] = 100
            

    save("a.npy",a)

def main2():
    wall = time.clock()
    
    #a = load("a.npy")

    a = zeros((1024,1024))
    for z in range(0, 750):
        a = Spider_Mountain_Wrapper( a, random.randint(50, 950), random.randint(50, 950))
    
    scipy.misc.imsave( 'Begin.png', a )

    #scipy.misc.imsave( 'SlopeBegin.png',Slope_Field(a))

    #                  amatrix is the matrix to work on
    #                  |  its is the number of iterations the algorithm runs through
    #                  |  |  d is the amount of rock which water pulls up
    #                  |  |  |     maxrat is the amount of sediment and water to move, 0.5 creates flatness
    #                  |  |  |     |    evap is the rate of evaporation of the water
    #                  |  |  |     |    |     sed is the rate of converting sediment into rock each round at the end of the algorithm, remaining sediment is removed from existance
    #                  |  |  |     |    |     |     waterinc is the amount of water to add each round
    #                  |  |  |     |    |     |     |
    #a = Erosion_Water( a, 3, 0.95, 0.5, 0.80, 0.95, 5 )
    #print Stats_Range(Slope_Field(a))
    a = Erosion_Thermal(a, 3, 1)
    scipy.misc.imsave( 'Eroded.png', a )

    #b = load("a.npy")  
    #a = (Matrix_Scale(a,0,100)-b)*2 + b

    #scipy.misc.imsave( 'SlopeFinal.png',Slope_Field(a))

    #a = Matrix_Scale( a, 20, 70 )
    #scipy.misc.imsave( 'HeavilyEroded.png', a )

    #a2 = load("a2.npy")
    #scipy.misc.imsave( 'HeavilyEroded2.png', a2 )
    #scipy.misc.imsave( 'Diff.png', a - a2 )

    #save("a2.npy",Matrix_Scale(a,20,70))

    #a -= load("a.npy")
    #scipy.misc.imsave( 'Delta.png', a )

    print "Done Heavy Erosion",(time.clock()-wall)

#main1t()
main2()
