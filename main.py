from pandac.PandaModules import loadPrcFileData 
loadPrcFileData("model-cache-dir",".\cache")
loadPrcFileData("audio-library-name","p3openal_audio")
loadPrcFileData("model-cache-textures", "1" )
#~ loadPrcFileData("default-far", "1000" )
loadPrcFileData('', 'win-size %i %i' % (1280, 720))
#~ loadPrcFileData('', 'win-size %i %i' % (640, 320))
loadPrcFileData('','fullscreen 0')
#~ loadPrcFileData("", "want-directtools #t")
#~ loadPrcFileData("", "want-tk #t")	
import sys,os
from array import array
#~ from theme import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
base.win.setCloseRequestEvent("CLOSEF4")
base.setBackgroundColor(0,0,0)
from shimgeon.game.gamestate import *
from shimgeon.game.game import *
from shimgeon.items.weapontemplate import *
from shimgeon.gui.rocketdeath import *
from shimgeon.gui.rocketstart import *
from shimgeon.level.level import *

#~ messenger.toggleVerbose()


class shimGeon(DirectObject):
	def __init__(self):
		base.camLens.setFar(40) 
		base.setFrameRateMeter(True)
		self.accept("escape",self.quitGame,)
		self.accept("CLOSEF4",self.quitGame,)
		taskMgr.add(self.dispatch,"dispatch Main",-40) 
		self.process=None
		
	def dispatch(self,task):
		if gameState.getInstance().getState()==C_INIT:
			gameState.getInstance().setState(C_MENU_START)
		elif gameState.getInstance().getState()==C_MENU_START:
			Level.reset()
			if isinstance(self.process,RocketStart)!=True:
				if self.process!=None:
					self.process.hideWindow()
				self.process=RocketStart.getInstance()
				self.process.getWindow()
		elif gameState.getInstance().getState()==C_GOPLAY:
			if isinstance(self.process,game)!=True:
				if self.process!=None:
					self.process.hideWindow()
			self.process=game()
			gameState.getInstance().setState(C_PLAYING)
		elif gameState.getInstance().getState()==C_CHANGING_LEVEL:
			if self.process!=None:
				self.process.destroy()
				self.process=None
				gameState.getInstance().setState(C_GOPLAY)
		elif gameState.getInstance().getState()==C_DEATH:
			if self.process!=None:
				self.process.destroy()
				self.process=None
			self.process=RocketDeath.getInstance()
			self.process.getWindow()
			gameState.getInstance().setState(C_MENU_DEATH)
		return task.cont
		
	def quitGame(self,):
		sys.exit()
		
app=shimGeon()
run()