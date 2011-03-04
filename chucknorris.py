#!/usr/bin/env python

class ChuckNorrisFacts(object):
	"""
	Awesome chuck norris facts
	"""
	
	__sentences = [
		"Chuck norris est trop fort",
		"Yippee chuck"
	]
	
	def get(self):
		return self.__class__.__sentences[0];

if __name__ == "__main__":
	facts = ChuckNorrisFacts()
	print facts.get()
