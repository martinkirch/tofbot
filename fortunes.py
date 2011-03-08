#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class Fortunes(object):
	"""
	Awesome fortunes
	"""
	
	__fortunes = [
		("Qui sème le vent récolte le tempo."),
		("Allez voir là-bas si j'y suis. Et ils marchèrent.")
	]
	
	def get(self, index = None):
		pool = self.__class__.__fortunes
		if index:
			return pool[index % len(pool)];
		else:
			random.seed()
			return pool[ random.randint(0, len(pool)-1) ];

if __name__ == "__main__":
	joker = Fortunes()
	print joker.get()
	print joker.get(1)
