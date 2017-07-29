# -*- coding: utf-8 -*- 
import sys,os
from panda3d.rocket import *
from shimgeon.gui.shimrocket import *
from shimgeon.sprite.character import *

class RocketDeath():
	instance=None
	def __init__(self):
		RocketDeath.instance=self
		self.context = shimRocket.getInstance().getContext()
		self.window = self.context.LoadDocument('windows/death.rml')
		
	@staticmethod
	def getInstance():
		if RocketDeath.instance==None:
			RocketDeath()
		return RocketDeath.instance
		
	def emptyWindow(self):
		content=self.window.GetElementById("content")
		listOfActualDiv=content.GetElementsByTagName("div")
		for div in listOfActualDiv:
			content.RemoveChild(div)
		
	def displayScore(self):
		self.emptyWindow()
		char=Character.getInstance()
		score=0
		score+=(char.getLevel()-1)*100
		score+=char.getMoney()
		score+=char.getDungeonLevelReached()*100
		monsters=char.getMonsters()
		mm=""
		nbMonster=0
		for m in monsters:
			nbMonster+=monsters[m]
			mm+="<p> -- " + str(monsters[m]) + " " + str(m) + "</p>"
			
		content=self.window.GetElementById("content")
		div=self.window.CreateElement("div")
		div.SetAttribute("id","generate")
		text="<span><p>" + str(char.getName()) + ", vous avez acquis " + str(score) + " pts</p>"
		text+="<p> Vous etiez " + char.getClasse() + "</p>"
		text+="<p> Vous etes niveau " + str(char.getLevel()) + "-1 * 100 = " + str((char.getLevel()-1)*100) + " pts</p>"
		text+="<p> Vous etes descendu au niveau " + str(char.getDungeonLevelReached()) + " * 100 = " + str(char.getDungeonLevelReached()*100) + " pts</p>"
		text+="<p> Vous avez ramasse " + str(char.getMoney()) + " = " + str(char.getMoney()) + " pts</p>"
		text+="<p> Vous avez tue  " + str(nbMonster) + " monsters = " + str(nbMonster) + " pts </p>"
		text+=mm
		text+="</span>"
		div.inner_rml=text
		div.SetAttribute("style","position:absolute;top:200px;left:100px;width:800px;height:500px;border: 1px solid #666;vertical-align :top;")
		content.AppendChild(div)
		div=self.window.CreateElement("div")
		div.SetAttribute("style","position:absolute; top:50px; left:50px;z-index:10;")
		btn=self.window.CreateElement("button")
		btn.SetAttribute("style","width:100px;height:30px;")
		btn.SetAttribute("class","topress")
		btn.SetAttribute("id","btnok")
		btn.AddEventListener("click","onOk(document)")
		btn.inner_rml="<span>Rejouer</span>"
		div.AppendChild(btn)
		content.AppendChild(div)


	def getWindow(self):
		self.displayScore()
		self.window.Show()
		return self.window
		
	def hideWindow(self):
		self.window.Hide()
		
	def destroy(self):
		self.context.UnloadDocument(self.window)
		