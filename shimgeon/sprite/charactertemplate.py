import xml.dom.minidom
import os, sys


from shimgeon.core.constantes import *
from shimgeon.sprite.sprite import *
from shimgeon.sprite.personatemplate import *

class CharacterTemplate(PersonaTemplate):
	listOfTemplate={}
	def __init__(self,xmlPart):
		super(CharacterTemplate,self).__init__(xmlPart)
		CharacterTemplate.listOfTemplate[self.id]=self
	
	def getItems(self):
		return self.items
	
	def getCaract(self):
		return self.force,self.dexterite,self.constitution,self.sagesse,self.chance
	
	def getPath(self):
		return  self.path
		
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
	
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/character.xml")
		it=dom.getElementsByTagName('character')
		for i in it:
			CharacterTemplate(i)
			
	@staticmethod
	def getTemplate(idTemplate):
		if len(CharacterTemplate.listOfTemplate)==0:
			CharacterTemplate.loadXml()
		if CharacterTemplate.listOfTemplate.has_key(idTemplate)==True:
			return CharacterTemplate.listOfTemplate[idTemplate]
			
		return None

	@staticmethod
	def getListOfTemplate():
		if len(CharacterTemplate.listOfTemplate)==0:
			CharacterTemplate.loadXml()
		return CharacterTemplate.listOfTemplate
	