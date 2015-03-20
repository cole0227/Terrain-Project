from PIL import Image


class SpriteSheetReader:
 
	def __init__(self, imageName, tileSize):
		self.spritesheet = Image.open(imageName)
		self.tileSize = tileSize
		self.margin = 0
	
	def getTile(self, tileX, tileY):
		posX = (self.tileSize * tileX) + (self.margin * (tileX + 1))
		posY = (self.tileSize * tileY) + (self.margin * (tileY + 1))
		box = (posX, posY, posX + self.tileSize, posY + self.tileSize)
		return self.spritesheet.crop(box)
	
class SpriteSheetWriter:
	
	def __init__(self, tileSize, spriteSheetSize):
		self.tileSize = tileSize
		self.spriteSheetSize = spriteSheetSize
		self.spritesheet = Image.new("RGBA", (self.spriteSheetSize, self.spriteSheetSize), (0,0,0,0))
		self.tileX = 0
		self.tileY = 0
		self.margin = 0
	
	def getCurPos(self):
		self.posX = (self.tileSize * self.tileX) + (self.margin * (self.tileX + 1))
		self.posY = (self.tileSize * self.tileY) + (self.margin * (self.tileY + 1))
		if (self.posX + self.tileSize > self.spriteSheetSize):
			self.tileX = 0
			self.tileY = self.tileY + 1
			self.getCurPos()
		if (self.posY + self.tileSize > self.spriteSheetSize):
			raise Exception('Image does not fit within spritesheet!')
	
	def addImage(self, image):
		self.getCurPos()		
		destBox = (self.posX, self.posY, self.posX + image.size[0], self.posY + image.size[1])
		self.spritesheet.paste(image, destBox)
		self.tileX = self.tileX + 1
	
	def show(self):
		self.spritesheet.show()
		
	def addImageAndRotations(self, image):
		self.addImage(image)
		image = image.rotate(90)
		self.addImage(image)
		image = image.rotate(90)
		self.addImage(image)
		image = image.rotate(90)
		self.addImage(image)
	 
	def save(self, imageName):
		self.spritesheet.save(imageName)
