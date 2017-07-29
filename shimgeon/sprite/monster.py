from shimgeon.sprite.persona import *
from shimgeon.sprite.monstertemplate import *
from shimgeon.game.gamestate import *
from shimgeon.items.itemtemplate import *
import random

class Monster(Persona):
	idcount=0
	listOfMonsters={}
	def __init__(self,idtemplate):		
		Monster.idcount+=1
		#~ super(Monster,self).__init__()
		super(Monster,self).__init__()
		self.id=Monster.idcount
		self.template=MonsterTemplate.getTemplate(idtemplate)
		self.force,	self.dexterite,self.constitution,self.intelligence,self.chance=self.template.getCaract()
		self.loadAnimations()
		self.node.setTexture(self.animations[self.direction][self.currentAnim])
		self.node.setTag('id',str(self.id))
		self.node.setTag('name',"Monster#" + str(self.id))
		self.node.setName("Monster#" + str(self.id))
		self.vitesse=0.05
		Monster.listOfMonsters[self.id]=self
		self.life=self.lifeMax=self.constitution*10
		self.level=0
		self.boss=0
		
	def findSuitableTemplate(self,slot):
		itemToSuit=None
		itemTemplates=ItemTemplate.getTemplates()
		for it in itemTemplates:
			if itemTemplates[it].getSuitable()==slot:
				f,d,c,i,ch=itemTemplates[it].getCaract()
				if self.force<=f and self.dexterite<=d and self.constitution<=c and self.intelligence<=i and self.chance<=ch:
					if itemToSuit!=None:
						f2,d2,c2,i2,ch2=itemTemplates[itemToSuite].getCaract()
						if f2<=f and d2<=d and c2<=c and i2<=i and ch2<ch:
							itemToSuit=it
					else:
						itemToSuit=it
		return itemToSuit
		
	def equip(self):
		suit=random.randint(0,1)
		if suit==1:
			itemToSuit=self.findSuitableTemplate(C_SLOT_LEFT)
			if itemToSuit!=None:
				it=getItemObjTemplate(it)
				self.leftHand=it
				
		suit=random.randint(0,1)
		if suit==1:
			itemToSuit=self.findSuitableTemplate(C_SLOT_RIGHT)
			if itemToSuit!=None:
				it=getItemObjTemplate(it)
				self.rightHand=it
		
		suit=random.randint(0,1)
		if suit==1:
			itemToSuit=self.findSuitableTemplate(C_SLOT_MIDDLE)
			if itemToSuit!=None:
				it=getItemObjTemplate(it)
				self.middle=it
		
		suit=random.randint(0,1)
		if suit==1:
			itemToSuit=self.findSuitableTemplate(C_SLOT_FEET)
			if itemToSuit!=None:
				it=getItemObjTemplate(it)
				self.feet=it
				
		suit=random.randint(0,1)
		if suit==1:
			itemToSuit=self.findSuitableTemplate(C_SLOT_HEAD)
			if itemToSuit!=None:
				it=getItemObjTemplate(it)
				self.head=it
		
		suit=random.randint(0,1)
		if suit==1:
			itemToSuit=self.findSuitableTemplate(C_SLOT_GLOVE)
			if itemToSuit!=None:
				it=getItemObjTemplate(it)
				self.glove=it
		
				
	def createNode(self):
		self.node=loader.loadModel('plane')
		self.node.setTexture(self.animations[self.direction][self.currentAnim])
		self.node.reparentTo(render)
		self.node.setTransparency(1)  
		self.node.setTwoSided(True) 
		self.node.setTag('name',"Monster#" + str(self.id))
		self.node.setTag('id',str(self.id))
		self.node.setName("Monster#" + str(self.id))
		self.node.setHpr(self.hpr)
		self.node.setPos(self.pos)
		
	def setLevel(self,lvl):
		self.level=lvl
		skillPoints=lvl*3
		if self.template.getClasse()==C_CLASS_WARRIOR:
			for i in range(skillPoints):
				c=random.randint(1,3)
				if c==1:
					self.force+=1
				elif c==2:
					self.dexterite+=1
				elif c==3:
					self.constitution+=1
					
		self.life=self.lifeMax=self.constitution*10
		
	def isBoss(self):
		return self.boss
		
	def setBoss(self,boss):
		self.boss=boss
		ambient = AmbientLight('ambient')
		ambient.setColor(Vec4(0.5, 1, 0.5, 1))
		ambientNP = self.node.attachNewNode(ambient)
		self.node.setLightOff()
		self.node.setLight(ambientNP)
		
	def getArmor(self):
		return self.template.getArmor()
		
	def getLoots(self):
		loots={}
		loots['money']=random.randint(0,self.level*10)
		if self.boss==1:
			loots['money']=loots['money']*2
		lootable=self.template.getLoots()

		lvl=gameState.getInstance().getLevel()
		
		listOfLoots=ItemTemplate.getItemByLevel(lvl)
		if len(listOfLoots)>0:
			nbLoots=random.randint(0,2)
			for i in range(nbLoots):
				if len(listOfLoots)>1:
					lootNb=random.randint(0,len(listOfLoots)-1)
				else:
					lootNb=0
				loots['item' + str(i)]=listOfLoots[lootNb]
			
		return loots
		
	def move(self,pos,timer):
		posChar=pos
		posM=self.getPos()
		newDirection=self.direction
		hasToMove=False
		if posChar.getX()>posM.getX() and (posChar.getX()-posM.getX())>0.5:
			newDirection=C_DIR_RIGHT
			hasToMove=True
		elif posChar.getX()<posM.getX() and (posM.getX()-posChar.getX())>0.5:
			newDirection=C_DIR_LEFT
			hasToMove=True
			
		if self.direction!=newDirection:
			self.direction=newDirection
		if timer<self.lastAnim:
			self.lastAnim=timer
		if hasToMove==True:
			dtAnim=timer-self.lastAnim
			if dtAnim>0.1:
				self.node.setTexture(self.animations[self.direction][self.currentAnim])
				self.lastAnim=timer
				self.currentAnim+=1
				if self.currentAnim>=self.template.getNbAnimation():
					self.currentAnim=0
			if self.direction==C_DIR_LEFT:
				self.node.setPos(self.node,(-self.vitesse,0,0))
			elif self.direction==C_DIR_RIGHT:
				self.node.setPos(self.node,(self.vitesse,0,0))
		hasToMove=False
		if posChar.getZ()>posM.getZ() and (posChar.getZ()-posM.getZ())>0.5:
			newDirection=C_DIR_UP
			hasToMove=True
		elif posChar.getZ()<posM.getZ() and (posM.getZ()-posChar.getZ())>0.5:
			newDirection=C_DIR_DOWN
			hasToMove=True
		if self.direction!=newDirection:
			self.direction=newDirection
		if hasToMove==True:
			dtAnim=timer-self.lastAnim
			if dtAnim>0.1:
				self.node.setTexture(self.animations[self.direction][self.currentAnim])
				self.lastAnim=timer
				self.currentAnim+=1
				if self.currentAnim>=self.template.getNbAnimation():
					self.currentAnim=0
			if self.direction==C_DIR_UP:
				self.node.setPos(self.node,(0,self.vitesse,0))
			elif self.direction==C_DIR_DOWN:
				self.node.setPos(self.node,(0,-self.vitesse,0))
		
	def getLifeMax(self):
		return self.lifeMax
		
	@staticmethod
	def getMonster(id):
		return Monster.listOfMonsters[id]
		
	def setPos(self,pos):
		self.node.setPos(pos)
		
	def getPos(self):
		return self.node.getPos()
		
	def getNode(self):
		return self.node
		
	def loadAnimations(self):
		setAnim=[]
		for i in range(1,self.template.getNbAnimation()+1):
			setAnim.append(loader.loadTexture(self.template.getPath() + "/down" + str(i)+ ".png"))
			self.animations[C_DIR_DOWN]=setAnim
		setAnim=[]	
		for i in range(1,self.template.getNbAnimation()+1):
			setAnim.append(loader.loadTexture(self.template.getPath() + "/up" + str(i)+ ".png"))
			self.animations[C_DIR_UP]=setAnim
		setAnim=[]
		for i in range(1,self.template.getNbAnimation()+1):
			setAnim.append(loader.loadTexture(self.template.getPath() + "/left" + str(i)+ ".png"))
			self.animations[C_DIR_LEFT]=setAnim
		setAnim=[]
		for i in range(1,self.template.getNbAnimation()+1):
			setAnim.append(loader.loadTexture(self.template.getPath() + "/right" + str(i)+ ".png"))
			self.animations[C_DIR_RIGHT]=setAnim
		
		