from shimgeon.sprite.fx import *
class RocketFx():
	nbWindow=0
	def __init__(self,el,doc,fx,time):
		RocketFx.nbWindow+=1
		self.id=RocketFx.nbWindow
		self.element=el
		self.time=time
		self.startTimer=globalClock.getRealTime()
		self.fx=FX.getFx(fx)
		img=doc.CreateElement("img")
		img.SetAttribute("src","../" + self.fx.getPath() + self.fx.getName() + "1" + self.fx.getExtension())
		img.SetAttribute("width","32")
		img.SetAttribute("height","32")
		self.element.AppendChild(img)
		self.document=doc
		
	def render(self):
		if (globalClock.getRealTime()-self.startTimer)>self.time:
			return True
		return False
		
	def destroy(self):
		if self.element!=None:
			content=self.document.GetElementById("contentfx")
			content.RemoveChild(self.element)
			#~ taskMgr.remove("rocketdegat" + str(self.id))
		
		