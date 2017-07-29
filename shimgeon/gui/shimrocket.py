from panda3d.rocket import *

class shimRocket:
	instance=None
	def __init__(self):
		#~ LoadFontFace("assets/brassiere.ttf")
		#~ LoadFontFace("assets/HWYGOTH.TTF")
		LoadFontFace("assets/hwygoth.ttf")
		#~ LoadFontFace("assets/Verah___.ttf")

		r = RocketRegion.make('pandaRocket', base.win)
		r.setActive(1)
		self.context = r.getContext()
		ih = RocketInputHandler()
		base.mouseWatcher.attachNewNode(ih)
		r.setInputHandler(ih)
	
	@staticmethod
	def getInstance():
		if shimRocket.instance==None:
			shimRocket.instance=shimRocket()
			
		return shimRocket.instance
		
	def getContext(self):
		return self.context
		
