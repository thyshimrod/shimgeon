from math import sqrt

def calcDistance(pos1,pos2):
	dx=pos1.getX()-pos2.getX()
	dy=pos1.getY()-pos2.getY()
	dz=pos1.getZ()-pos2.getZ()
	currentDistance=int(round(sqrt(dx*dx+dy*dy+dz*dz),0))
	return currentDistance