from shimgeon.items.itemtemplate import *
import random 

class Item(object):
	idcount=0
	listOfItem={}
	def __init__(self,idtemplate):
		Item.idcount+=1
		self.id=Item.idcount
		self.template=ItemTemplate.getTemplate(idtemplate)
		#~ print "Item::__init__" + str(idtemplate) + "/" + str(self.template) + "/" + str(self)
		Item.listOfItem[self.id]=self
		self.bonus={}
		
	def addRandomBonus(self):
		nbBonus=5
		if self.template.getTypeItem()==C_ITEM_WEAPON:
			nbBonus=8
			bon=random.randint(1,nbBonus)
			if bon<=5:
				self.bonus[bon]=1
			elif bon==C_BONUS_DEGAT:
				self.bonus[bon]=random.randint(1,3)
			elif bon==C_BONUS_PORTEE:
				self.bonus[bon]=1
			elif bon==C_BONUS_VITESSE:
				self.bonus[bon]=-0.1
		elif self.template.getTypeItem()==C_ITEM_ARMOR:
			nbBonus=6
			nbBonus=8
			bon=random.randint(1,nbBonus)
			if bon<=5:
				self.bonus[bon]=1
			elif bon==6:
				self.bonus[C_BONUS_ARMOR]=random.randint(1,5)
		else:
			nbBonus=0
		
	def getBonus(self):
		return self.bonus
		
	def getCaract(self):
		return self.template.getCaract()
		
	def getVitesse(self):
		return self.template.vitesse
	
	def getSuitable(self):
		return self.template.getSuitable()
		
	def getLevel(self):
		return self.level
		
	def createNode(self):
		self.node=loader.loadModel('plane')
		self.node.reparentTo(render)   
		self.node.setTransparency(1)  
		self.node.setHpr(0,90,0)
		self.node.hide()
		self.texture=loader.loadTexture(self.template.getIcon())
		self.node.setTexture(self.texture)
		self.node.setTag('id',str(self.id))
		self.node.setName("item#" + str(self.id))
		self.node.setScale(0.5)
		
	def getIdTemplate(self):
		return self.template.getId()
		
	def removeNode(self):
		if self.node!=None:
			self.node.detachNode()
			self.node.removeNode()		
			self.node=None
		
	def getName(self):
		return self.template.getName()
		
	def getTypeItem(self):
		return self.template.getTypeItem()
		
	@staticmethod
	def getItem(id):
		if Item.listOfItem.has_key(id)==False:
			return Item(id)
		if Item.listOfItem.has_key(id)==True:
			return Item.listOfItem[id]
		return None
		
	def getIcon(self):
		return self.template.getIcon()
		
	def show(self):
		self.node.show()
		
	def hide(self):
		if self.node!=None:
			self.node.hide()
		
	def setPos(self,pos):
		self.node.setPos(pos)
		
	def getPos(self):
		if self.node!=None:
			return self.node.getPos()
		return None
		
	def getId(self):
		return self.id
	
	def getNode(self):
		return self.node
