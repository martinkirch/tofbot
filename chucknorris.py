#!/usr/bin/env python

class ChuckNorrisFacts(object):
	"""
	Awesome chuck norris facts
	"""
	
	__sentences = [
		("Chuck norris est tellement fort qu'il peut applaudir d'une seule main"),
		("Il n'y a que sur Google qu'on peut taper Chuck Norris")
	]
	
	def get(self):
		return self.__class__.__sentences[0];

if __name__ == "__main__":
	facts = ChuckNorrisFacts()
	print facts.get()
