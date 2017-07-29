# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *
from shimgeon.core.constantes import *
from shimgeon.items.item import *
from shimgeon.items.weapon import *
from shimgeon.items.itemfactory import *
from shimgeon.sprite.character import *

class rocketItemInfo():
	instance=None
	def __init__(self):
		rocketItemInfo.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window = self.context.LoadDocument('windows/infoitem.rml')
		self.items=[]
		
	@staticmethod
	def getInstance():
		if rocketItemInfo.instance==None:
			rocketItemInfo()
		return rocketItemInfo.instance
		
	def emptyWindow(self):
		content=self.window.GetElementById("contentiteminfo")
		
		listOfActualDiv=content.GetElementsByTagName("div")
		for div in listOfActualDiv:
			content.RemoveChild(div)
			
		
	def showWindow(self,idItem):
		mouseX=(base.mouseWatcherNode.getMouseX()+1)
		mouseY=(base.mouseWatcherNode.getMouseY()+1)
		if mouseX<=1:
			mouseX*=float(C_USER_WIDTH/2)
			mouseX+=100
		else:
			mouseX*=float(C_USER_WIDTH/2)
			mouseX-=400
		mouseY*=float(C_USER_HEIGHT/2)
		mouseY=C_USER_HEIGHT-mouseY
		mouseY-=100

		self.window.SetAttribute("style","body{width:300px;height:250px;top:" + str(mouseY) + "px;left:" + str(mouseX) + "px;}")
		
		self.emptyWindow()
		
		obj=ItemFactory.getItemObj(idItem)
			
		content=self.window.GetElementById("contentiteminfo")
		div=self.window.CreateElement("div")
		div.SetAttribute("style","position:absolute;top:70px;left:200px;width:50px;")
		el=self.window.CreateElement("img")
		el.SetAttribute("src","../" + obj.getIcon())
		el.SetAttribute("style","width:64;height:64;")
		div.AppendChild(el)
		content.AppendChild(div)
		
		div=self.window.CreateElement("div")
		div.SetAttribute("style","position:absolute;top:70px;left:30px;width:50px;")
		div.inner_rml=obj.getName()
		content.AppendChild(div)
				
		top=130
		if obj.getTypeItem()==C_ITEM_WEAPON:
			div=self.window.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:130px;left:30px;width:100px;")
			div.inner_rml="degats : " + str(obj.getDegatMin()) + "-" + str(obj.getDegatMax())
			content.AppendChild(div)
			div=self.window.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:160px;left:30px;width:100px;")
			div.inner_rml="Portee : " + str(obj.getRange())
			content.AppendChild(div)
			div=self.window.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:190px;left:30px;width:100px;")
			div.inner_rml="Vitesse : " + str(obj.getVitesse())
			content.AppendChild(div)
			top=220
		elif obj.getTypeItem()==C_ITEM_ARMOR:
			div=self.window.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:130px;left:30px;width:100px;")
			div.inner_rml="Armure : " + str(obj.getArmure())
			content.AppendChild(div)
			top=160
		elif obj.getTypeItem()==C_ITEM_POTION:
			div=self.window.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:130px;left:0px;width:200px;")
			div.inner_rml="Gain de vie : " + str(obj.getLife())
			content.AppendChild(div)
			top=160
			
		### Bonus ########################	
		bonus=obj.getBonus()
		for b in bonus:
			div=self.window.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:" + str(top+30) + "px;left:0px;width:200px;color:#1e90ff;")
			if b==C_BONUS_FORCE:
				div.inner_rml="Force : + " + str(bonus[b])
			elif b==C_BONUS_DEXTERITE:
				div.inner_rml="Dexterite : + " + str(bonus[b])
			elif b==C_BONUS_INTELLIGENCE:
				div.inner_rml="Intelligence : + " + str(bonus[b])
			elif b==C_BONUS_CONSTITUTION:
				div.inner_rml="Constitution : + " + str(bonus[b])
			elif b==C_BONUS_CHANCE:
				div.inner_rml="Chance : + " + str(bonus[b])
			elif b==C_BONUS_DEGAT:
				div.inner_rml="Degat : + " + str(bonus[b])
			elif b==C_BONUS_PORTEE:
				div.inner_rml="Force : + " + str(bonus[b])
			elif b==C_BONUS_VITESSE:
				div.inner_rml="Force : - " + str(bonus[b])
			elif b==C_BONUS_ARMOR:
				div.inner_rml="Armure : + " + str(bonus[b])
			content.AppendChild(div)
			
			top+=30	
		### Prerequis ########################	
		div=self.window.CreateElement("div")
		div.SetAttribute("style","position:absolute;top:" + str(top+30) + "px;left:30px;width:100px;")
		div.inner_rml="Prerequis"
		content.AppendChild(div)
		div=self.window.CreateElement("div")
		div.SetAttribute("style","position:absolute;top:" + str(top+60) + "px;left:20px;width:150px;")
		text="<span>"
		force,dexterite,constitution,intelligence,chance=obj.getCaract()
		char=Character.getInstance()
		if force>0:
			if char.getForce()>=force:
				text+="<p>Force : " + str(force) + "</p>"
			else:
				text+="<p> <span style='color:#ff0000;'>Force : " + str(force) + "</span></p>"
		if dexterite>0:
			if char.getDexterite()>=dexterite:
				text+="<p>Dexterite : " + str(dexterite) + "</p>"
			else:
				text+="<p> <span style='color:#ff0000;'>Force : " + str(force) + "</span></p>"
		if constitution>0:
			if char.getConstitution()>=constitution:
				text+="<p>Consitution : " + str(constitution) + "</p>"
			else:
				text+="<p> <span style='color:#ff0000;'>Force : " + str(force) + "</span></p>"
		if intelligence>0:
			if char.getIntelligence()>=intelligence:
				text+="<p>Intelligence : " + str(intelligence) + "</p>"
			else:
				text+="<p> <span style='color:#ff0000;'>Force : " + str(force) + "</span></p>"
		if chance>0:
			if char.getChance()>=chance:
				text+="<p>Chance : " + str(chance) + "</p>"
			else:
				text+="<p> <span style='color:#ff0000;'>Force : " + str(force) + "</span></p>"
		text+="</span>"
		div.inner_rml=text
		content.AppendChild(div)
		
		self.window.Show()
		
	def hideWindow(self):
		self.window.Hide()
		