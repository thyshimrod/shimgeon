from shimgeon.items.item import *
from shimgeon.items.potiontemplate import *
from shimgeon.core.constantes import *

class Potion(Item):
	listOfPotion={}
	def __init__(self,idtemplate):
		super(Potion,self).__init__(idtemplate)
		Potion.listOfPotion[self.id]=self
		self.template=PotionTemplate.getTemplate(idtemplate)
				
	def getLife(self):
		return self.template.getLife()
		
	@staticmethod
	def castToPotion(obj):
		return Potion(obj.getIdTemplate())
		
	@staticmethod
	def getPotion(id):
		if Potion.listOfPotion.has_key(id)==True:
			return Potion.listOfPotion[id]
		else:
			obj=Item.getItem(id)
			if obj!=None:
				if obj.getTypeItem()==C_ITEM_POTION:
					return Potion.castToPotion(obj)
		return None
		
		
	