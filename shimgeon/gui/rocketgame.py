# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from pandac.PandaModules import  Point2,Point3

from shimgeon.gui.shimrocket import *
from shimgeon.gui.rockettextmontant import *
from shimgeon.sprite.fx import *
from shimgeon.gui.rocketfx import *
from shimgeon.core.constantes import *
from shimgeon.sprite.character import *


class rocketGame():
	instance=None
	def __init__(self):
		rocketGame.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window=None
		self.window = self.context.LoadDocument('windows/backgroundgame.rml')
		self.slot=self.context.LoadDocument('windows/slotitem.rml')
		self.obj=None
		self.window.Show()
		self.slots={}
		self.textMontant=[]
		self.fx=[]
		taskMgr.add(self.render, "rocketgame")
		
	def onEquipTemplate(self,idTemplate):
		idSlot=int(self.slot.GetElementById("idslot").value)
		it=ItemTemplate.getTemplate(int(idTemplate))
		if it!=None:
			self.slots[idSlot]=it
			sl=self.window.GetElementById("slot" + str(idSlot))
			sl.SetAttribute("src","../" + it.getIcon())
			
	def use(self,idSlot):
		items=Character.getInstance().getInventory()
		if self.slots.has_key(int(idSlot))==True:
			if self.slots[int(idSlot)]!=None:
				idTemplate=self.slots[int(idSlot)].getId()
				for it in items:
					if it.getIdTemplate()==idTemplate:
						if it.getTypeItem()==C_ITEM_POTION:
							Character.getInstance().onDrink(it)
							break
						
			stillInInventory=False
			for it in items:
				if it.getIdTemplate()==idTemplate:
					stillInInventory=True
					break
			if stillInInventory==False:
				self.slots[int(idSlot)]=None
				sl=self.window.GetElementById("slot" + str(idSlot))
				sl.SetAttribute("src","../datas/gui/slot1.png" )
		
	def emptyWindow(self):
		content=self.slot.GetElementById("contentslotitem")
		listOfActualDiv=content.GetElementsByTagName("div")
		for div in listOfActualDiv:
			content.RemoveChild(div)
		
	def equipSlot(self,idSlot):
		self.emptyWindow()
		items=Character.getInstance().getInventory()
		content=self.slot.GetElementById("contentslotitem")
		self.slot.GetElementById("idslot").value=str(idSlot)
		i=0
		j=0
		for it in items:
			if i>4:
				i=0
				j+=1
			if it.getTypeItem()==C_ITEM_POTION:
				div=self.window.CreateElement("div")
				div.SetAttribute("style","position:absolute;top:" + str(80 + j*70) + "px;left:" + str((30+i*70)) + "px;width:70px;height:70px;")
				div.AddEventListener("mouseover","onShowItemInfo(" + str(it.getId()) + ")")
				div.AddEventListener("mouseout","onHideItemInfo()")
				el=self.window.CreateElement("img")
				suitable=True
				force,dexterite,constitution,intelligence,chance=it.getCaract()
				if force>Character.getInstance().getForce():
					suitable=False
				if dexterite>Character.getInstance().getDexterite():
					suitable=False
				if constitution>Character.getInstance().getConstitution():
					suitable=False
				if intelligence>Character.getInstance().getIntelligence():
					suitable=False
				if chance>Character.getInstance().getChance():
					suitable=False
				
				if suitable==False:
					ind=it.getIcon().find(".png")
					el.SetAttribute("src","../" + it.getIcon()[:ind] + "ko.png")
				else:
					el.SetAttribute("src","../" + it.getIcon())
					el.AddEventListener("dblclick","equip(" + str(it.getIdTemplate()) + ",document)")
				el.SetAttribute("width","64")
				
				div.AppendChild(el)
				content.AppendChild(div)
				i+=1
		self.slot.Show()
		
	def render(self,task):
		fToDestroy=[]
		for f in self.fx:
			if f.render()==True:
				fToDestroy.append(f)
				
		for f in fToDestroy:
			f.destroy()
			self.fx.remove(f)
			
		textToDestroy=[]
		for t in self.textMontant:
			if t.render()==True:
				textToDestroy.append(t)
				
		for t in textToDestroy:
			t.destroy()
			self.textMontant.remove(t)
			
		img=self.window.GetElementById("lifeimgchar")
		hp=Character.getInstance().getLife()
		hpMax=Character.getInstance().getLifeMax()
		prcent=int(100*round(float(hp)/float(hpMax),1))
		if prcent<0:
			prcent=0
		if prcent>100:
			prcent=100
		img.SetAttribute("src","../datas/gui/pgbv" + str(prcent) + ".png")
		div=self.window.GetElementById("divlifename")
		div.inner_rml="PV : " + str(hp) + "/" + str(hpMax)
		
		img=self.window.GetElementById("xpchar")
		xp=Character.getInstance().getXp()
		prev=Character.getInstance().getPreviousLevel()
		next=Character.getInstance().getNextLevel()
		nbXp=xp-prev
		xpToReach=next-prev
		prcent=int(100*round(float(nbXp)/float(xpToReach),1))
		if prcent<0:
			prcent=0
		if prcent>100:
			prcent=100
		img.SetAttribute("src","../datas/gui/pgb" + str(prcent) + ".png")
		div=self.window.GetElementById("divxpname")
		div.inner_rml="XP : " + str(xp) + "/" + str(next)
		
		div=self.window.GetElementById("divnamechar")
		div.inner_rml=Character.getInstance().getName() + " (Niv : " + str(Character.getInstance().getLevel()) + " )" + " Or : " + str(Character.getInstance().getMoney()) + " po"
		
		return task.cont
		
	
	@staticmethod
	def getInstance():
		if rocketGame.instance==None:
			rocketGame()
		return rocketGame.instance
		
	def showWindow(self):
		if self.window!=None:
			self.window.Show()
		return self.window
		
	def map3dToAspect2d(self, node, point): 
		"""Maps the indicated 3-d point (a Point3), which is relative to 
		the indicated NodePath, to the corresponding point in the aspect2d 
		scene graph. Returns the corresponding Point3 in aspect2d. 
		Returns None if the point is not onscreen. """ 

		# Convert the point to the 3-d space of the camera 
		p3 = base.cam.getRelativePoint(node, point) 

		# Convert it through the lens to render2d coordinates 
		p2 = Point2() 
		if not base.camLens.project(p3, p2): 
			return None 

		r2d = Point3(p2[0], 0, p2[1]) 

		# And then convert it to aspect2d coordinates 
		a2d = aspect2d.getRelativePoint(render2d, r2d) 

		return a2d
		
	def renderFx(self,obj,idFx,vit):
		pos=self.map3dToAspect2d(render,obj.getNode().getPos(render))
		x=pos.getX()
		z=pos.getZ()
		x+=C_RATIO_X
		x=(x*C_USER_WIDTH/(C_RATIO_X*2))-10
		z+=1
		z=C_USER_HEIGHT-(z*C_USER_HEIGHT/2)-20
		content=self.window.GetElementById("contentfx")
		div=self.window.CreateElement("div")
		div.SetAttribute("style","position:absolute;top:" + str(z) + "px;left:" + str(x) + "px;width:64px;height:64px;")
		content.AppendChild(div)
		f=RocketFx(div,self.window,idFx,vit)
		self.fx.append(f)
		
		
	def renderDegat(self,obj,degat,critique=False):
		if obj!=None:
			pos=self.map3dToAspect2d(render,obj.getNode().getPos(render))
			if pos!=None:		
				x=pos.getX()
				z=pos.getZ()
				x+=C_RATIO_X
				x=(x*C_USER_WIDTH/(C_RATIO_X*2))
				z+=1
				z=C_USER_HEIGHT-(z*C_USER_HEIGHT/2)-30
				content=self.window.GetElementById("contentdegat")
				div=self.window.CreateElement("div")
				div.SetAttribute("style","position:absolute;top:" + str(z) + "px;left:" + str(x) + "px;width:64px;height:64px;")
				if critique==True:
					div.inner_rml="<span style='color:red;font-size:22;'>critique " + str(degat) + "</span>"
				else:
					div.inner_rml="<span>" + str(degat) + "</span>"
				content.AppendChild(div)
				t=RocketTextMontant(div,self.window,z)
				self.textMontant.append(t)
				
	def renderGold(self,obj):
		if obj!=None:
			pos=self.map3dToAspect2d(render,obj.getNode().getPos(render))
			if pos!=None:		
				x=pos.getX()
				z=pos.getZ()
				x+=C_RATIO_X
				x=(x*C_USER_WIDTH/(C_RATIO_X*2))
				z+=1
				z=C_USER_HEIGHT-(z*C_USER_HEIGHT/2)-30
				content=self.window.GetElementById("contentdegat")
				div=self.window.CreateElement("div")
				div.SetAttribute("style","position:absolute;top:" + str(z) + "px;left:" + str(x) + "px;width:64px;height:64px;")
				div.inner_rml="<span style='color:yellow;'>" + str(obj.getNb()) + " po</span>"
				content.AppendChild(div)
				t=RocketTextMontant(div,self.window,z)
				self.textMontant.append(t)
		
	def renderLife(self,obj):
		hp=obj.getLife()
		hpMax=obj.getLifeMax()
		prcent=int(100*round(float(hp)/float(hpMax),1))
		if prcent>=0:
			divImg=self.window.GetElementById("divlifeimg")
			divImg.SetAttribute("style","display:Block;")
			img=self.window.GetElementById("lifeimg")
			if prcent>100:
				prcent=100
			img.SetAttribute("src","../datas/gui/pgbv" + str(prcent) + ".png")
			divName=self.window.GetElementById("divname")
			divName.SetAttribute("style","display:Block;")
			if obj.isBoss()==1:
				divName.inner_rml="<span style='color:#ff0000;'>Boss " + obj.getName() + " (Niv " + str(obj.getLevel()) + ")</span>"
			else:
				divName.inner_rml="<span>" + obj.getName() + " (Niv " + str(obj.getLevel()) + ")</span>"
		
			
	def noRenderLife(self):
		divName=self.window.GetElementById("divname")
		divName.SetAttribute("style","display:None;")
		divImg=self.window.GetElementById("divlifeimg")
		divImg.SetAttribute("style","display:None;")
		
		
	def hideWindow(self):
		self.window.Hide()
		self.slot.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		self.context.UnloadDocument(self.slot)
		