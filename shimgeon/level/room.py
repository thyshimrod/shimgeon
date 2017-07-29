from shimgeon.sprite.sprite import *
from shimgeon.level.theme import *
import random
from math import sqrt

class Room():
	def __init__(self,x,y,pos,idSprite,corridor=False):
		self.x=x
		self.y=y
		self.pos=pos
		self.corridor=corridor
		#~ self.texture=loader.loadTexture(texture)
		self.idSprite=idSprite
		self.dalles=[]
		self.gates=[]
		self.wayTo=[]
		self.decors=[]
		self.loadGround()
		#~ self.generateWall()
		if self.corridor==False:
			listOfTheme=Theme.getListOfTheme()
			
			nb=random.randint(0,len(listOfTheme))
			i=0
			for k in listOfTheme.keys():
				if i==nb:
					i=k
					break
				i+=1
			self.theme=Theme.getTheme(i)
			
			self.loadDecor()
			
	def appendGate(self,gate):
		self.gates.append(gate)
		
	def destroy(self):
		for d in self.dalles:
			d.destroy()
		for d in self.decors:
			d.destroy()
		
	def getDecors(self):
		return self.decors
		
	def loadDecor(self):
		nb=round(sqrt(self.x*self.y))
		nbDecor=random.randint(int(nb/4),round(nb/2,0))
		for i in range(nbDecor):
			x=random.uniform(1,self.x-1)
			z=random.uniform(1,self.y-1)
			decor=self.theme.getRandomSprite()
			#~ decor=Sprite(48)
			decor.setPos((self.pos.getX()+x,99.99-(decor.getScale()-0.5),self.pos.getZ()+z))
			#~ decor.setHpr((180,180,180))
			#~ decor.node.setScale(-1)
			self.decors.append(decor)
		
	def hide(self):
		for d in self.dalles:
			d.hide()
		for d in self.decors:
			d.hide()
			
	def show(self):
		for d in self.dalles:
			d.show()
		for d in self.decors:
			d.show()
		
	def loadGround(self):
		#~ s=Sprite(self.idSprite)
		#~ s.setPos((self.pos.getX(),self.pos.getY(),self.pos.getZ()))                
		#~ s.setScale(self.x*self.y)
		#~ s.setTextureModeRepeat()
		for i in range(self.x):
			for j in range(self.y):
				s=Sprite(self.idSprite)
				s.setPos((i+self.pos.getX(),self.pos.getY(),j+self.pos.getZ()))                
				self.dalles.append(s)
		
	def generateWall(self):
		if self.corridor==False:
			for i in range(self.x):
				for g in self.gates:
					if ((g.getPos().getX()-1)>=(i+self.pos.getX())  or  (g.getPos().getX()+1)<(i+self.pos.getX())) or g.getPos().getZ()!=(self.pos.getZ()-0.5+self.y):
						s=Sprite(self.idSprite)
						s.setPos((i+self.pos.getX(),self.pos.getY()-0.5,self.pos.getZ()-0.5+self.y))                
						s.setHpr((0,90,0))
						self.dalles.append(s)
						s=Sprite(self.idSprite)
						s.setPos((i+self.pos.getX(),self.pos.getY()-1.5,self.pos.getZ()-0.5+self.y))
						s.setHpr((0,90,0))
						self.dalles.append(s)
			
			for i in range(self.y):
				for g in self.gates:
					if ((g.getPos().getZ()-1)>=(i+self.pos.getZ())  or  (g.getPos().getZ()+1)<(i+self.pos.getZ())) or g.getPos().getX()!=(self.pos.getX()-0.5+self.x):
						s=Sprite(self.idSprite)
						s.setPos((self.pos.getX()+self.x-0.5,self.pos.getY()-0.5,self.pos.getZ()+i))                
						s.setHpr((90,0,90))
						self.dalles.append(s)
						s=Sprite(self.idSprite)
						s.setPos((self.pos.getX()+self.x-0.5,self.pos.getY()-1.5,self.pos.getZ()+i))                
						s.setHpr((90,0,90))
						self.dalles.append(s)
	
				
	def addWayToRoom(self,room):
		self.wayTo.append(room)
		
	def getWayTo(self):
		return self.way
				
	def getPos(self):
		return self.pos
		
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def hasWayTo(self,room):
		for r in self.wayTo:
			if r==room:
				return True
		return False
		