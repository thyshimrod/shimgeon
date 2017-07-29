# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *
from shimgeon.sprite.charactertemplate import *
from shimgeon.sprite.character import *
from shimgeon.game.gamestate import *

class RocketStart():
	instance=None
	def __init__(self):
		RocketStart.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.background= self.context.LoadDocument('windows/background.rml')
		self.window = self.context.LoadDocument('windows/start.rml')
		self.window2 = self.context.LoadDocument('windows/choosehero.rml')
		self.currentTemplate=0
		
	@staticmethod
	def getInstance():
		if RocketStart.instance==None:
			RocketStart()
		return RocketStart.instance
		
	def prec(self):
		self.currentTemplate-=1
		templates=CharacterTemplate.getListOfTemplate()
		if self.currentTemplate<0:
			self.currentTemplate=len(templates)-1
		self.showTemplate()
		
	def next(self):
		self.currentTemplate+=1
		templates=CharacterTemplate.getListOfTemplate()
		if self.currentTemplate>=len(templates):
			self.currentTemplate=0
		self.showTemplate()
		
	def showTemplate(self):
		templates=CharacterTemplate.getListOfTemplate()
		i=0
		for ch in CharacterTemplate.getListOfTemplate():
			if i==self.currentTemplate:
				i=ch
				break
			i+=1
		ch=templates[i]
		img="../" + ch.getPath() + "/down1.png"
		face=self.window2.GetElementById("face")
		face.SetAttribute("src",str(img))
		name=self.window2.GetElementById("nametemplate")
		name.inner_rml=str(ch.getName())
		name.value=str(ch.getName())
		idtemplate=self.window2.GetElementById("idtemplate")
		idtemplate.value=str(ch.getId())
		
	def chooseHero(self):
		self.window.Hide()
		self.showTemplate()
		self.window2.GetElementById("name").Focus()
		self.window2.Show()
		
	def play(self):
		idtemplate=self.window2.GetElementById("idtemplate").value
		ch=Character(int(idtemplate))
		ch.setName(self.window2.GetElementById("name").value)
		gameState.getInstance().setState(C_GOPLAY)

	def getWindow(self):
		self.background.Show()
		print self.background
		self.background.PullToFront()
		self.window.PullToFront()
		self.window.Show()
		return self.window
		
	def hideWindow(self):
		self.background.Hide()
		self.window.Hide()
		self.window2.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		self.context.UnloadDocument(self.window2)
		self.context.UnloadDocument(self.background)
		