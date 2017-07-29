import xml.dom.minidom
import os, sys
from shimgeon.core.constantes import *
from shimgeon.sprite.spritetemplate import *
from pandac.PandaModules import * 
from panda3d.core import Texture

class Sprite(object):
	idcount=0
	listOfSprite={}
	listOfTexture={}
	def __init__(self,idtemplate):
		#~ print "Sprite :: __init__" + str(idtemplate)
		Sprite.idcount+=1
		self.id=Sprite.idcount
		self.path=""
		self.texture=None
		self.size=0
		self.node=None
		self.name=""
		self.nb=0
		self.pos=(0,0,0)
		self.hpr=(0,0,0)
		self.template=SpriteTemplate.getTemplate(idtemplate)
		self.createNode()	
		Sprite.listOfSprite[self.id]=self
		
	def createNode(self):
		self.node=loader.loadModel('plane')
		#~ print "Sprite::CreateNode" + str(self.template.getPath())
		if Sprite.listOfTexture.has_key(self.template.getPath()):
			self.texture=Sprite.listOfTexture[self.template.getPath()]
		else:
			self.texture=loader.loadTexture(self.template.getPath())
			Sprite.listOfTexture[self.template.getPath()]=self.texture
		self.node.reparentTo(render)
		self.node.setTransparency(1)  
		self.node.setTexture(self.texture)
		self.node.setHpr(self.template.getHpr())
		self.node.setScale(self.template.getScale())
		self.node.setTwoSided(True) 
		self.node.setName("Sprite#" + str(self.id))
		if self.template.getClickable()==1:
			self.node.setTag("id",str(self.id))
		
		
	def getTexture(self):
		return self.texture
	
	def setTextureModeRepeat(self):
		self.texture.setWrapU(Texture.WMRepeat)
		self.texture.setWrapV(Texture.WMRepeat)
	
	def setScale(self,scale):
		self.scale=scale
		self.node.setScale(scale)
		
	def getScale(self):
		return self.template.getScale()
		
	def getHeight(self):
		return self.template.getHeight()
		
	def getWidth(self):
		return self.template.getWidth()
		
	def isBlockable(self):
		return self.template.isBlockable()
		
	def getNb(self):
		return self.nb
		
	def setNb(self,nb):
		self.nb=nb
			
	def getPath(self):
		return self.template.getPath()
			
	def hide(self):
		self.pos=self.node.getPos()
		self.hpr=self.node.getHpr()
		self.destroy()
		
	def show(self):
		self.createNode()
		self.node.setPos(self.pos)
		self.node.setHpr(self.hpr)
	
	def setPos(self,pos):
		if self.template.getScale()==0.5:
			self.node.setPos(pos[0],pos[1]-0.5,pos[2])
		elif self.node.getH()==0 and self.node.getP()==0 and self.node.getR()==0 and self.template.getId()>10:
			self.node.setPos(pos[0],pos[1]+1.4,pos[2])
		else:
			self.node.setPos(pos)
		
	def getPos(self):
		return self.node.getPos()
		
	def getName(self):
		return self.template.getName()
		
	@staticmethod
	def getSprite(id):
		if Sprite.listOfSprite.has_key(id)==True:
			return Sprite.listOfSprite[id]
		return None
		
	def getHpr(self):
		return self.node.getHpr()
		
	def setHpr(self,hpr):
		self.node.setHpr(hpr)
		
	def destroy(self):
		self.node.detachNode()
		self.node.removeNode()
		#~ Sprite.listOfSprite.remove(self)
	
	def getNode(self):
		return self.node