from shimgeon.sprite.persona import *
from shimgeon.sprite.charactertemplate import *
from pandac.PandaModules import *
from shimgeon.items.weapon import *
from shimgeon.items.armor import *
from shimgeon.items.potion import *
from shimgeon.items.itemfactory import *

class Character(Persona):
	idcount=0
	instance=None
	def __init__(self,idtemplate):
		super(Character,self).__init__()
		Character.idcount+=1
		self.id=Character.idcount
		self.template=CharacterTemplate.getTemplate(idtemplate)
		self.force,	self.dexterite,self.constitution,self.intelligence,self.chance=self.template.getCaract()
		self.loadAnimations()
		self.node.setTexture(self.animations[self.direction][self.currentAnim])
		self.xp=0
		self.money=0
		self.nextLevel=200
		self.previousLevel=0
		self.monsters={}
		#~ self.life=20
		self.skillPoints=0
		self.dungeonLevelReached=0
		items=self.template.getItems()
		for it in items:
			item=ItemFactory.getItemObj(it)
			if item!=None:
				if items[it]==0:
					self.inventory.append(item)
				else:
					self.onEquip(item)
		
		Character.instance=self
		self.name=""
		self.life=self.constitution*10+100
		self.lifeMax=self.life
		
	def getLifeMax(self):
		return (self.constitution*10+100)
		
	def onDelete(self,obj):
		print self.inventory
		if self.inventory.count(obj)>0:
			self.inventory.remove(obj)
		
	def onDrink(self,obj):
		self.life+=obj.getLife()
		if self.life>self.getLifeMax():
			self.life=self.getLifeMax()
		self.removeFromInventory(obj)
		
	def getSkillPoints(self):
		return self.skillPoints
		
	def setCaractPoint(self,car):
		if car==C_CARAC_FORCE:
			self.force+=1
		elif car==C_CARAC_DEXTERITE:
			self.dexterite+=1
		elif car==C_CARAC_CONSTITUTION:
			self.constitution+=1
			self.lifeMax=self.constitution*10+100
		elif car==C_CARAC_INTELLIGENCE:
			self.intelligence+=1
		elif car==C_CARAC_CHANCE:
			self.chance+=1
		self.skillPoints-=1
		
	def getClasse(self):
		return self.template.getName()
		
	def getName(self):
		return self.name
		
	def destroy(self):
		super(Character,self).destroy()
		self.node.detachNode()
		self.node.removeNode()
		Character.instance=None
		
	def setName(self,name):
		self.name=name
		
	def onEquip(self,obj):
		print "onEquip" + str(obj)  +"/" + str(obj.getSuitable())
		if obj.getSuitable()==C_SLOT_LEFT:
			if self.leftHand!=None:
				self.addToInventory(self.leftHand)
			self.leftHand=obj
			self.removeFromInventory(obj)
		elif obj.getSuitable()==C_SLOT_MIDDLE:
			if self.middle!=None:
				self.addToInventory(self.middle)
			self.middle=obj
			self.removeFromInventory(obj)
		elif obj.getSuitable()==C_SLOT_GLOVE:
			if self.glove!=None:
				self.addToInventory(self.glove)
			self.glove=obj
			self.removeFromInventory(obj)
		elif obj.getSuitable()==C_SLOT_FEET:
			if self.feet!=None:
				self.addToInventory(self.feet)
			self.feet=obj
			self.removeFromInventory(obj)
		elif obj.getSuitable()==C_SLOT_HEAD:
			if self.head!=None:
				self.addToInventory(self.head)
			self.head=obj
			self.removeFromInventory(obj)
		elif obj.getSuitable()==C_SLOT_RIGHT:
			if self.rightHand!=None:
				self.addToInventory(self.rightHand)
			self.rightHand=obj
			self.removeFromInventory(obj)
			
		print self.leftHand
		
	def getDungeonLevelReached(self):
		return self.dungeonLevelReached
		
	def setDungeonLevelReached(self,lvl):
		if self.dungeonLevelReached<lvl:
			self.dungeonLevelReached=lvl
		
	def getMonsters(self):
		return self.monsters
		
	def appendMonster(self,mm):
		if self.monsters.has_key(mm.getName()):
			self.monsters[mm.getName()]+=1
		else:
			self.monsters[mm.getName()]=1
		
	def getMoney(self):
		return self.money
		
	def addMoney(self,money):
		self.money+=money
		
	def getPreviousLevel(self):
		return self.previousLevel
		
	def getNextLevel(self):
		return self.nextLevel
		
	def addXp(self,xp):
		self.xp+=xp
		if self.xp>=self.nextLevel:
			diff=self.nextLevel-self.previousLevel
			oldNext=self.nextLevel
			self.nextLevel+=(diff*2)
			self.level+=1
			self.previousLevel=oldNext
			self.skillPoints+=3
			
	def getXp(self):
		return self.xp
		
	@staticmethod
	def getInstance():
		if Character.instance==None:
			Character(1)
		return Character.instance
		
	def loadAnimations(self):
		setAnim=[]
		setAnim.append(loader.loadTexture(self.template.getPath() + "/down1.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/down2.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/down3.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/down4.png"))
		self.animations[C_DIR_DOWN]=setAnim
		setAnim=[]
		setAnim.append(loader.loadTexture(self.template.getPath() + "/up1.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/up2.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/up3.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/up4.png"))
		self.animations[C_DIR_UP]=setAnim
		setAnim=[]
		setAnim.append(loader.loadTexture(self.template.getPath() + "/left1.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/left2.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/left3.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/left4.png"))
		self.animations[C_DIR_LEFT]=setAnim
		setAnim=[]
		setAnim.append(loader.loadTexture(self.template.getPath() + "/right1.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/right2.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/right3.png"))
		setAnim.append(loader.loadTexture(self.template.getPath() + "/right4.png"))
		self.animations[C_DIR_RIGHT]=setAnim
		
	def move(self,timer,dir):
		if timer<self.lastAnim:
			self.lastAnim=timer
		if self.direction!=dir:
			self.direction=dir
		dtAnim=timer-self.lastAnim
		if dtAnim>0.1:
			self.node.setTexture(self.animations[self.direction][self.currentAnim])
			self.lastAnim=timer
			self.currentAnim+=1
			if self.currentAnim>3:
				self.currentAnim=0
		
		if self.direction==C_DIR_UP:
			self.node.setPos(self.node,(0,self.vitesse,0))
		elif self.direction==C_DIR_DOWN:
			self.node.setPos(self.node,(0,-self.vitesse,0))
		elif self.direction==C_DIR_LEFT:
			self.node.setPos(self.node,(-self.vitesse,0,0))
		elif self.direction==C_DIR_RIGHT:
			self.node.setPos(self.node,(self.vitesse,0,0))
			
		#~ print self.node.getPos()