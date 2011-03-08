#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class Riddles(object):
	"""
	Awesome riddles
	"""
	
	__jokes = [
		("Tu connais l'histoire de Toto au toilettes?", "Ben moi non plus"),
		("Où est charlie?", "Sur ta mère"),
                ("Qu'est-ce qui est vert, qui vit sous terre, et qui mange des pierres ?", "Le mange cailloux")
	]
	
	def get(self, index = None):
		pool = self.__class__.__jokes
		if index:
			return pool[index % len(pool)];
		else:
			random.seed()
			return pool[ random.randint(0, len(pool)-1) ];

if __name__ == "__main__":
	joker = Riddles()
	print joker.get()
	print joker.get(1)
