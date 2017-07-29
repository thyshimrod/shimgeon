import xml.dom.minidom
import os, sys

class FX:
	listOfFx={}
	def __init__(self,xmlPart):
		self.name=str(xmlPart.getElementsByTagName('name')[0].firstChild.data)
		self.id=int(xmlPart.getElementsByTagName('id')[0].firstChild.data)
		self.path=str(xmlPart.getElementsByTagName('path')[0].firstChild.data)
		self.extension=str(xmlPart.getElementsByTagName('extension')[0].firstChild.data)
		self.nbAnimation=int(xmlPart.getElementsByTagName('nbanimation')[0].firstChild.data)
		FX.listOfFx[self.id]=self
		
	@staticmethod
	def loadXml():
		dom = xml.dom.minidom.parse("config/fx.xml")
		it=dom.getElementsByTagName('fx')
		for i in it:
			#~ typeitem=int(i.getElementsByTagName('fx')[0].firstChild.data)
			FX(i)
			
	@staticmethod
	def getFx(id):
		if len(FX.listOfFx)==0:
			FX.loadXml()
		if FX.listOfFx.has_key(id)==True:
			return FX.listOfFx[id]
		else:
			return None
			
	def getName(self):
		return self.name
		
	def getId(self):
		return self.id
		
	def getPath(self):
		return self.path
		
	def getExtension(self):
		return self.extension
		
	def getNbAnimation(self):
		return self.nbAnimation