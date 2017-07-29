# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *
from shimgeon.sprite.character import *

class RocketCaract():
	instance=None
	def __init__(self):
		RocketCaract.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window = self.context.LoadDocument('windows/caract.rml')
		self.show=False
		
	@staticmethod
	def getInstance():
		if RocketCaract.instance==None:
			RocketCaract()
		return RocketCaract.instance
		
	def addCarac(self,car):
		Character.getInstance().setCaractPoint(int(car))
		self.showCaract()
	
	def showCaract(self):
		char=Character.getInstance()
		d=self.window.GetElementById("force")
		d.inner_rml=str(char.getForce())
		d=self.window.GetElementById("dexterite")
		d.inner_rml=str(char.getDexterite())
		d=self.window.GetElementById("constitution")
		d.inner_rml=str(char.getConstitution())
		d=self.window.GetElementById("intelligence")
		d.inner_rml=str(char.getIntelligence())
		d=self.window.GetElementById("chance")
		d.inner_rml=str(char.getChance())
		d=self.window.GetElementById("skillpoints")
		d.inner_rml=str(char.getSkillPoints())
		
		if char.getSkillPoints()>0:
			self.window.GetElementById("pluschance").SetAttribute("style","display:Block;")
			self.window.GetElementById("plusintelligence").SetAttribute("style","display:Block;")
			self.window.GetElementById("plusconstitution").SetAttribute("style","display:Block;")
			self.window.GetElementById("plusdexterite").SetAttribute("style","display:Block;")
			self.window.GetElementById("plusforce").SetAttribute("style","display:Block;")
			self.window.GetElementById("skillpoints").SetAttribute("style","display:Block;")
		else:
			self.window.GetElementById("pluschance").SetAttribute("style","display:None;")
			self.window.GetElementById("plusintelligence").SetAttribute("style","display:None;")
			self.window.GetElementById("plusconstitution").SetAttribute("style","display:None;")
			self.window.GetElementById("plusdexterite").SetAttribute("style","display:None;")
			self.window.GetElementById("plusforce").SetAttribute("style","display:None;")
			self.window.GetElementById("skillpoints").SetAttribute("style","display:None;")

	def getWindow(self):
		if self.show==False:
			self.show=True
			self.showCaract()
			self.window.Show()
		else:
			self.show=False
			self.window.Hide()
		return self.window
		
	def hideWindow(self):
		self.window.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		