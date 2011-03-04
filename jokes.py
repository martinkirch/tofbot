#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class Jokes(object):
	"""
	Awesome jokes
	"""
	
	__jokes = [
		("Voici l'histoire de Toto aux toilettes..."),
		("Une autre histoire")
	]
	
	def get(self, index = None):
		pool = self.__class__.__jokes
		if index:
			return pool[index % len(pool)];
		else:
			random.seed()
			return pool[ random.randint(0, len(pool)-1) ];

if __name__ == "__main__":
	joker = Jokes()
	print joker.get()
	print joker.get(1)
