import random
import math
import xml.dom.minidom
from math import sqrt
from pandac.PandaModules import *
from shimgeon.level.theme import *
from shimgeon.sprite.sprite import *
from shimgeon.level.room import *
from shimgeon.sprite.monster import *
from shimgeon.items.item import *

class Level():
	levels={}
	def __init__(self,level):
		self.level=level
		self.rooms=[]
		self.corridors=[]
		self.monsters=[]
		self.decors=[]
		self.items=[]
		self.typeGround=random.randint(1,7)
		self.confMonsters={}
		self.loadConfig()
		self.startPoint=Vec3(0,0,0)
		self.startingRoom=None
		self.generateLevel()
		self.generateRoad()
		self.generateMonsters()
		Level.levels[self.level]=self
		
	def loadConfig(self):
		dom = xml.dom.minidom.parse("config/levels.xml")
		it=dom.getElementsByTagName('level')
		for i in it:
			id=int(i.getElementsByTagName('id')[0].firstChild.data)
			if id==self.level:
				self.confMonsters={}
				monsters=i.getElementsByTagName('monster')
				for m in monsters:
					id=int(m.getElementsByTagName('id')[0].firstChild.data)
					prcent=int(m.getElementsByTagName('prcent')[0].firstChild.data)
					self.confMonsters[id]=prcent
				
		
	@staticmethod
	def reset():
		for l in Level.levels:
			Level.levels[l].destroy()
			
		Level.levels={}
		
	def hide(self):
		for r in self.rooms:
			r.hide()
		for c in self.corridors:
			c.hide()
		for m in self.monsters:
			m.hide()
		for d in self.decors:
			d.hide()
		for i in self.items:
			i.hide()
			
	def show(self):
		for r in self.rooms:
			r.show()
		for c in self.corridors:
			c.show()
		for m in self.monsters:
			m.show()
		for d in self.decors:
			d.show()
		for i in self.items:
			i.show()
		
	def destroy(self):
		for r in self.rooms:
			r.destroy()
		for c in self.corridors:
			c.destroy()
		for m in self.monsters:
			m.destroy()
		for d in self.decors:
			d.destroy()
		for i in self.items:
			i.removeNode()
		
	def appendItem(self,it):
		self.items.append(it)
		
	def removeItem(self,it):
		if self.items.count(it)>0:
			self.items.remove(it)
			it.hide()
		
	def getMonsters(self):
		return self.monsters
		
	def generateMonsters(self):
		for r in self.rooms:
			if r!=self.startingRoom:
				size=int(sqrt(r.getX()*r.getY())/2)
				for i in range(size):
					stx=random.uniform(1,r.getX()-1)
					stz=random.uniform(1,r.getY()-1)
					ps=r.getPos()
					l=Vec3(r.getPos().getX()+stx,r.getPos().getY()-0.5,r.getPos().getZ()+stz)
					typeMonsterRd=random.randint(1,100)
					start=0
					typeMonster=0
					for tm in self.confMonsters:
						if typeMonsterRd>start and typeMonsterRd<=(self.confMonsters[tm]+start):
							typeMonster=tm
							break
						else:
							start+=self.confMonsters[tm]
					m=Monster(typeMonster)
					boss=random.randint(1,100)
					rg=random.randint(1,2)
					if boss<10:
						m.setBoss(1)
						rgboss=random.randint(2,4)
						m.setLevel(self.level+rg+rgboss)
					else:
						m.setLevel(self.level+rg)
					m.equip()
					m.setPos(l)
					self.monsters.append(m)
			
	def appendDecor(self,decor):
		self.decors.append(decor)
		
	def removeDecor(self,decor):
		if self.decors.count(decor)>0:
			decor.destroy()
			self.decors.remove(decor)
		
	def removeMonster(self,mm):
		if self.monsters.count(mm)>0:
			mm.destroy()
			self.monsters.remove(mm)
			
	def checkRooms(self,x,z,h,w):
		collide=False
		for r in self.rooms:
			if x> r.getPos().getX() and x< (r.getX()+r.getPos().getX()) and z>r.getPos().getZ() and z<(r.getPos().getZ()+r.getY()):
				collide=True
			if (x+w)> r.getPos().getX() and (x+w)< (r.getX()+r.getPos().getX()) and z>r.getPos().getZ() and z<(r.getPos().getZ()+r.getY()):
				collide=True
			if (x+w)> r.getPos().getX() and (x+w)< (r.getX()+r.getPos().getX()) and (z+h)>r.getPos().getZ() and (z+h)<(r.getPos().getZ()+r.getY()):
				collide=True
			if x> r.getPos().getX() and x< (r.getX()+r.getPos().getX()) and (z+h)>r.getPos().getZ() and (z+h)<(r.getPos().getZ()+r.getY()):
				collide=True
		return collide
		
	def generateLevel(self):
		nbRoom=random.randint(2,10)
		for nb in range(nbRoom):
			c=True
			while c==True:
				x=random.randint(0,50)
				z=random.randint(0,50)
				h=random.randint(10,12)
				w=random.randint(10,12)
				c=self.checkRooms(x,z,h,w)
			print "room : " + str(h) + "/" + str(w) + "/" + str(x) + ",100," + str(z)
			self.rooms.append(Room(h,w,Vec3(x,100,z),self.typeGround))
		#~ #Calculation of start point
#~ room : 11/12/23,100,38
#~ room : 10/10/24,100,10
		#~ self.rooms.append(Room(11,12,Vec3(23,100,38),2))
		#~ self.rooms.append(Room(10,10,Vec3(24,100,10),1))
		#~ self.rooms.append(Room(12,11,Vec3(18,100,34),self.typeGround))
		#~ room : 10/10/9,100,50
#~ room : 12/10/35,100,6
		#~ self.rooms.append(Room(10,10,Vec3(9,100,50),1))
		#~ self.rooms.append(Room(12,10,Vec3(35,100,6),self.typeGround))
		r=random.randint(0,len(self.rooms)-1)
		#~ r=0
		rom=self.rooms[r]
		self.startingRoom=rom
		h=rom.getY()
		w=rom.getX()
		ps=rom.getPos()
		stz=random.randint(1,h-1)
		stx=random.randint(1,w-1)
		self.startPoint=Vec3(rom.getPos().getX()+stx,rom.getPos().getY()-0.5,rom.getPos().getZ()+stz)
		upstair=Sprite(10)
		upstair.setPos((self.startPoint.getX(),self.startPoint.getY()+0.001,self.startPoint.getZ())) 
		self.decors.append(upstair)
	
		#~ #Calculation of e d point
		r=random.randint(1,len(self.rooms)-1)
		#~ r=0
		rom=self.rooms[r]
		self.endingRoom=rom
		h=rom.getY()
		w=rom.getX()
		ps=rom.getPos()
		stz=random.randint(1,h-1)
		stx=random.randint(1,w-1)
		self.endingPoint=Vec3(rom.getPos().getX()+stx,rom.getPos().getY()-0.5,rom.getPos().getZ()+stz)
		downStair=Sprite(11)
		downStair.setPos((self.endingPoint.getX(),self.endingPoint.getY()+0.001,self.endingPoint.getZ())) 
		self.decors.append(downStair)
		###

		
		
	def generateRoad(self):
		i=0
		for r in self.rooms:
			if len(self.rooms)>i+1:	
				nearestRoom=self.rooms[i+1]
				if nearestRoom!=None:
					r.addWayToRoom(nearestRoom)
					nearestRoom.addWayToRoom(r)
					pos1=r.getPos()
					pos2=nearestRoom.getPos()
					pY=random.randint(1,r.getY()-2)
					pY2=random.randint(1,nearestRoom.getY()-2)
					pX=random.randint(1,r.getX()-2)
					pX2=random.randint(1,nearestRoom.getX()-2)
					
					distX=abs((pos1.getX()+pX)-(pos2.getX()+pX2))
					if pos1.getZ()>pos2.getZ():
						distZ=pos1.getZ()-r.getY()-pos2.getZ()
					else:
						distZ=pos2.getZ()-nearestRoom.getY()-pos1.getZ()
						
					if pos1.getX()>pos2.getX():
						distX=pos1.getX()-r.getX()-pos2.getX()
					else:
						distX=pos2.getX()-nearestRoom.getX()-pos1.getX()
					print str(distX) + "/" + str(distZ) + "/" + str(pos1.getX()) + str(pos2.getX()) + "/" + str(pos1.getZ()) + str(pos2.getZ())
					if distX<distZ:
						p=random.randint(1,r.getY()-2)
						p2=random.randint(1,nearestRoom.getY()-2)
						lg1=abs(int(distX/2))
						 
						if pos1.getX()>pos2.getX():
							if distX>0:
								gate=Sprite(24)
								gate.setPos((pos1.getX()+0.5-1,99,pos1.getZ()+p+0.5))
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								r.appendGate(gate)
								gate=Sprite(24)
								gate.setPos((pos2.getX()+0.5+nearestRoom.getX()-1,99,pos2.getZ()+p2+0.5)) 
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								nearestRoom.appendGate(gate)
								self.corridors.append(Room(lg1,2,Vec3(pos1.getX()-lg1+1,100.02,pos1.getZ()+p),9,True))			
								if pos1.getZ()<pos2.getZ():
									distanceX=int((pos2.getZ()+p2)-(pos1.getZ()+p))
									self.corridors.append(Room(2,distanceX+1,Vec3(pos1.getX()-lg1,100.02,pos1.getZ()+p),9,True))			
									self.corridors.append(Room(lg1+3,2,Vec3(pos1.getX()-distX-1,100.02,pos2.getZ()+p2),9,True))			
								else:
									distanceX=int((pos1.getZ()+p)-(pos2.getZ()+p2))
									self.corridors.append(Room(2,distanceX+1,Vec3(pos1.getX()-lg1,100.02,pos1.getZ()+p-distanceX+1),9,True))			
									self.corridors.append(Room(lg1+3,2,Vec3(pos1.getX()-distX-1,100.02,pos1.getZ()+p-distanceX),9,True))			
							else:
								gate=Sprite(24)
								gate.setPos((pos1.getX()+0.5-1,99,pos1.getZ()+p+0.5))
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								r.appendGate(gate)
								gate=Sprite(24)
								p2=random.randint(1,nearestRoom.getY()+distX)
								distanceX=int(pos1.getX()-(pos2.getX()+p2))
								if pos1.getZ()>pos2.getZ():
									gate.setPos((pos2.getX()+p2+0.5,99,pos2.getZ()-0.5+nearestRoom.getY()))				
								else:
									gate.setPos((pos2.getX()+p2+0.5,99,pos2.getZ()-0.5))
								self.corridors.append(Room(distanceX+1,2,Vec3(pos1.getX()+0.5-distanceX,100.02,pos1.getZ()+p),9,True))		
								distanceZ=abs(int(pos1.getZ()+p-pos2.getZ()-nearestRoom.getY()))
								if pos1.getZ()>pos2.getZ():
									self.corridors.append(Room(2,distanceZ+3,Vec3(pos2.getX()+p2,100.02,pos2.getZ()+nearestRoom.getY()-1),9,True))		
								else:
									self.corridors.append(Room(2,abs(distanceZ)+3,Vec3(pos2.getX()+p2,100.02,pos1.getZ()+r.getY()-1),9,True))		
								self.decors.append(gate)
								nearestRoom.appendGate(gate)
						else:
							if distX>0:
								self.corridors.append(Room(lg1+3,2,Vec3(pos1.getX()+r.getX()-2+1,100.02,pos1.getZ()+p),9,True))			
								gate=Sprite(24)
								gate.setPos((pos1.getX()+r.getX()+0.5-1,99,pos1.getZ()+p+0.5))
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								r.appendGate(gate)
								gate=Sprite(24)
								gate.setPos((pos2.getX()+0.5-1,99,pos2.getZ()+p2+0.5)) 
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								nearestRoom.appendGate(gate)
								if pos1.getZ()<pos2.getZ():
									distanceZ=int((pos2.getZ()+p2)-(pos1.getZ()+p))
									self.corridors.append(Room(2,distanceZ+2,Vec3(pos1.getX()+r.getX()+lg1,100.02,pos1.getZ()+p),9,True))			
									self.corridors.append(Room(lg1+3,2,Vec3(pos2.getX()-2-lg1,100.02,pos2.getZ()+p2),9,True))			
								else:
									distanceZ=int((pos1.getZ()+p)-(pos2.getZ()+p2))
									self.corridors.append(Room(2,distanceZ+1,Vec3(pos1.getX()+r.getX()+lg1,100.02,pos1.getZ()+p-distanceZ+1),9,True))			
									self.corridors.append(Room(lg1+3,2,Vec3(pos2.getX()-2-lg1,99.99,pos1.getZ()+p-distanceZ),3,True))			
							else:
								gate=Sprite(24)
								gate.setPos((pos1.getX()+r.getX()+0.5-1,99,pos1.getZ()+p+0.5))
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								r.appendGate(gate)
								p2=random.randint(0-distX,nearestRoom.getX())
								gate=Sprite(24)
								gate.setPos((pos2.getX()+p2-0.5,99,pos2.getZ()-0.5))
								self.decors.append(gate)
								r.appendGate(gate)
								distanceX=abs(int(pos1.getX()+r.getX()-pos2.getX()-p2))
								distanceZ=int(pos1.getZ()+p-pos2.getZ())
								
								
								self.corridors.append(Room(distanceX+1,2,Vec3(pos1.getX()+r.getX()-1,100.02,pos1.getZ()+p),9,True))			
								if distanceZ<0:
									self.corridors.append(Room(2,distanceZ+1,Vec3(pos1.getX()+r.getX()+distanceX-1,100.02,pos1.getZ()+p),9,True))			
								else:
									self.corridors.append(Room(2,distanceZ+1,Vec3(pos1.getX()+r.getX()+distanceX-1,100.02,pos2.getZ()),9,True))			
					else:
						if pos1.getZ()<pos2.getZ():
							if distZ>0:
								p=random.randint(1,r.getX()-2)
								p2=random.randint(1,nearestRoom.getX()-2)
								lg1=abs(int(distZ/2))
								gate=Sprite(24)
								gate.setPos((pos1.getX()+pX+0.5,99,pos1.getZ()+r.getY()-0.5))
								self.decors.append(gate)
								r.appendGate(gate)
								gate=Sprite(24)
								gate.setPos((pos2.getX()+pX2+0.5,99,pos2.getZ()-0.5))
								self.decors.append(gate)
								nearestRoom.appendGate(gate)
								if pos1.getX()<pos2.getX():
									distanceX=int((pos2.getX()+p2)-(pos1.getX()+p))
									self.corridors.append(Room(distanceX+1,2,Vec3(pos1.getX()+pX,99.99,pos1.getZ()+r.getY()+lg1),9,True))			
								else:
									distanceX=int((pos1.getX()+pX)-(pos2.getX()+pX2))
									self.corridors.append(Room(distanceX+2,2,Vec3(pos2.getX()+pX2,99.99,pos1.getZ()+r.getY()+lg1),9,True))			
								
								self.corridors.append(Room(2,lg1+2,Vec3(pos1.getX()+pX,99.99,pos1.getZ()+r.getY()-1),9,True))			
								if (distZ-(lg1*2))>0:
									self.corridors.append(Room(2,lg1+3,Vec3(pos2.getX()+pX2,99.99,pos1.getZ()+r.getY()+lg1),9,True))			
								else:
									self.corridors.append(Room(2,lg1+1,Vec3(pos2.getX()+pX2,99.99,pos1.getZ()+r.getY()+lg1),9,True))			
							else:
								p=random.randint(1,r.getY()-2)
								p2=random.randint(1,nearestRoom.getX()-2)
								lg1=abs(int(distZ/2))
								gate=Sprite(24)
								gate.setPos((pos2.getX()+pX2+0.5,99,pos2.getZ()-0.5))
								self.decors.append(gate)
								nearestRoom.appendGate(gate)
								gate=Sprite(24)
								if pos1.getX()<pos2.getX():
									gate.setPos((pos1.getX()+r.getX()-0.5,99,pos1.getZ()+p-0.5))
									distanceX=int((pos2.getX()+p2)-pos1.getX()-r.getX())
									self.corridors.append(Room(distanceX,2,Vec3(pos1.getX()+r.getX()-1,100.02,pos1.getZ()+p),9,True))	
								else:
									gate.setPos((pos1.getX()-0.5,99,pos1.getZ()+p-0.5))
									distanceX=abs(int(pos1.getX()-(pos2.getX()+p2)))
									self.corridors.append(Room(distanceX+2,2,Vec3(pos2.getX()+p2-1,100.02,pos1.getZ()+p),9,True))	
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								r.appendGate(gate)
								
								distanceZ=abs(int((pos1.getZ()+p)-pos2.getZ()))
								self.corridors.append(Room(2,distanceZ+3,Vec3(pos2.getX()+p2-1,100.02,pos1.getZ()+p),9,True))
						else:			
							if distZ>0:
								lg1=int(distZ/2)
								gate=Sprite(24)
								gate.setPos((pos1.getX()+pX+0.5,99,pos1.getZ()-0.5))
								self.decors.append(gate)
								r.appendGate(gate)
								gate=Sprite(24)
								gate.setPos((pos2.getX()+pX2+0.5,99,pos2.getZ()+nearestRoom.getY()-0.5))
								self.decors.append(gate)
								nearestRoom.appendGate(gate)
								if pos1.getX()<pos2.getX():
									distanceX=int((pos2.getX()+pX2)-(pos1.getX()+pX))
									self.corridors.append(Room(distanceX+1,2,Vec3(pos1.getX()+pX,100.02,pos1.getZ()-lg1+1),9,True))			
								else:
									distanceX=int((pos1.getX()+pX)-(pos2.getX()+pX2))
									self.corridors.append(Room(distanceX+1,2,Vec3(pos2.getX()+pX2,100.02,pos1.getZ()-lg1+1),9,True))			
								self.corridors.append(Room(2,lg1,Vec3(pos1.getX()+pX,100.02,pos1.getZ()-lg1+1),9,True))			
								if (distZ-(lg1*2))>0:
									self.corridors.append(Room(2,lg1+4,Vec3(pos2.getX()+pX2,100.02,pos1.getZ()-(lg1*2)-2),9,True))			
								else:
									self.corridors.append(Room(2,lg1+3,Vec3(pos2.getX()+pX2,100.02,pos1.getZ()-(lg1*2)-1),9,True))			
							else:
								p=random.randint(1,r.getY()-2)
								p2=random.randint(1,nearestRoom.getX()-2)
								lg1=abs(int(distZ/2))
								gate=Sprite(24)
								gate.setPos((pos1.getX()+r.getX()-0.5,99,pos1.getZ()+p))
								gate.getNode().setHpr((90,0,-90))
								self.decors.append(gate)
								r.appendGate(gate)
								gate=Sprite(24)
								gate.setPos((pos2.getX()+pX2+0.5,99,pos2.getZ()+nearestRoom.getY()-0.5))
								self.decors.append(gate)
								nearestRoom.appendGate(gate)
								distanceX=int((pos2.getX()+pX2) - (pos1.getX()+r.getX()))
								distanceZ=int((pos1.getZ()+p)-(pos2.getZ()+nearestRoom.getY()))
								self.corridors.append(Room(distanceX+2,2,Vec3(pos1.getX()+r.getX()-1,100.02,pos1.getZ()+p),9,True))
								self.corridors.append(Room(2,distanceZ+3,Vec3(pos1.getX()+r.getX()+distanceX,100.02,pos2.getZ()+nearestRoom.getY()-1),9,True))
			i+=1
		#~ for r in self.rooms:
			#~ r.generateWall()
	def calcDistance(self,pos1,pos2):
		dx=pos1.getX()-pos2.getX()
		dy=pos1.getY()-pos2.getY()
		dz=pos1.getZ()-pos2.getZ()
		currentDistance=int(round(sqrt(dx*dx+dy*dy+dz*dz),0))
		return currentDistance
	
		
	def getStartPoint(self):
		return self.startPoint
		
	@staticmethod
	def getLevel(level):
		if Level.levels.has_key(level)!=True:
			Level.levels[level]=Level(level)
		else:
			Level.levels[level].show()
		return Level.levels[level]
			
	def validMvt(self,pos):
		valid=False
		collided=None
		listOfRooms=[]
		for r in self.rooms:
			if pos.getX()>(r.getPos().getX()) and pos.getX()<(r.getPos().getX()+r.getX()-1):
				if pos.getZ()>(r.getPos().getZ()) and pos.getZ()<(r.getPos().getZ()+r.getY()-1):
					valid=True
					listOfRooms.append(r)
		for r in self.corridors:
			if pos.getX()>(r.getPos().getX()) and pos.getX()<(r.getPos().getX()+r.getX()-1):
				if pos.getZ()>(r.getPos().getZ()) and pos.getZ()<(r.getPos().getZ()+r.getY()-1):
					valid=True
					listOfRooms.append(r)
		for r in listOfRooms:
			decors=r.getDecors()
			for d in decors:
				if d.isBlockable()==1:
					if (pos.getX()+0.8)>(d.getPos().getX()) and pos.getX()<(d.getPos().getX()+d.getWidth()):
						if pos.getZ()>(d.getPos().getZ()) and pos.getZ()<(d.getPos().getZ()+d.getHeight()):
							valid=False
							collided=d
							
		for m in self.monsters:
			if (pos.getX()+1)>(m.getPos().getX()) and pos.getX()<(m.getPos().getX()+m.getWidth()):
				if pos.getZ()>(m.getPos().getZ()) and pos.getZ()<(m.getPos().getZ()+m.getHeight()):
					valid=False
					collided=m
					
		return valid,collided
		