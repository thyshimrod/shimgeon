from shimgeon.items.item import *
from shimgeon.items.armortemplate import *
from shimgeon.core.constantes import *

class Armor(Item):
	listOfArmor={}
	def __init__(self,idtemplate):
		super(Armor,self).__init__(idtemplate)
		Armor.listOfArmor[self.id]=self
		self.template=ArmorTemplate.getTemplate(idtemplate)
				
	def getArmure(self):
		return self.template.getArmor()
		
	@staticmethod
	def castToArmor(obj):
		return Armor(obj.getIdTemplate())
		
	@staticmethod
	def getArmor(id):
		if Armor.listOfArmor.has_key(id)==True:
			return Armor.listOfArmor[id]
		else:
			obj=Item.getItem(id)
			if obj!=None:
				if obj.getTypeItem()==C_ITEM_ARMOR:
					return Armor.castToArmor(obj)
		return None
		
		
	