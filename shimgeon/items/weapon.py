from shimgeon.items.item import *
from shimgeon.items.weapontemplate import *
from shimgeon.core.constantes import *

class Weapon(Item):
	listOfWeapon={}
	def __init__(self,idtemplate):
		super(Weapon,self).__init__(idtemplate)
		Weapon.listOfWeapon[self.id]=self
		self.template=WeaponTemplate.getTemplate(idtemplate)
		
	def getSubType(self):
		return self.template.getSubType()
			
	def getDegatMin(self):
		return self.template.getDegatMin()
		
	def getDegatMax(self):
		return self.template.getDegatMax()
		
	def getRange(self):
		return self.template.getRange()
		
	@staticmethod
	def castToWeapon(obj):
		return Weapon(obj.getIdTemplate())
		
	@staticmethod
	def getWeapon(id):
		if Weapon.listOfWeapon.has_key(id)==True:
			return Weapon.listOfWeapon[id]
		else:
			obj=Item.getItem(id)
			if obj!=None:
				if obj.getTypeItem()==C_ITEM_WEAPON:
					obj=Weapon.castToWeapon(obj)
					return obj
		return None
		
		
	