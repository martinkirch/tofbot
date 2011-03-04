#!/usr/bin/env python

from speech import SentenceCollection

class ChuckNorrisFacts(SentenceCollection):
	"""
	Awesome chuck norris facts
	"""
	
	__sentences = [
		"Chuck norris est trop fort",
		"Yippee chuck"
	]

if __name__ == "__main__":
	facts = ChuckNorrisFacts()
	print facts.get()
