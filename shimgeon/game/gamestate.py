C_INIT=0
C_GOPLAY=2
C_PLAYING=3
C_CHANGING_LEVEL=4
C_DEATH=5
C_MENU_DEATH=6
C_MENU_START=7
C_MENU_CHOOSE_CHAR=8

class gameState:
	instance=None
	def __init__(self):
		self.state=C_INIT
		gameState.instance=self
		self.level=0
		
	def getLevel(self):
		return self.level
		
	def setLevel(self,lvl):
		self.level=lvl
	
	def getState(self):
		return self.state
		
	def setState(self,state):
		self.state=state
		
	@staticmethod
	def getInstance():
		if gameState.instance==None:
			gameState.instance=gameState()
			
		return gameState.instance