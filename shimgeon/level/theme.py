import xml.dom.minidom
import os, sys
from shimgeon.sprite.sprite import *
from shimgeon.sprite.spritetemplate import *
import random


class Theme:
	listOfTheme={}
	def __init__(self,xmlPart):
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.id=int(xmlPart.getElementsByTagName('id')[0].firstChild.data)
		skillItems=xmlPart.getElementsByTagName('skillitem')
		self.sprite=[]
		sp=xmlPart.getElementsByTagName('idsprite')
		for s in sp:
			self.sprite.append(int(s.firstChild.data))
		Theme.listOfTheme[self.id]=self
		
	def getRandomSprite(self):
		nb=random.randint(0,len(self.sprite))
		i=0
		for k in self.sprite:
			if i==nb:
				i=k
				break
			i+=1
		return Sprite(i)
		
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/themeset.xml")
		it=dom.getElementsByTagName('theme')
		for i in it:
			Theme(i)

	@staticmethod
	def getTheme(id):
		if len(Theme.listOfTheme)==0:
			Theme.loadXml()
		if Theme.listOfTheme.has_key(id)==True:
			return Theme.listOfTheme[id]
		return None
		
	@staticmethod
	def getListOfTheme():
		if len(Theme.listOfTheme)==0:
			Theme.loadXml()
		return Theme.listOfTheme
		