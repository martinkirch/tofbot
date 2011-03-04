#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class ChuckNorrisFacts(object):
	"""
	Awesome chuck norris facts
	"""
	
	__sentences = [
		("Chuck norris est tellement fort qu'il peut applaudir d'une seule main"),
		("Il n'y a que sur Google qu'on peut taper Chuck Norris")
	]
	
	def get(self, index = None):
		pool = self.__class__.__sentences
		if index:
			return pool[index % len(pool)];
		else:
			random.seed()
			return pool[ random.randint(0, len(pool)-1) ];

# tester
if __name__ == "__main__":
	facts = ChuckNorrisFacts()
	print facts.get()
	print facts.get(1)
