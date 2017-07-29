import xml.dom.minidom
import os, sys

from shimgeon.core.constantes import *
class ItemTemplate(object):
	listOfTemplate={}
	def __init__(self,xmlPart):
		self.id=int(xmlPart.getElementsByTagName('id')[0].firstChild.data)
		self.typeItem=int(xmlPart.getElementsByTagName('typeitem')[0].firstChild.data)
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.icon=str(xmlPart.getElementsByTagName('icon')[0].firstChild.data)
		self.suitable=int(xmlPart.getElementsByTagName('suitable')[0].firstChild.data)
		self.force=self.dexterite=self.constitution=self.chance=self.intelligence=0
		self.level=int(xmlPart.getElementsByTagName('level')[0].firstChild.data)
		if xmlPart.getElementsByTagName('force')!=None and len(xmlPart.getElementsByTagName('force'))>0:
			self.force=int(xmlPart.getElementsByTagName('force')[0].firstChild.data)
		if xmlPart.getElementsByTagName('constitution')!=None and len(xmlPart.getElementsByTagName('constitution'))>0:
			self.constitution=int(xmlPart.getElementsByTagName('constitution')[0].firstChild.data) 
		if xmlPart.getElementsByTagName('dexterite')!=None and len(xmlPart.getElementsByTagName('dexterite'))>0:
			self.dexterite=int(xmlPart.getElementsByTagName('dexterite')[0].firstChild.data)
		if xmlPart.getElementsByTagName('chance')!=None and len(xmlPart.getElementsByTagName('chance'))>0:
			self.chance=int(xmlPart.getElementsByTagName('chance')[0].firstChild.data)
		if xmlPart.getElementsByTagName('intelligence')!=None and len(xmlPart.getElementsByTagName('intelligence'))>0:
			self.intelligence=int(xmlPart.getElementsByTagName('intelligence')[0].firstChild.data)
		
	def getLevel(self):
		return self.level
		
	def getCaract(self):
		return self.force,self.dexterite,self.constitution,self.intelligence,self.chance
		
	def getSuitable(self):
		return self.suitable
		
	def getId(self):
		return self.id
		
	def getIcon(self):
		return self.icon
		
	def getName(self):
		return self.name
		
	def getTypeItem(self):
		return self.typeItem
		
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/items.xml")
		it=dom.getElementsByTagName('item')
		for i in it:
			item=ItemTemplate(i)
			ItemTemplate.listOfTemplate[item.getId()]=item
		
	@staticmethod
	def getTemplates():
		return ItemTemplate.listOfTemplate
		
			
	@staticmethod
	def getTemplate(idTemplate):
		if len(ItemTemplate.listOfTemplate)==0:
			ItemTemplate.loadXml()
		if ItemTemplate.listOfTemplate.has_key(idTemplate)==True:
			return ItemTemplate.listOfTemplate[idTemplate]
		return None
		
	@staticmethod
	def getItemByLevel(level):
		level+=1
		listOfTemplate=[]
		if len(ItemTemplate.listOfTemplate)==0:
			ItemTemplate.loadXml()
		for it in ItemTemplate.listOfTemplate:
			if ItemTemplate.listOfTemplate[it].getLevel()>=(level-3) and ItemTemplate.listOfTemplate[it].getLevel()<=level:
				listOfTemplate.append(ItemTemplate.listOfTemplate[it])
		return listOfTemplate
		