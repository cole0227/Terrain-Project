import pygame
import random


# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)
 
class Sprite_Sheet(object):
    def __init__(self, filename,conversion=None):
        try:
            if(conversion == None):
                self.sheet = pygame.image.load(filename).convert()
                self.alpha = False;
                
            elif(conversion == "Alpha"):
                self.sheet = pygame.image.load(filename).convert_alpha()
                self.alpha = True;

        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        if(self.alpha == True):
            image = pygame.Surface(rect.size).convert_alpha()
        else:
            image = pygame.Surface(rect.size).convert()

        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    #Load an image given a valid index
    def image_by_index(self, size, index, colorkey = None):
        numcols = self.sheet.get_width() / size;
        return self.image_at((index % numcols * size,
                              index / numcols * size,
                              size,
                              size), colorkey)
        
    #Load an image given valid coords
    def image_by_coords(self, size, x, y, colorkey = None):
        self.image_by_index(self, size, x+y*self.sheet.get_width() / size, colorkey)

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

