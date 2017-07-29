import random

from shimgeon.sprite.sprite import *


class Persona(Sprite):
	def __init__(self):
		self.animations={}
		self.direction=C_DIR_DOWN
		self.vitesse=0.05
		self.lastMove=0
		self.lastAnim=0
		self.currentAnim=0
		self.nbAnim=0
		self.node=loader.loadModel('plane')
		self.node.reparentTo(render)   
		self.node.setTransparency(1)  
		self.node.setHpr(0,90,0)
		self.level=1
		self.rightHand=None
		self.leftHand=None
		self.middle=None
		self.glove=None
		self.feet=None
		self.head=None
		self.armor=0
		self.inventory=[]
		self.vitesseFrappe=0.5
		self.degatMin=1
		self.degatMax=2
		self.life=100
		self.lastFrappe=0
		self.lifeMax=100
		self.portee=2
		self.lastDegat=0
		self.lastRegen=0
		self.intelligence=0
		self.constitution=0
		self.dexterite=0
		self.intelligence=0
		self.force=0
		self.chance=0
		
	def getBonusDefensif(self):
		bd=self.getArmor()
		return bd
		
	def getBonusOffensif(self):
		bo=0
		if self.leftHand!=None:
			if self.leftHand.getSubType()==C_ITEM_WEAPON_CONTACT:
				bo=self.getForce()
			else:
				bo=self.getDexterite()
		
		return bo
		
	def getBonusDegat(self):
		bonus=0
		if self.leftHand!=None:
			if self.leftHand.getSubType()==C_ITEM_WEAPON_CONTACT:
				bonus+=self.getForce()/5
		else:
			bonus+=self.getForce()/5
							
		return bonus
		
	def getForce(self):
		force=self.force + self.getBonus(C_BONUS_FORCE)
		return force
		
	def getDexterite(self):
		dexterite=self.dexterite+ self.getBonus(C_BONUS_DEXTERITE)
		return dexterite
		
	def getConstitution(self):
		constitution=self.constitution+ self.getBonus(C_BONUS_CONSTITUTION)
		return constitution
		
	def getChance(self):
		chance=self.chance+ self.getBonus(C_BONUS_CHANCE)
		return chance
		
	def getIntelligence(self):
		intelligence=self.intelligence+ self.getBonus(C_BONUS_INTELLIGENCE)
		return intelligence
		
	def getMiddle(self):
		return self.middle
		
	def getGlove(self):
		return self.glove
	
	def getHead(self):
		return self.head
		
	def getFeet(self):
		return self.feet
		
	def getArmor(self):
		armor=self.armor
		if self.middle!=None:
			armor+=self.middle.getArmure()
		if self.glove!=None:
			armor+=self.glove.getArmure()			
		if self.head!=None:
			armor+=self.head.getArmure()			
		if self.feet!=None:
			armor+=self.feet.getArmure()			
		if self.rightHand!=None:
			if self.rightHand.getTypeItem()==C_ITEM_ARMOR:
				armor+=self.feet.getArmure()			
		armor+=self.getBonus(C_BONUS_ARMOR)
		return self.armor
		
	def getBonus(self,typeBonus):
		val=0
		if self.middle!=None:
			bonus=self.middle.getBonus()
			if len(bonus)>0:
				for b in bonus:
					if b==typeBonus:
						val+=bonus[b]
		if self.glove!=None:
			bonus=self.glove.getBonus()
			if len(bonus)>0:
				for b in bonus:
					if b==typeBonus:
						val+=bonus[b]
		if self.head!=None:
			bonus=self.head.getBonus()
			if len(bonus)>0:
				for b in bonus:
					if b==typeBonus:
						val+=bonus[b]
		if self.feet!=None:
			bonus=self.feet.getBonus()
			if len(bonus)>0:
				for b in bonus:
					if b==typeBonus:
						val+=bonus[b]
		if self.rightHand!=None:
			bonus=self.righthand.getBonus()
			if len(bonus)>0:
				for b in bonus:
					if b==typeBonus:
						val+=bonus[b]
		if self.leftHand!=None:
			bonus=self.leftHand.getBonus()
			if len(bonus)>0:
				for b in bonus:
					if b==typeBonus:
						val+=bonus[b]
		return val
		
	def getLeftHand(self):
		return self.leftHand
	
	def getRightHand(self):
		return self.rightHand
		
	def setRightHand(self,obj):
		self.rightHand=obj
		
	def setLeftHand(self,obj):
		self.leftHand=obj
		
	def getInventory(self):
		return self.inventory
		
	def addToInventory(self,obj):
		self.inventory.append(obj)
		
	def removeFromInventory(self,obj):
		if self.inventory.count(obj)>0:
			self.inventory.remove(obj)
	
	def getPortee(self):
		range=0
		if self.leftHand!=None:
			range=self.leftHand.getRange()
		else:
			range=self.portee
		range+=self.getBonus(C_BONUS_PORTEE)
		return range
		
	def setDamage(self,dmg):
		self.life-=dmg
		self.lastDegat=globalClock.getRealTime()
		
	def run(self):
		if (globalClock.getRealTime()-self.lastDegat)>9:
			if self.life<self.lifeMax:
				if (globalClock.getRealTime()-self.lastRegen)>0.5:
					self.lastRegen=globalClock.getRealTime()
					self.life+=3
		elif (globalClock.getRealTime()-self.lastDegat)>6:
			if self.life<self.lifeMax:
				if (globalClock.getRealTime()-self.lastRegen)>0.5:
					self.lastRegen=globalClock.getRealTime()
					self.life+=2
		elif (globalClock.getRealTime()-self.lastDegat)>3:
			if self.life<self.lifeMax:
				if (globalClock.getRealTime()-self.lastRegen)>0.5:
					self.lastRegen=globalClock.getRealTime()
					self.life+=1
					
		if self.life> self.lifeMax:
			self.life=self.lifeMax
	
	def getVitesseFrappe(self):
		vitesse=0
		if self.leftHand!=None:
			vitesse=self.leftHand.getVitesse()
		else:
			vitesse=self.vitesseFrappe
		vitesse-=self.getBonus(C_BONUS_VITESSE)
		return vitesse
		
	def getLifeMax(self):
		return self.constitution*10
		
	def frappe(self,timer,bonusDefensif=0):
		if timer<self.lastFrappe:
			self.lastFrappe=timer
		if (timer-self.lastFrappe)>self.vitesseFrappe:
			self.lastFrappe=timer
			fp=random.randint(1,100)
			if fp==1:
				return False,self.getDamage(),False
			elif fp==100:
				return True,self.getDamage()*2,True
			else:
				toReach=bonusDefensif-self.getBonusOffensif()
				if toReach<fp:
					crit=random.randint(1,100)
					if crit<=self.chance:
						return True,self.getDamage()*2,True
					else:
						return True,self.getDamage(),False
				else:
					return False,self.getDamage(),False
		return False,0,False
		
	def getLife(self):
		return self.life
		
	def getDegatMin(self):
		if self.leftHand!=None:
			return self.leftHand.getDegatMin()
		return self.degatMin
		
	def getDegatMax(self):
		degatMax=0
		if self.leftHand!=None:
			degatMax=self.leftHand.getDegatMax()
		else:
			degatMax=self.degatMax
		degatMax+=self.getBonus(C_BONUS_DEGAT)
		return degatMax
		
	def setPos(self,pos):
		self.node.setPos(pos)
		
	def getPos(self):
		return self.node.getPos()
		
	def getNode(self):
		return self.node
		
	def destroy(self):
		self.node.detachNode()
		self.node.removeNode()
		
	def getLevel(self):
		return self.level
		
	def getDamage(self):
		damage=random.randint(self.getDegatMin(),self.getDegatMax())
		damage+=self.getBonusDegat()
		return damage
		