# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *

class rocketUpStair():
	instance=None
	def __init__(self):
		rocketUpStair.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window = self.context.LoadDocument('windows/upstair.rml')
		
	@staticmethod
	def getInstance():
		if rocketUpStair.instance==None:
			rocketUpStair()
		return rocketUpStair.instance
			
	def getWindow(self):
		self.window.Show()
		return self.window
		
	def hideWindow(self):
		self.window.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		