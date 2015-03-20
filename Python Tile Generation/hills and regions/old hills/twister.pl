from numpy import *
import random
import matplotlib.pyplot as plt

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

#random.seed(0)

scale = 20

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

def dome(amatrix,size):
    a = amatrix
    for x in range(0,size):
        for y in range(0,size):
            #a[x][y] = a[x][y]-sqrt(max((x-(size-1)/2)**2+(y-(size-1)/2)**2,(mini+maxi)*size/2))*(mini+maxi)/size
            a[x][y] = a[x][y]-sqrt(max((x-(size-1)/2)**2+(y-(size-1)/2)**2,(mini+maxi)*size/2))+210
            if(a[x][y] < mini):
                a[x][y]= mini
            elif (a[x][y] > maxi):
                a[x][y]= maxi
    return a

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

def snake(length,curvature,size,edge):
    a=zeros((size,size))
    startx = random.randint(0+edge,size-edge-1)
    starty = random.randint(0+edge,size-edge-1)
    startdirection = random.randint(0,360)
    centerdistance = sqrt((startx-(size-1)/2.0)**2+(starty-(size-1)/2.0)**2.0)
    centerangle = arctan(
        (startx-(size-1)/2.0)/
        (starty-(size-1)/2.0)
        )
    print startx, starty, centerdistance, centerangle
    a[startx][starty] = 1
    
    for x in range(0,length):
        startx = int(startx+sin(360-startdirection)*3)
        starty = int(starty+cos(360-startdirection)*3)
        
        startx=max(min(startx,size-1),0)
        starty=max(min(starty,size-1),0)
        
        a[startx][starty]=1
    return a

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
b = simplesmooth(b,scale*8)
b = doublematrix(b,scale*8)
b = doublematrix(b,scale*16)


c = zeros((scale*32,scale*32))
c = generate(c,scale*32,2)


d = ((a*6+b*3-c)/10)
print d[0][0]
print d[scale*16][scale*16]
d = gaussian(d,scale*32,8)

#for x in range(0,scale*8):
#    for y in range(0,scale*8):
#        if c[x][y] < 70:
#            c[x][y] = -100

#plt.imshow(snake(50,0,200,0))
plt.imshow(d)
plt.savefig('hill.png')