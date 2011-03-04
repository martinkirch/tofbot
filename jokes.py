#!/usr/bin/env python

class Jokes(object):
	"""
	Awesome jokes
	"""
	
	__jokes = [
		"Sans blague!"
	]
	
	def get(self):
		return self.__class__.__jokes[0];

if __name__ == "__main__":
	joker = Jokes()
	print joker.get()
