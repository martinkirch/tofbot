#!/usr/bin/env python

class Riddles(object):
	"""
	Awesome riddles
	"""
	
	__jokes = [
		("Tu connais l'histoire de Toto au toilettes?", "Ben moi non plus")
	]
	
	def get(self):
		return self.__class__.__jokes[0];

if __name__ == "__main__":
	joker = Riddles()
	print joker.get()
