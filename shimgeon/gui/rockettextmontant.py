class RocketTextMontant():
	nbWindow=0
	def __init__(self,el,doc,z):
		RocketTextMontant.nbWindow+=1
		self.id=RocketTextMontant.nbWindow
		self.element=el
		self.document=doc
		self.z=z
		self.startTime=globalClock.getRealTime()
		#~ taskMgr.add(self.render, "rocketdegat" + str(self.id))
		
	def render(self):
		self.element.SetAttribute("style","top:" + str(self.z) +"px;")
		self.z-=1
		if (globalClock.getRealTime()-self.startTime)>1:
			return True
		return False
		
	def destroy(self):
		if self.element!=None:
			content=self.document.GetElementById("contentdegat")
			content.RemoveChild(self.element)
		