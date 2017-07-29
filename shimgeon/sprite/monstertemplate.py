import xml.dom.minidom
import os, sys

from shimgeon.core.constantes import *
from shimgeon.sprite.sprite import *
from shimgeon.sprite.personatemplate import *

class MonsterTemplate(PersonaTemplate):
	listOfTemplate={}
	def __init__(self,xmlPart):
		super(MonsterTemplate,self).__init__(xmlPart)
		drops=xmlPart.getElementsByTagName('loot')
		self.loots={}
		for d in drops:
			id=int(d.getElementsByTagName('iditem')[0].firstChild.data)
			prcent=int(d.getElementsByTagName('prcent')[0].firstChild.data)
			self.loots[id]=prcent
		MonsterTemplate.listOfTemplate[self.id]=self
		self.width=1
		self.height=1
		self.nbAnimation=int(xmlPart.getElementsByTagName('nbanimation')[0].firstChild.data)
		self.armor=int(xmlPart.getElementsByTagName('armor')[0].firstChild.data)
		self.classe=int(xmlPart.getElementsByTagName('class')[0].firstChild.data)
		
	def getClasse(self):
		return self.classe
	
	def getArmor(self):
		return self.armor
		
	def getLoots(self):
		return self.loots
		
	def getWidth(self):
		return self.width
		
	def getHeight(self):
		return self.height
	
	def getNbAnimation(self):
		return self.nbAnimation
		
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/monster.xml")
		it=dom.getElementsByTagName('monster')
		for i in it:
			MonsterTemplate(i)
			
	@staticmethod
	def getTemplate(idTemplate):
		if len(MonsterTemplate.listOfTemplate)==0:
			MonsterTemplate.loadXml()
		if MonsterTemplate.listOfTemplate.has_key(idTemplate)==True:
			return MonsterTemplate.listOfTemplate[idTemplate]
			
		return None

	