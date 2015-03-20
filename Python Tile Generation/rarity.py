from multiprocessing import Process, Queue
from random import *
import time
import sys

from numpy import *



rarity = ('common','uncommon','rare','mythical')


def getItem():

    prob = random.random()

    if(prob > 0.4):
        return 0 # common 60%

    elif(prob > 0.11):
        return 1 #uncommon 29%

    elif(prob > 0.01):
        return 2 #rare 10%

    else:
        return 3 #mythical 1%


# takes every item in an array, and produces
# an array 1/2 that size, 
def combine(amatrix):

    size = int( amatrix.size )
    another = zeros((size/2))

    for x in range(size/2):

        y = x+size/2
     
        if(random.random() < 0.95):
            
            if(amatrix[x] >= amatrix[y]):
                
                another[x] = amatrix[x]
            else:
                
                another[x] = amatrix[y]
        else:
            
            if(amatrix[x] >= amatrix[y] ):
                
                another[x] = amatrix[y]
            else:
                
                another[x] = amatrix[x]
                
    return another


size = 16384 * 50
item = zeros((size))

for x in range(size):
    item[x] = getItem()

items = item
itemSorted = sort(item)
print 1, histogram(item,4)[0]*1.0/item.size,"{", itemSorted[0],",",itemSorted[itemSorted.size-1],"}"

for x in range(9):
    
    items = combine(items)
    itemsSorted = sort(items)
    print 2 ** (x+1), histogram(items,4)[0]*1.0/items.size,
    print "{", itemsSorted[0],",",itemsSorted[itemsSorted.size-1],'} (',
    print items.size,', $',2 ** (x+1) * 0.03 + 2.49,"}"

#print items
