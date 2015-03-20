import scipy.misc
from numpy import *
import random
import time
import hills
from functions import *

#
# Main function
#
def clouds(scale):

    #
    # Timekeeping
    #           
    wall = time.clock()
    wall2 = wall


    #
    # Large Boring Hills
    #
    a = zeros(( scale , scale ))
    Generate( a, 0)
    a = Matrix_Double( a )
    a = Matrix_Double( a )
    a = Gaussian_Blur( a, 2 )
    a = Matrix_Double( a )
    a = Matrix_Double( a )

    #print "Done Large Boring Hills",(time.clock()-wall)
    wall = time.clock()


    #
    # Little Boring Hills
    #
    b = zeros(( scale*4 , scale*4 ))
    Generate( b, 0 )
    b = Matrix_Double( b )
    b = Gaussian_Blur( b, 2 )
    b = Matrix_Double( b )

    #print "Done Little Boring Hills",(time.clock()-wall)
    wall = time.clock()


    #
    # Extra Noise
    #
    c = zeros(( scale*16 , scale*16 ))
    Generate( c, 0 )

    #print "Done Adding Noise",(time.clock()-wall)
    wall = time.clock()


    #
    # More Hills
    #
    d = zeros(( scale*16 , scale*16 ))
    Sparse_Hills_Basic(d , scale/2 , 20 )
    d = Gaussian_Blur( d, 32 )
    d = Matrix_Scale( d, 0, 100 )

    #print "Done Adding Hills",(time.clock()-wall)
    wall = time.clock()

    #
    # Finishing Up
    #
    k = 3 * a + 2 * b + c + 5 * d
    #scipy.misc.imsave( 'example1.png', Gaussian_Blur( k , 3 ) )
    
    Dome(k)
    k = Gaussian_Blur( k, 2 )
    k = Matrix_Scale( k, 0, 100 )

    #print "Done Blurring and Doming",(time.clock()-wall)
    wall = time.clock()

    #scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), k )
    print "Done Cloud",(time.clock()-wall2),'s'
    
    
    return k


scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(32))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(32))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(32))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(32))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(32))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(32))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(64))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(64))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(64))
scipy.misc.imsave( 'terrain_section_%d.png' % (time.clock() * 100 ), clouds(64))


