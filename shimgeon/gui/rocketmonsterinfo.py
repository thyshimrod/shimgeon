# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *


class rocketGame():
	instance=None
	def __init__(self):
		rocketGame.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window=None
		self.window = self.context.LoadDocument('windows/backgroundgame.rml')
		self.obj=None
		
	@staticmethod
	def getInstance():
		if rocketGame.instance==None:
			rocketGame()
		return rocketGame.instance
		
	def showWindow(self):
		if self.window!=None:
			self.window.Show()
		return self.window
		
	def renderLife(self,obj):
			#~ ship=user.instance.getCurrentCharacter().ship
			#~ hp=ship.getHullPoints()
			#~ hpmax=ship.getMaxHullPoints()
			
			#~ prcent=int(100*round(float(hp)/float(hpmax),1))
		img=self.window.GetElementById("lifeimg")
		img.SetAttribute("src","datas/gui/pgb100.png")
		self.window.Show()
			
		
		
	def hideWindow(self):
		self.window.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		