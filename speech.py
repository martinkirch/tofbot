class SentenceCollection(object):
	"""
	Base class for sentences provider
	This one implements all accessors (random, sequencial, etc...)
	Child classes are only wrapping thematic setences wrappers
	"""
	
	__sentences = []
	
	def get(self):
		return self.__class__.__sentences[0]

