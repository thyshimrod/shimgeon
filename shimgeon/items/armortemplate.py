import xml.dom.minidom
import os, sys
from shimgeon.core.constantes import *
from shimgeon.items.itemtemplate import *

class ArmorTemplate(ItemTemplate):
	listOfTemplate={}
	def __init__(self,xmlPart):
		super(ArmorTemplate,self).__init__(xmlPart)		
		self.armor=int(xmlPart.getElementsByTagName('armor')[0].firstChild.data)
		ArmorTemplate.listOfTemplate[self.id]=self
		
	def getArmor(self):
		return self.armor
			
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/items.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			typeItem=int(i.getElementsByTagName('typeitem')[0].firstChild.data)
			if typeItem==C_ITEM_ARMOR:
				ArmorTemplate(i)
			
	@staticmethod
	def getTemplate(idTemplate):
		print "weapontemplate::getTEmplate" + str(idTemplate)
		if len(ArmorTemplate.listOfTemplate)==0:
			ArmorTemplate.loadXml()
		if ArmorTemplate.listOfTemplate.has_key(idTemplate)==True:
			return ArmorTemplate.listOfTemplate[idTemplate]
			
		return None