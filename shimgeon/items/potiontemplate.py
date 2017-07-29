import xml.dom.minidom
import os, sys
from shimgeon.core.constantes import *
from shimgeon.items.itemtemplate import *

class PotionTemplate(ItemTemplate):
	listOfTemplate={}
	def __init__(self,xmlPart):
		super(PotionTemplate,self).__init__(xmlPart)		
		self.life=int(xmlPart.getElementsByTagName('life')[0].firstChild.data)
		self.subType=int(xmlPart.getElementsByTagName('subtype')[0].firstChild.data)
		PotionTemplate.listOfTemplate[self.id]=self
		
	def getSubType(self):
		return self.subType
		
	def getLife(self):
		return self.life
			
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/items.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			typeItem=int(i.getElementsByTagName('typeitem')[0].firstChild.data)
			if typeItem==C_ITEM_POTION:
				PotionTemplate(i)
			
	@staticmethod
	def getTemplate(idTemplate):
		if len(PotionTemplate.listOfTemplate)==0:
			PotionTemplate.loadXml()
		if PotionTemplate.listOfTemplate.has_key(idTemplate)==True:
			return PotionTemplate.listOfTemplate[idTemplate]
			
		return None