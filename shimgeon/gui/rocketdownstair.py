# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *

class rocketDownStair():
	instance=None
	def __init__(self):
		rocketDownStair.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window = self.context.LoadDocument('windows/downstair.rml')
		#~ menuState.instance.setState(C_DEATH_WAITING)q
		
	@staticmethod
	def getInstance():
		if rocketDownStair.instance==None:
			rocketDownStair()
		return rocketDownStair.instance
			
	def getWindow(self):
		self.window.Show()
		return self.window
		
	def hideWindow(self):
		self.window.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		