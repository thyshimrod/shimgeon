import xml.dom.minidom
import os, sys

from shimgeon.core.constantes import *
from shimgeon.sprite.sprite import *

class PersonaTemplate(object):
	listOfTemplate={}
	def __init__(self,xmlPart):
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.path=xmlPart.getElementsByTagName('path')[0].firstChild.data
		self.id=int(xmlPart.getElementsByTagName('id')[0].firstChild.data)
		self.constitution=int(xmlPart.getElementsByTagName('constitution')[0].firstChild.data)
		self.force=int(xmlPart.getElementsByTagName('force')[0].firstChild.data)
		self.sagesse=int(xmlPart.getElementsByTagName('sagesse')[0].firstChild.data)
		self.dexterite=int(xmlPart.getElementsByTagName('dexterite')[0].firstChild.data)
		self.chance=int(xmlPart.getElementsByTagName('chance')[0].firstChild.data)
		self.items={}
		items=xmlPart.getElementsByTagName('item')
		for it in items:
			id=int(it.getElementsByTagName('iditem')[0].firstChild.data)
			equipe=int(it.getElementsByTagName('equipe')[0].firstChild.data)
			self.items[id]=equipe
		PersonaTemplate.listOfTemplate[self.id]=self
	
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
	def loadXml(file):
		dom = xml.dom.minidom.parse("config/" + file  + ".xml")
		it=dom.getElementsByTagName(file)
		for i in it:
			CharacterTemplate(i)
			
	@staticmethod
	def getTemplate(idTemplate,file):
		if len(CharacterTemplate.listOfTemplate)==0:
			CharacterTemplate.loadXml(file)
		if CharacterTemplate.listOfTemplate.has_key(idTemplate)==True:
			return CharacterTemplate.listOfTemplate[idTemplate]
			
		return None

	@staticmethod
	def getListOfTemplate():
		if len(CharacterTemplate.listOfTemplate)==0:
			CharacterTemplate.loadXml()
		return CharacterTemplate.listOfTemplate
	