# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *
from shimgeon.sprite.character import *
from shimgeon.items.itemfactory import *

class RocketEquip():
	instance=None
	def __init__(self):
		RocketEquip.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window = self.context.LoadDocument('windows/equip.rml')
		self.windowChoose= self.context.LoadDocument('windows/onequip.rml')
		self.show=False
		
	@staticmethod
	def getInstance():
		if RocketEquip.instance==None:
			RocketEquip()
		return RocketEquip.instance
		
	def onChoose(self,objId):
		inputId=self.windowChoose.GetElementById("iditem")
		inputId.value=str(objId)
		self.windowChoose.Show()
		
	def onDelete(self,objId):
		obj=ItemFactory.getItemObj(int(objId))
		print "RocketEquip::onDelete" + str(obj)
		Character.getInstance().onDelete(obj)
		self.emptyWindow()
		self.showInventory()
		
	def onEquip(self,objId):
		obj=ItemFactory.getItemObj(int(objId))
		if obj.getTypeItem()==C_ITEM_WEAPON or obj.getTypeItem()==C_ITEM_ARMOR:
			Character.getInstance().onEquip(obj)
		elif obj.getTypeItem()==C_ITEM_POTION:
			Character.getInstance().onDrink(obj)
		self.emptyWindow()
		self.showInventory()

	def emptyWindow(self):
		content=self.window.GetElementById("contentequip")
		listOfActualDiv=content.GetElementsByTagName("div")
		for div in listOfActualDiv:
			content.RemoveChild(div)

	def showInventory(self):
		items=Character.getInstance().getInventory()
		content=self.window.GetElementById("contentequip")
		i=0
		j=0
		for it in items:
			if i>4:
				i=0
				j+=1
			div=self.window.CreateElement("div")
			div.SetAttribute("style","position:absolute;top:" + str(100 + j*70) + "px;left:" + str((450+i*70)) + "px;width:70px;height:70px;")
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
				el.AddEventListener("dblclick","onEquip(" + str(it.getId()) + ")")
			el.SetAttribute("width","64")
			
			div.AppendChild(el)
			content.AppendChild(div)
			i+=1
		
		div=self.window.GetElementById("divlefthand")
		img=self.window.GetElementById("lefthand")
		if Character.getInstance().getLeftHand()!=None:
			img.SetAttribute("src","../" + Character.getInstance().getLeftHand().getIcon())
			div.AddEventListener("mouseover","onShowItemInfo(" + str(Character.getInstance().getLeftHand().getId()) + ")")
			div.AddEventListener("mouseout","onHideItemInfo()")
		else:
			img.SetAttribute("src","../datas/gui/slot1.png")
			
		div=self.window.GetElementById("divrighthand")
		img=self.window.GetElementById("righthand")
		if Character.getInstance().getRightHand()!=None:
			img.SetAttribute("src","../" + Character.getInstance().getRightHand().getIcon())
			div.AddEventListener("mouseover","onShowItemInfo(" + str(Character.getInstance().getRightHand().getId()) + ")")
			div.AddEventListener("mouseout","onHideItemInfo()")
		else:
			img.SetAttribute("src","../datas/gui/slot1.png")
			
		div=self.window.GetElementById("divmiddle")
		img=self.window.GetElementById("middle")
		if Character.getInstance().getMiddle()!=None:
			img.SetAttribute("src","../" + Character.getInstance().getMiddle().getIcon())
			div.AddEventListener("mouseover","onShowItemInfo(" + str(Character.getInstance().getMiddle().getId()) + ")")
			div.AddEventListener("mouseout","onHideItemInfo()")
		else:
			img.SetAttribute("src","../datas/gui/slot1.png")
			
		div=self.window.GetElementById("divglove")
		img=self.window.GetElementById("glove")
		if Character.getInstance().getGlove()!=None:
			img.SetAttribute("src","../" + Character.getInstance().getGlove().getIcon())
			div.AddEventListener("mouseover","onShowItemInfo(" + str(Character.getInstance().getGlove().getId()) + ")")
			div.AddEventListener("mouseout","onHideItemInfo()")
		else:
			img.SetAttribute("src","../datas/gui/slot1.png")
			
		div=self.window.GetElementById("divhead")
		img=self.window.GetElementById("head")
		if Character.getInstance().getHead()!=None:
			img.SetAttribute("src","../" + Character.getInstance().getHead().getIcon())
			div.AddEventListener("mouseover","onShowItemInfo(" + str(Character.getInstance().getHead().getId()) + ")")
			div.AddEventListener("mouseout","onHideItemInfo()")
		else:
			img.SetAttribute("src","../datas/gui/slot1.png")
			
		div=self.window.GetElementById("divfeet")
		img=self.window.GetElementById("feet")
		if Character.getInstance().getFeet()!=None:
			img.SetAttribute("src","../" + Character.getInstance().getFeet().getIcon())
			div.AddEventListener("mouseover","onShowItemInfo(" + str(Character.getInstance().getFeet().getId()) + ")")
			div.AddEventListener("mouseout","onHideItemInfo()")
		else:
			img.SetAttribute("src","../datas/gui/slot1.png")

	def getWindow(self):
		if self.show==False:
			self.show=True
			self.emptyWindow()
			self.showInventory()
			self.window.Show()
		else:
			self.show=False
			self.window.Hide()
		return self.window
		
	def hideWindow(self):
		self.window.Hide()
		self.windowChoose.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		self.context.UnloadDocument(self.windowChoose)
		