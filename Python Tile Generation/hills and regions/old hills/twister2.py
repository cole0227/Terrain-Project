from numpy import *
import random
import matplotlib.pyplot as plt
from time import *

import hills

def myrandint(lower,upper):
    rand = random.randint(lower,upper)
    #rand = rand*rand/(lower+upper)*2
    rand = rand*rand/(lower+upper)/2+rand*3/4
    rand = lower+upper-rand
    rand = rand*rand/(lower+upper)+rand/2
    #rand = rand*rand/(lower+upper)+rand/2
    return int(rand)

def gaussian(amatrix, size, intensity):
    kernel = hills.gaussian_kernel(size, size, intensity)
    blur = hills.apply_kernel(size, size, amatrix, kernel)
    return blur


myseed = myrandint(0,9000)
random.seed(myseed)
print "Seed:", myseed

scale = 25

mini = 0
maxi = 100

def generate(amatrix,size,edge):
    a = amatrix
    for x in range(edge,size-edge):
        for y in range(edge,size-edge):
            #a[x][y]= random.gauss(1.5,0.5)
            a[x][y] = myrandint(mini,maxi)
            if (a[x][y] > maxi):
                a[x][y]= maxi
    return a

def domelegacy(amatrix,size):
    a = amatrix
    b=0.0
    for x in range(0,size):
        for y in range(0,size):
            b-=amatrix[x][y]
            a[x][y] = a[x][y]-sqrt(max(
                (x-(size-1)/2)**2+
                (y-(size-1)/2)**2,
                100*size/2))
            b+=amatrix[x][y]
    #print b/size**2
    return a-b/size**2

def dome(amatrix,size,parama,paramb):
    
    # Converts a relatively flat landscape into a dome-shaped island.
    # does not change the average elevation
    
    a = amatrix
    b=0.0
    for x in range(0,size):
        for y in range(0,size):
            b-=amatrix[x][y]
            a[x][y] -= max(sqrt(
                (x-(size-1)/2)**2+
                (y-(size-1)/2)**2),parama)*paramb/(size-1)
            b+=amatrix[x][y]
    #print b/size**2
    return a-b/size**2

def simplesmooth(amatrix,size):
    a = amatrix
    b = amatrix
    for x in range(1,size-1):
        for y in range(1,size-1):
            b[x][y] = ((a[x][y]*4+a[x-1][y-1]+a[x-1][y]+a[x-1][y+1]+a[x][y+1]+a[x+1][y+1]+a[x+1][y]+a[x+1][y-1]+a[x][y-1])/12)
    return a

def planes(amatrix,size):
    anothermatrix = amatrix
    for x in range(0,size):
        for y in range(0,size):
            
            if anothermatrix[x][y]< (maxi-mini)/4 :
                anothermatrix[x][y]+=(maxi-mini)/12
            elif anothermatrix[x][y]< (maxi-mini)/2 :
                anothermatrix[x][y]-=(maxi-mini)/12
            elif anothermatrix[x][y]< 3*(maxi-mini)/4 :
                anothermatrix[x][y]+=(maxi-mini)/12
            else :
                anothermatrix[x][y]-=(maxi-mini)/12
    return anothermatrix

def peaksandvalleys(amatrix,size):
    a = amatrix
    b = amatrix
    for x in range(1,size-1):
        for y in range(1,size-1):
            minimum = min(a[x-1][y-1],a[x-1][y],a[x-1][y+1],a[x][y+1],a[x+1][y+1],a[x+1][y],a[x+1][y-1],a[x][y-1])
            maximum = max(a[x-1][y-1],a[x-1][y],a[x-1][y+1],a[x][y+1],a[x+1][y+1],a[x+1][y],a[x+1][y-1],a[x][y-1])
            if(a[x][y] < minimum):
                b[x][y]= minimum
            elif (a[x][y] > maximum):
                b[x][y]= maximum
    return b

def stats(amatrix,size):
    stats = zeros(10)
    for x in range(0,size):
        for y in range(0,size):
            stats[amatrix[x][y]/10]+=1
    return stats

def rangestats(amatrix,size):
    stats = [100,0]
    for x in range(0,size):
        for y in range(0,size):
            stats[0]=min(stats[0],amatrix[x][y])
            stats[1]=max(stats[1],amatrix[x][y])
    return stats

def snake(length,curvature,size):
    a=zeros((size,size))
    startx = random.randint(size/4,size*3/4)
    starty = random.randint(size/4,size*3/4)
    #startdirection = random.uniform(0,math.pi*2)
    startdirection = 0
    for x in range(0,length):
                
        a[startx][starty]=5000
        
        startx = int(startx+sin(startdirection)*3)
        starty = int(starty+cos(startdirection)*3)
        
        startx=max(min(startx,size-1),0)
        starty=max(min(starty,size-1),0)
        
        startdirection += curvature/100.0
        
    return a

def minmax(amatrix,size,minimum,maximum):
    for x in range(0,size):
        for y in range(0,size):
            amatrix[x][y] = max(minimum,min(maximum,amatrix[x][y]))
    return amatrix

def minmax2(amatrix,size,minimum,maximum):
    
    # Forces a matrix to within set bounds
    
    rs=rangestats(amatrix,size)
    factor=(maximum-minimum)/(rs[1]-rs[0])
    
    amatrix = (amatrix-rs[0])*factor+minimum
    return amatrix

def doublematrix(alltheway,acrossthesky):
    a = alltheway
    b = zeros((acrossthesky*2,acrossthesky*2))
    for x in range(0,acrossthesky):
        for y in range(0,acrossthesky):
            b[2*x][2*y]=a[x][y]
            b[2*x+1][2*y]=a[x][y]
            b[2*x][2*y+1]=a[x][y]
            b[2*x+1][2*y+1]=a[x][y]
            
    return b

def fromto(amatrix,size,makethis,intothis):
    for x in range(0,size):
        for y in range(0,size):
            if (amatrix[x][y] == makethis) :
                amatrix[x][y] = intothis
    return amatrix

def safeislands():
    a = zeros((scale,scale))
    a = generate(a,scale,1)
    a = doublematrix(a,scale)
    a = simplesmooth(a,scale*2)
    a = doublematrix(a,scale*2)
    a = doublematrix(a,scale*4)
    a = simplesmooth(a,scale*8)
    a = doublematrix(a,scale*8)
    a = doublematrix(a,scale*16)
    a = dome(a,scale*32)
    
    
    b = zeros((scale*4,scale*4))
    b = generate(b,scale*4,1)
    b = doublematrix(b,scale*4)
    #b = gaussian(b,scale*8,3)
    b = simplesmooth(b,scale*8)
    b = doublematrix(b,scale*8)
    b = doublematrix(b,scale*16)
    b = dome(b,scale*32)
    
    
    c = zeros((scale*32,scale*32))
    c = generate(c,scale*32,2)
    
    
    d = (a*6+b*3-c)/9
    
    print rangestats(d,scale*32)
    
    for x in range(0,scale*32):
        for y in range(0,scale*32):
            if d[x][y] < 25:
                d[x][y] = -10
    
    d = gaussian(d,scale*32,3)
    
    return d


def heightmap():
    timetot = clock()
    time = clock()
    
    a = zeros((scale,scale))
    a = generate(a,scale,scale/8)
    a = doublematrix(a,scale)
    a = doublematrix(a,scale*2)
    a = simplesmooth(a,scale*4)
    a = doublematrix(a,scale*4)
    a = doublematrix(a,scale*8)
    a = simplesmooth(a,scale*16)
    a = doublematrix(a,scale*16)
    #a = dome(a,scale*32)
    
    print "Done Boring Large Hills		[",clock()-time,"s ]"
    
    time = clock()
    
    b = zeros((scale*4,scale*4))
    b = generate(b,scale*4,scale*3/5)
    b = doublematrix(b,scale*4)
    b = doublematrix(b,scale*8)
    b = simplesmooth(b,scale*16)
    b = doublematrix(b,scale*16)
    #b = dome(b,scale*32)
    print "Done Boring Little Hills	[",clock()-time,"s ]"
    
    time = clock()
    
    e =  snake(scale*10,-1,scale*32)
    e += snake(scale*10,1,scale*32)
    e +=  snake(scale*8,-3,scale*32)
    e += snake(scale*8,3,scale*32)
    e += snake(scale*6,-2,scale*32)
    e += snake(scale*6,2,scale*32)
    e = gaussian(e,scale*32,7)
    #print rangestats(e,scale*32)
    e = minmax(e,scale*32,0,80)
    print "Done Sneaky Snaking Ridges	[",clock()-time,"s ]"
    
    time = clock()
    
    d = (a*3+b+e*3)/7
    d = dome(d,scale*32,150,400)
    print "Done Doming the Earth		[",clock()-time,"s ]"
    
    time = clock()
    
    #print rangestats(d,scale*32)
    d = minmax2(d,scale*32,-300,200)
    d = minmax(d,scale*32,0,200)
    d = fromto(d,scale*32,0,-50)
    d = gaussian(d,scale*32,3)
    print "Done Smoothing and Everything	[",clock()-time,"s ]"
    print "Total Time: 			[",clock()-timetot,"s ]"
    
    #plt.imshow(e)
    #plt.savefig('hill_chains.png')
    plt.imshow(d)
    plt.savefig('sample_%d.svg' % myseed,bbox_inches='tight', pad_inches=0)
    return d

