import voronoi
import perlin

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

def GeneratePerlin(size, scale=2.0, seed=-42):

    if(seed == -42):
        seed = random.randint(127,65535)
        #seed = random.randint(8,64)
        #seed = 2^seed

    perlinMap = zeros((size,size))
    
    per = perlin.SimplexNoise()
    per.randomize(seed)

    for x in range (0,size):
        for y in range (0,size):
            perlinMap[x][y] = per.noise2(x*scale/size,y*scale/size)

    return perlinMap


def PerlinLayers(size,layers):
    
    a = GeneratePerlin(size)
    for i in range(1,layers):

        a*= 2
        a += GeneratePerlin(size,8.0*i)*(layers-i)/layers
    
    return a

wall = time()

a = PerlinLayers(512,3)
imsave("Perlin.png",a)
print "All the layers:",time()-wall
