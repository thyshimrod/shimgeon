import xml.dom.minidom
import os, sys

from shimgeon.core.constantes import *

class SpriteTemplate():
	listOfTemplate={}
	def __init__(self,xmlPart):
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.path=xmlPart.getElementsByTagName('path')[0].firstChild.data
		self.id=int(xmlPart.getElementsByTagName('id')[0].firstChild.data)
		h=int(xmlPart.getElementsByTagName('h')[0].firstChild.data)
		p=int(xmlPart.getElementsByTagName('p')[0].firstChild.data)
		r=int(xmlPart.getElementsByTagName('r')[0].firstChild.data)
		self.height=float(xmlPart.getElementsByTagName('height')[0].firstChild.data)
		self.width=float(xmlPart.getElementsByTagName('width')[0].firstChild.data)
		self.clickable=int(xmlPart.getElementsByTagName('clickable')[0].firstChild.data)
		self.blockable=int(xmlPart.getElementsByTagName('blockable')[0].firstChild.data)
		self.hpr=(h,p,r)
		self.scale=float(xmlPart.getElementsByTagName('scale')[0].firstChild.data)
		SpriteTemplate.listOfTemplate[self.id]=self
	
	def getId(self):
		return self.id
	
	def getHeight(self):
		return self.height
		
	def getWidth(self):
		return self.width
	
	def getPath(self):
		return  self.path
		
	def getName(self):
		return self.name
		
	def getHpr(self):
		return self.hpr
		
	def getScale(self):
		return self.scale
		
	def isBlockable(self):
		return self.blockable
		
	def getClickable(self):
		return self.clickable
	
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/sprites.xml")
		it=dom.getElementsByTagName('sprite')
		for i in it:
			SpriteTemplate(i)
			
	@staticmethod
	def getTemplate(idTemplate):
		if len(SpriteTemplate.listOfTemplate)==0:
			SpriteTemplate.loadXml()
		if SpriteTemplate.listOfTemplate.has_key(idTemplate)==True:
			return SpriteTemplate.listOfTemplate[idTemplate]
			
		return None

	