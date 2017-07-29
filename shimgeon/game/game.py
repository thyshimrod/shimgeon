# -*- coding: iso-8859-1 -*-
import sys,os
from math import sqrt
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionTraverser,CollisionNode
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay
from pandac.PandaModules import GeomNode
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import Quat
from shimgeon.level.level import *
from shimgeon.sprite.character import *
from shimgeon.sprite.monster import *
from shimgeon.gui.rocketgame import *
from shimgeon.core.function import *
from shimgeon.game.gamestate import *
from shimgeon.gui.rocketdownstair import *
from shimgeon.gui.rocketupstair import *
from shimgeon.gui.rocketequip import *
from shimgeon.gui.rocketcaract import *
from shimgeon.items.item import *

class game(DirectObject):
	instance=None
	def __init__(self):
		self.keysDown={}
		self.last=0
		self.lastAnim=0
		self.mousebtn = [0,0,0]
		self.accept("arrow_up",self.keyDown,['arrow_up',1])
		self.accept("arrow_up-up",self.keyDown,['arrow_up',0])
		self.accept("arrow_down",self.keyDown,['arrow_down',1])
		self.accept("arrow_down-up",self.keyDown,['arrow_down',0])
		self.accept("arrow_left",self.keyDown,['arrow_left',1])
		self.accept("arrow_left-up",self.keyDown,['arrow_left',0])
		self.accept("arrow_right",self.keyDown,['arrow_right',1])
		self.accept("arrow_right-up",self.keyDown,['arrow_right',0])
		self.accept("z",self.keyDown,['z',1])
		self.accept("z-up",self.keyDown,['z',0])
		self.accept("f1",self.keyDown,['f1',1])
		self.accept("f1-up",self.keyDown,['f1',0])
		self.accept("f2",self.keyDown,['f2',1])
		self.accept("f2-up",self.keyDown,['f2',0])
		self.accept("f12",self.keyDown,['f12',1])
		self.accept("f12-up",self.keyDown,['f12',0])
		self.accept("z",self.keyDown,['z',1])
		self.accept("z-up",self.keyDown,['z',0])
		self.accept("z",self.keyDown,['z',1])
		self.accept("z-up",self.keyDown,['z',0])
		self.accept("q",self.keyDown,['q',1])
		self.accept("q-up",self.keyDown,['q',0])
		self.accept("s",self.keyDown,['s',1])
		self.accept("s-up",self.keyDown,['s',0])
		self.accept("d",self.keyDown,['d',1])
		self.accept("d-up",self.keyDown,['d',0])
		self.accept("w",self.keyDown,['w',1])
		self.accept("w-up",self.keyDown,['w',0])
		self.accept("x",self.keyDown,['x',1])
		self.accept("x-up",self.keyDown,['x',0])
		self.accept("c",self.keyDown,['c',1])
		self.accept("c-up",self.keyDown,['c',0])
		self.accept("i",self.keyDown,['i',1])
		self.accept("i-up",self.keyDown,['i',0])
		self.accept("escape",self.quitGame,)
		self.accept("CLOSEF4",self.quitGame,)
		self.mousebtn = [0,0,0]
		self.accept("mouse1", self.setMouseBtn, [0, 1])
		self.accept("mouse1-up", self.setMouseBtn, [0, 0])
		self.accept("mouse2", self.setMouseBtn, [1, 1])
		self.accept("mouse2-up", self.setMouseBtn, [1, 0])
		self.accept("mouse3", self.setMouseBtn, [2, 1])
		self.accept("mouse3-up", self.setMouseBtn, [2, 0])
		self.level=Level.getLevel(gameState.getInstance().getLevel())
		self.char=Character.getInstance()
		self.char.setDungeonLevelReached(gameState.getInstance().getLevel())
		self.char.setPos((5,99.99,2))
		self.timerBtnClick=globalClock.getRealTime()
		base.disableMouse()
		base.camera.reparentTo(self.char.getNode())
		base.camera.setY(-19.5)
		base.camera.setZ(6)
		base.camera.lookAt(self.char.getNode())
		#~ plight = PointLight('plight')
		#~ plight.setColor(VBase4(1, 0.8, 1, 1))
		#~ self.plnp = render.attachNewNode(plight)
		#~ plnp.setY(-5)
		#~ plight.setAttenuation(Point3(0, 0, 0.5))
		#~ render.setLight(self.plnp)
		self.char.setPos((self.level.getStartPoint().getX(),self.level.getStartPoint().getY()-0.01,self.level.getStartPoint().getZ()))
		#~ self.plnp.setPos((self.level.getStartPoint().getX(),self.level.getStartPoint().getY()-3,self.level.getStartPoint().getZ()))
		slight = Spotlight('slight')
		slight.setColor(VBase4(1, 1, 0.8, 1))
		lens = PerspectiveLens()
		slight.setLens(lens)
		self.slnp = self.char.getNode().attachNewNode(slight)
		self.slnp.setPos(0, 20, -10)
		self.slnp.lookAt(self.char.node)
		render.setLight(self.slnp)
		render.setShaderAuto()
		self.picker = CollisionTraverser()            #Make a traverser
		
		self.pq     = CollisionHandlerQueue()         #Make a handler
		
		taskMgr.add(self.controlCamera, "camera-task")
		self.pickerNode=CollisionNode('mouseRay')
		self.pickerNP=base.camera.attachNewNode(self.pickerNode)
		self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
		self.pickerRay=CollisionRay()
		self.pickerNode.addSolid(self.pickerRay)
		self.picker.addCollider(self.pickerNP, self.pq)
		taskMgr.add(self.pickmouse,"pickmouse")
		rocketGame.getInstance().showWindow()
		alight = AmbientLight('alight')
		alight.setColor(VBase4(0.1, 0.1, 0.1, 1))
		self.alnp = render.attachNewNode(alight)
		render.setLight(self.alnp)
		
		
		#~ self.s=Sprite(3)
		#~ self.s.node.setPos((self.char.getPos().getX()-2,self.char.getPos().getY(),self.char.getPos().getZ()))
		#~ ambient = AmbientLight('ambient')
		#~ ambient.setColor(Vec4(0.5, 1, 0.5, 1))
		#~ ambientNP = self.char.node.attachNewNode(ambient)
		 
		# If we did not call setLightOff() first, the green light would add to
		# the total set of lights on this object. Since we do call
		# setLightOff(), we are turning off all the other lights on this
		# object first, and then turning on only the green light.
		#~ self.char.node.setLightOff()
		#~ self.char.node.setLight(ambientNP)
		amb=random.randint(0,1)
		if amb==0:
			self.ambientSound = base.loader.loadSfx("datas/audio/radakan - volcanic caves.ogg")
		else:
			self.ambientSound = base.loader.loadSfx("datas/audio/dark_caves.ogg")
		self.ambientSound.setLoop(True)
		self.ambientSound.play()
		
		self.coinSound = base.loader.loadSfx("datas/audio/coin.ogg")
		self.swordSound = base.loader.loadSfx("datas/audio/swing.ogg")
		self.bottleSound = base.loader.loadSfx("datas/audio/bottle.ogg")
		self.deathSound = base.loader.loadSfx("datas/audio/shade12.ogg")
		#~ render.setLightOff()
		
	def destroy(self):
		print "game::destroy"
		taskMgr.remove("camera-task")
		taskMgr.remove("pickmouse")
		self.ignore("arrow_up")
		self.ignore("arrow_up-up")
		self.ignore("arrow_down")
		self.ignore("arrow_down-up")
		self.ignore("arrow_left")
		self.ignore("arrow_left-up")
		self.ignore("arrow_right")
		self.ignore("arrow_right-up")
		self.ignore("w")
		self.ignore("w-up")
		self.ignore("x")
		self.ignore("x-up")
		self.ignore("c")
		self.ignore("c-up")
		self.ignore("z")
		self.ignore("z-up")
		self.ignore("q")
		self.ignore("q-up")
		self.ignore("s")
		self.ignore("s-up")
		self.ignore("d")
		self.ignore("d-up")
		self.ignore("i")
		self.ignore("i-up")
		self.ignore("escape")
		self.ignore("CLOSEF4")
		self.ignore("mouse1")
		self.ignore("mouse1-up")
		self.ignore("mouse2")
		self.ignore("mouse2-up")
		self.ignore("mouse3")
		self.ignore("mouse3-up")
		self.level.hide()
		rocketGame.getInstance().hideWindow()
		self.ambientSound.stop()
		self.slnp.detachNode()
		self.slnp.removeNode()
		self.alnp.detachNode()
		self.alnp.removeNode()
		render.setLightOff()
		base.loader.unloadSfx(self.coinSound )
		base.loader.unloadSfx(self.bottleSound )
		base.loader.unloadSfx(self.swordSound )
		base.loader.unloadSfx(self.ambientSound )
		base.loader.unloadSfx(self.deathSound )
		
	def setMouseBtn(self, btn, value):
		self.mousebtn[btn]=value
		if btn==0 and value==1:
			self.timerBtnClick=globalClock.getRealTime()
		
	def pickmouse(self,task):
		"""
			manage click on item
		"""
		mm=None		
		if base.mouseWatcherNode.hasMouse() != False:
			mpos=base.mouseWatcherNode.getMouse()
			self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

			self.picker.traverse(render)
			
			if self.pq.getNumEntries() > 0:
				self.pq.sortEntries() #this is so we get the closest object
				for i in range (self.pq.getNumEntries()):
					nodeInQueue=self.pq.getEntry(i).getIntoNodePath()
					obj=None
					tabNode=str(nodeInQueue).split("/")
					objFromRender=render.find(tabNode[1]).node()
					objName=objFromRender.getName()
					#~ print objName
					if objName.find("#")!=-1:
						tabName=objName.split("#")
						if tabName[0]=="Monster":
							mm=Monster.getMonster(int(tabName[1]))
							if mm.node.isHidden()==False:
								rocketGame.getInstance().renderLife(mm)
								if self.mousebtn[0]==1:
									if calcDistance(self.char.getPos(),mm.getPos())<=self.char.getPortee():
										frappe,degat,critique=self.char.frappe(task.time)
										if frappe==True:
											self.swordSound.play()
											#~ prc=random.randint(1,100)
											#~ if prc>mm.getArmor():
											mm.setDamage(degat)
											rocketGame.getInstance().renderDegat(mm,degat,critique)
											rocketGame.getInstance().renderFx(mm,1,self.char.getVitesseFrappe()/2)
											if mm.getLife()<=0:
												self.deathSound.play()
												self.char.addXp(mm.getLifeMax())
												self.char.appendMonster(mm)
												drops=mm.getLoots()
												for d in drops:
													if d=='money':
														if drops[d]>0:
															pos=(mm.getPos().getX()+random.uniform(0,0.5),mm.getPos().getY(),mm.getPos().getZ()+random.uniform(0,0.5))
															money=Sprite(23)
															money.setPos(pos)
															money.setNb(drops[d])
															self.level.appendDecor(money)
															self.coinSound.play()
													elif d.find('item')!=-1:
														pos=(mm.getPos().getX()+random.uniform(0,0.5),mm.getPos().getY(),mm.getPos().getZ()+random.uniform(0,0.5))
														#~ print "game itemToDrop " + str(drops[d].getId())
														it=ItemFactory.getItemObjTemplate(drops[d].getId())
														if mm.isBoss()==1:
															it.addRandomBonus()
														it.createNode()
														it.setPos(pos)
														it.show()
														if it.getTypeItem()==C_ITEM_POTION:
															self.bottleSound.play()
														self.level.appendItem(it)
												self.level.removeMonster(mm)
										elif frappe==False and degat>0:
											rocketGame.getInstance().renderDegat(mm,"rate")
												
								break
						elif tabName[0]=="Sprite":
							obj=Sprite.getSprite(int(tabName[1]))
							if obj.getName()=="downstair":
								if self.mousebtn[0]==1:
									if calcDistance(self.char.getPos(),obj.getPos())<=2:
										rocketDownStair.getInstance().getWindow()
							elif obj.getName()=="upstair":
								if self.mousebtn[0]==1:
									if calcDistance(self.char.getPos(),obj.getPos())<=2:
										if gameState.getInstance().getLevel()>0:
											rocketUpStair.getInstance().getWindow()
							elif obj.getName()=="money":
								if self.mousebtn[0]==1:
									if calcDistance(self.char.getPos(),obj.getPos())<=2:
										if (globalClock.getRealTime()-self.timerBtnClick)<0.1:
											obj=Sprite.getSprite(int(tabName[1]))
											self.char.addMoney(obj.getNb())
											rocketGame.getInstance().renderGold(obj)
											self.level.removeDecor(obj)
											self.timerBtnClick-=globalClock.getRealTime()
											break
							if obj.getName()!="gate" and obj.getName()!="money":
								break
						elif tabName[0]=="item":
							if self.mousebtn[0]==1:
								obj=Item.getItem(int(tabName[1]))
								if obj.getNode()!=None:
									if calcDistance(self.char.getPos(),obj.getPos())<=2:
										if (globalClock.getRealTime()-self.timerBtnClick)<0.1:
											self.level.removeItem(obj)
											obj.removeNode()
											if obj.getTypeItem()==C_ITEM_WEAPON:
												obj=Weapon.castToWeapon(obj)
											self.char.addToInventory(obj)
											self.timerBtnClick-=globalClock.getRealTime()							
					else:
						break

			
			if mm==None:
				rocketGame.getInstance().noRenderLife()

		return task.cont
		
	def keyDown(self,key,value):
		if value==0:
			if self.keysDown.has_key(key)==True:
				del self.keysDown[key]				
		else:
			self.keysDown[key]=value
		
	def quitGame(self,):
		sys.exit()
	
	def controlCamera(self, task):
		dt = task.time - self.last
		self.last = task.time
		dtAnim=task.time-self.lastAnim
		oldPos=self.char.getPos()
		if self.keysDown.has_key('q'):
			if (self.keysDown['q']!=0):
				 self.char.move(task.time,C_DIR_LEFT)
		if self.keysDown.has_key('s'):
			if (self.keysDown['s']!=0):
				self.char.move(task.time,C_DIR_DOWN)
		if self.keysDown.has_key('d'):
			if (self.keysDown['d']!=0):
				self.char.move(task.time,C_DIR_RIGHT)
		if self.keysDown.has_key('z'):
			if (self.keysDown['z']!=0):
				self.char.move(task.time,C_DIR_UP)
		if self.keysDown.has_key('arrow_up'):
			if (self.keysDown['arrow_up']!=0):
				base.camera.setY(base.camera.getY()+0.5)
		if self.keysDown.has_key('arrow_down'):
			if (self.keysDown['arrow_down']!=0):
				base.camera.setY(base.camera.getY()-0.5)
		if self.keysDown.has_key('arrow_left'):
			if (self.keysDown['arrow_left']!=0):
				base.camera.setZ(base.camera.getZ()+0.2)
		if self.keysDown.has_key('arrow_right'):
			if (self.keysDown['arrow_right']!=0):
				base.camera.setZ(base.camera.getZ()-0.2)
		if self.keysDown.has_key('w'):
			if (self.keysDown['w']!=0):
				#~ self.s.node.setP(self.s.node.getP()+1)
				#~ print self.s.node.getP()
				pass
		if self.keysDown.has_key('i'):
			if (self.keysDown['i']!=0):
				RocketEquip.getInstance().getWindow()
				self.keysDown['i']=0
		if self.keysDown.has_key('c'):
			if (self.keysDown['c']!=0):
				RocketCaract.getInstance().getWindow()
				self.keysDown['c']=0
		if self.keysDown.has_key('f1'):
			if (self.keysDown['f1']!=0):
				rocketGame.getInstance().use(1)
				self.keysDown['f1']=0
		if self.keysDown.has_key('f2'):
			if (self.keysDown['f2']!=0):
				rocketGame.getInstance().use(2)
				self.keysDown['f2']=0
		if self.keysDown.has_key('f2'):
			if (self.keysDown['f2']!=0):
				gameState.getInstance().setState(C_DEATH)
				self.keysDown['f2']=0
		validMvt,collidedObj=self.level.validMvt(self.char.getPos())
		if validMvt==False:
			self.char.setPos(oldPos)

		for m in self.level.getMonsters():
			distance=calcDistance(m.getPos(),self.char.getPos())
			if (distance<10) and (distance>1):
				oldPos=m.getPos()
				m.move(self.char.getPos(),task.time)
				validMvt,collidedObj=self.level.validMvt(m.getPos())
				if validMvt==False and isinstance(collidedObj,Monster)!=True:
					m.setPos(oldPos)
			if distance<=2:
				frappe,degat,critique=m.frappe(task.time,m.getBonusDefensif())
				if frappe==True:
					prc=random.randint(1,100)
					if prc>self.char.getArmor():
						self.swordSound.play()
						self.char.setDamage(degat)
						rocketGame.getInstance().renderDegat(self.char,degat)
						rocketGame.getInstance().renderFx(self.char,1,m.getVitesseFrappe()/2)
						if self.char.getLife()<=0:
							gameState.getInstance().setState(C_DEATH)
				elif frappe==False and degat>0:
					rocketGame.getInstance().renderDegat(self.char,"rate")
				
		self.char.run()
		#~ self.slnp.setPos((self.char.getPos().getX(),self.char.getPos().getY()-4,self.char.getPos().getZ()+1))
		#~ print self.gate.getHpr()

		return task.cont
		




