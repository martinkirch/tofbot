#!/usr/bin/env python

class Tofades(object):
	"""
	Awesome tofades
	"""
	
	__sentences = [
		("Ho ho ho"),
		("Ha ha ha")
	]
	
	def get(self):
		return self.__class__.__sentences[0];

if __name__ == "__main__":
	tof = Tofades()
	print tof.get()
