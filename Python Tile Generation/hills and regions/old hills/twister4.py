import scipy
from numpy import *
import random
import matplotlib.pyplot as plt
#import wx
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


scale = 16

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
    
    # Converts a relatively flat landscape into a dome-shaped island.
    # does not change the average elevation
    
    #min1=0
    #min2=0
    #max1=0
    #max2=0
    b=0.0
    
    for x in range(0,size):
        for y in range(0,size):
            b-=amatrix[x][y]
            
	    #if(sqrt((x-(size-1)/2)**2+(y-(size-1)/2)**2)<8*scale):
	    #	max1+=1
	    #else:
	    #	max2+=1
	    #if(sqrt((x-(size-1)/2)**2+(y-(size-1)/2)**2)>16*scale):
	    #	min1+=1
	    #else:
	    #	min2+=1
	    
            c = min(max(sqrt(
                (x-(size-1)/2)**2+
                (y-(size-1)/2)**2),8*scale),16*scale)*20/scale
            amatrix[x][y] -= c           
    
            b+=amatrix[x][y]
            #print c
    
    #print "Average b =",b/size**2
    #print 1.0*max1/max2,1.0*min1/min2
    return amatrix-b/size**2

def stats(amatrix,size):
    stats = zeros(10)
    myrange = rangestats(amatrix,size)
    rng = (myrange[1]-myrange[0])/10
    for x in range(0,size):
        for y in range(0,size):
            stats[amatrix[x][y]/rng]+=1
    return stats

def rangestats(amatrix,size):
    stats = [100,0]
    for x in range(0,size):
        for y in range(0,size):
            stats[0]=min(stats[0],amatrix[x][y])
            stats[1]=max(stats[1],amatrix[x][y])
    return stats

def snake(length,curvature,quadrant):
    a=zeros((scale*32,scale*32))
    startx = random.randint(scale*4,scale*16)+quadrant%2*scale*12
    starty = random.randint(scale*4,scale*16)+quadrant/2*scale*12
    startdirection = random.uniform(0,math.pi*2)
    for x in range(0,length):
                
        a[startx][starty]=2000
        
        startx = int(startx+sin(startdirection)*3)
        starty = int(starty+cos(startdirection)*3)
        
        startx=max(min(startx,scale*32-1),0)
        starty=max(min(starty,scale*32-1),0)
        
        if( x*2 > length ):
            startdirection -= curvature/(4.0*scale)
        else:
            startdirection += curvature/(4.0*scale)
        
    return a

def crop(amatrix,size,minimum,maximum):
    for x in range(0,size):
        for y in range(0,size):
            amatrix[x][y] = max(minimum,min(maximum,amatrix[x][y]))
    return amatrix

def minmax(amatrix,size,minimum,maximum):
    
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

def erode(amatrix,size,iter,rainfall,sedimentation,evaporation):

    terrain = amatrix
    total = 0
    water = zeros((size,size))
    sediment = zeros((size,size))
    def move_things(x,y,x1,y1):
        
        x1%=size
        y1%=size
    	diff = 0
    	if( water[x][y] > 0):

    	    diff = max(min(water[x][y],(terrain[x][y]+water[x][y]+sediment[x][y] - terrain[x1][y1]-water[x1][y1]-sediment[x1][y1])/2),0)
    	    #print diff
    	    sediment[x1][y1] += diff*sediment[x][y]/water[x][y]
    	    sediment[x ][y ] -= diff*sediment[x][y]/water[x][y]
    	    water[x ][y ] -= diff
    	    water[x1][y1] += diff

	else:
	    water[x][y]    /= 2
	    sediment[x][y] /= 2

    	return diff

    rand = 1000
    for z in range(0,iter):

	water+=rainfall
	for x in range(0,size):

	    #scipy.misc.imsave('dirt_%d.png' %(rand),sediment)
	    #scipy.misc.imsave('water_%d.png' %(rand),water)
	    rand+=1

	    for y in range(0,size):

	        terrain[x][y] -=sedimentation*water[x][y]
	        sediment[x][y]+=sedimentation*water[x][y]
	    	total += move_things(x,y,x-1,y  )
	    	total += move_things(x,y,x  ,y-1)
	    	total += move_things(x,y,x+1,y  )
	    	total += move_things(x,y,x  ,y+1)
		
    	water=water*(1-evaporation)
	sediment = clear_edges(sediment,size)
	water = clear_edges(water,size)

    print total/size/size
    scipy.misc.imsave('sediment.png',sediment)
    scipy.misc.imsave('water.png',water)
    print rangestats(terrain,size)
    print rangestats(sediment,size)
    print rangestats(water,size)
    return terrain+sediment


def clear_edges(amatrix,size):
    for x in range(0,size):
	amatrix[x][0]=amatrix[x][3]
	amatrix[x][1]=amatrix[x][3]
	amatrix[x][2]=amatrix[x][3]
	amatrix[x][size-1]=amatrix[x][size-4]
	amatrix[x][size-2]=amatrix[x][size-4]
	amatrix[x][size-3]=amatrix[x][size-4]
    for y in range(0,size):    
	amatrix[size-1][y]=amatrix[size-4][y]
	amatrix[size-2][y]=amatrix[size-4][y]
	amatrix[size-3][y]=amatrix[size-4][y]
    return amatrix


def heightmap():
    myseed = myrandint(0,9000)
    #myseed = 4
    random.seed(myseed)
    print "Seed:", myseed

    timetot = clock()
    time = clock()
    
    a = zeros((scale,scale))
    a = generate(a,scale,scale/10)
    a = doublematrix(a,scale)
    a = doublematrix(a,scale*2)
    a = doublematrix(a,scale*4)
    a = gaussian(a,scale*8,5)
    a = doublematrix(a,scale*8)
    a = doublematrix(a,scale*16)
    #print rangestats(a,scale*32)
    print "Done Boring Large Hills:	[",clock()-time,"s ]"
    
    time = clock()
    
    b = zeros((scale*8,scale*8))
    b = generate(b,scale*8,scale*1/2)
    b = doublematrix(b,scale*8)
    b = gaussian(b,scale*16,2)
    b = doublematrix(b,scale*16)
    #print rangestats(b,scale*32)
    print "Done Boring Little Hills:	[",clock()-time,"s ]"
    
    
    time = clock()
    
    c = zeros((scale*32,scale*32))
    c = generate(b,scale*32,scale*2)
    print "Done Boring Tiny Deviations:	[",clock()-time,"s ]"

    time = clock()
    
    e =  snake(scale*10,-2,0)
    e += snake(scale*10,2,3)
    if(scale>19):
    	e += snake(scale*8,-1,2)
    	e += snake(scale*8,1,1)
    e = gaussian(e,scale*32,7)
    e = crop(e,scale*32,0,38)
    e = minmax(e,scale*32,0,80)
    #print rangestats(e,scale*32)
    print "Done Sneaky Snaking Ridges:	[",clock()-time,"s ]"
    
    time = clock()
    
    #d = (a*4+b+e*3)/8
    #d = (a*4+b+e*3)/8 + dome(d,scale*32)
    d = 2*a+2*b+c+4*dome(2*a+e,scale*32)
    #d = dome(zeros((scale*32,scale*32)),scale*32)+b
    print "Done Doming the Earth:		[",clock()-time,"s ]"
    
    time = clock()
    
    #print rangestats(d,scale*32)
    d = minmax(d,scale*32,-200,250)
    d = crop(d,scale*32,0,200)
    #d = fromto(d,scale*32,0,-50)
    d = gaussian(d,scale*32,2)
    print "Done Smoothing			[",clock()-time,"s ]"
    
    scipy.misc.imsave('before_%d.png' %scale,d)
    
    #print stats(d,scale*32)
    print rangestats(d,scale*32)
    d = erode(d,scale*32,2,100,0.7,0.5)
    d = clear_edges(d,scale*32)
    #print stats(d,scale*32)
    d = crop(d,scale*32,0,225)
    #d = gaussian(d,scale*32,2)
    print rangestats(d,scale*32)
    
    scipy.misc.imsave('after_%d.png' %scale,d)

    #fig = plt.figure()    
    #plt.imshow(d)
    #fig.set_size_inches(5,5)
    #fig.savefig('hills_%d.png' % scale,bbox_inches='tight', pad_inches=0)
    ##fig.savefig('%d_%d.png' % (scale,myseed),bbox_inches='tight', pad_inches=0)
    ##fig.savefig('%d.png' % myseed),bbox_inches='tight', pad_inches=0)
    
    
    print "Done Erosion			[",clock()-time,"s ]"
    print "Total Time: 			[",clock()-timetot,"s ]"
    print "-------------------------------------------"
    return d

scale=8
heightmap()
#scale=20
#heightmap()

#savetxt('txt.txt',heightmap(),fmt='%12.6G')
#for x in range(12,26):
#    scale=x
#    heightmap()
