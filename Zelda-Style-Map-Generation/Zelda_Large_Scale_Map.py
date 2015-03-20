import sys
import cStringIO
import gc
import time
import math
import sys
import random
import os
from collections import defaultdict

import numpy
import scipy
from scipy.misc import imsave
import scipy.ndimage
import pygame
from pygame.locals import *
import pygame.time
import pygame.font

from gaussian_blur import gaussian_blur
from map_generation import *

TILE_SIZE = 32

class Map_Chunk(object):

    def __init__(self, map_width, map_height):

        self.map_height = map_height
        self.map_width = map_width
        tiles = pygame.image.load("tiles.png")
        self.tiles = [tiles.subsurface((0*32,0,32,32)),
                      tiles.subsurface((1*32,0,32,32)),
                      tiles.subsurface((2*32,0,32,32)),
                      tiles.subsurface((3*32,0,32,32)),
                      tiles.subsurface((4*32,0,32,32)),
                      tiles.subsurface((5*32,0,32,32)),
                      tiles.subsurface((6*32,0,32,32)),
                      tiles.subsurface((7*32,0,32,32)),
                      tiles.subsurface((5*32,0,32,32)),
                      tiles.subsurface((7*32,0,32,32)),
                      tiles.subsurface((2*32,0,32,32))]
        self.tiles[8].set_alpha(75)
        self.tiles[9].set_alpha(75)
        self.tiles[10].set_alpha(75)

        self.map = numpy.zeros((self.map_width,self.map_height))+10

    def test_for(self,x,y,val,distance=1):
        
        result = 0;
        for x1 in range(x-distance,x+1+distance):
            for y1 in range(y-distance,y+1+distance):
                if(x1 > -1 and y1 > -1 and
                   x1 < self.map_width and
                   y1 < self.map_height and
                   self.map[x1, y1] == val):
                    result+=1
        return result

    def map_over(self,new):
        for x in range(0,self.map_width):
            for y in range(0,self.map_height):
                if(new[x,y]!=-100):
                    self.map[x,y]=new[x,y]
    
    def convert_tuple_to_integer(self,mapped):

        newmap = numpy.zeros((self.map_width,self.map_height))-100

        for x in range(0,self.map_width):
            for y in range(0,self.map_height):
                newmap[x,y] = mapped[x][y]
        return newmap

    def surround(self, distance, val_initial, val_surround, val_maximum=19, val_minimum=-99, chance = 1.0):
        for x in range(0,self.map_width):
            for y in range(0,self.map_height):
                if(self.map[x,y] == val_initial):
                    for x1 in range(x-distance,x+1+distance):
                        for y1 in range(y-distance,y+1+distance):
                            if(chance > random.random() and
                               x1 > -1 and y1 > -1 and
                               x1 < self.map_width and
                               y1 < self.map_height and
                               (x1-x)**2+(y1-y)**2 < (distance+0.5)**2 and
                               self.map[x1, y1] <= val_maximum and
                               self.map[x1, y1] >= val_minimum):
                                    self.map[x1, y1]=val_surround

    def gen(self,grid_scale=40):
        newmap = numpy.zeros((self.map_width,self.map_height))-100
        
        #seed water

        sea = self.convert_tuple_to_integer(WeightedCaveFactory(self.map_width,self.map_height,0.55).get_map())
        sea2 = gaussian_blur(sea,3)

        for x in range(0,self.map_width):
            for y in range(0,self.map_height):
                if(sea2[x][y] < 1.47):
                    self.map[x][y] = 0
                if(sea[x][y] == 0):
                    self.map[x][y] = 0

        for z in range(0,self.map_width*self.map_height/grid_scale/grid_scale):
            self.map[random.randint(0,self.map_width-1),random.randint(0,self.map_height-1)]=20

        self.surround(2,20,21,chance=0.3)
        self.surround(2,21,30)
        self.surround(1,30,31,chance=0.5)
        self.surround(1,0,1,10000,9,chance=0.4)
        self.surround(1,1,2,10000,9)

    def draw(self):

        surf = pygame.Surface((TILE_SIZE*self.map_width,TILE_SIZE*self.map_height))
        
        typedict = {
            0:8,  #deep water
            1:8,  #deep water
            2:5,  #water
            10:0, #grass
            31:2, #outer town
            30:10, #town
            20:9,#city innder
            21:7} #city

        for x in range(0,self.map_width):
            for y in range(0,self.map_height):
                surf.blit(self.tiles[typedict[self.map[x,y]]],(x*TILE_SIZE,y*TILE_SIZE),(0,0,TILE_SIZE,TILE_SIZE))

        return surf

delta = time()
m = Map_Chunk(400,400)
m.gen()

print "Gen Done",(time()-delta)
delta = time()

pygame.image.save(m.draw(),"sample.png")
print "Image Done",(time()-delta)
        
