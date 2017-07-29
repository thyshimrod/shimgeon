import xml.dom.minidom
import os, sys
from shimgeon.core.constantes import *
from shimgeon.items.itemtemplate import *

class WeaponTemplate(ItemTemplate):
	listOfTemplate={}
	def __init__(self,xmlPart):
		super(WeaponTemplate,self).__init__(xmlPart)
		self.range=int(xmlPart.getElementsByTagName('range')[0].firstChild.data)
		self.degatMin=int(xmlPart.getElementsByTagName('degatmin')[0].firstChild.data)
		self.degatMax=int(xmlPart.getElementsByTagName('degatmax')[0].firstChild.data)
		self.subType=int(xmlPart.getElementsByTagName('subtype')[0].firstChild.data)
		self.vitesse=float(xmlPart.getElementsByTagName('vitesse')[0].firstChild.data)
		WeaponTemplate.listOfTemplate[self.id]=self
	
	def getVitesse(self):
		return self.vitesse
		
	def getSubType(self):
		return self.subType
		
	def getDegatMin(self):
		return self.degatMin
		
	def getDegatMax(self):
		return self.degatMax
		
	def getRange(self):
		return self.range
		
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/items.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			typeItem=int(i.getElementsByTagName('typeitem')[0].firstChild.data)
			if typeItem==C_ITEM_WEAPON:
				WeaponTemplate(i)
			
	@staticmethod
	def getTemplate(idTemplate):
		if len(WeaponTemplate.listOfTemplate)==0:
			WeaponTemplate.loadXml()
		if WeaponTemplate.listOfTemplate.has_key(idTemplate)==True:
			return WeaponTemplate.listOfTemplate[idTemplate]
			
		return None