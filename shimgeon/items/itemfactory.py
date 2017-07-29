from shimgeon.items.item import *
from shimgeon.items.weapon import *
from shimgeon.items.armor import *
from shimgeon.items.potion import *

class ItemFactory:
	@staticmethod
	def getItemObj(itemId):
		obj=Item.getItem(itemId)
		if obj!=None:
			if obj.getTypeItem()==C_ITEM_WEAPON:
				obj=Weapon.getWeapon(itemId)
			elif obj.getTypeItem()==C_ITEM_ARMOR:
				obj=Armor.getArmor(itemId)
			elif obj.getTypeItem()==C_ITEM_POTION:
				obj=Potion.getPotion(itemId)
		return obj
	
	@staticmethod
	def getItemObjTemplate(idTemplate):
		objTemplate=ItemTemplate.getTemplate(idTemplate)
		obj=None
		if objTemplate!=None:
			if objTemplate.getTypeItem()==C_ITEM_WEAPON:
				obj=Weapon(idTemplate)
			elif objTemplate.getTypeItem()==C_ITEM_ARMOR:
				obj=Armor(idTemplate)
			elif objTemplate.getTypeItem()==C_ITEM_POTION:
				obj=Potion(idTemplate)
			else:
				obj=Item(idTemplate)
		return obj