# -*- coding: utf-8 -*-

import weakref

class StateDefine(object):
	"""
	"""
	NULL = 0
	Dead = 1
	Quest = 2
	LoopQuest = 3
	RandMove = 4
	Fight = 5
	Wait = 6

class AIStateBase(object):
	"""
	角色AI状态基类
	"""
	def __init__(self, ai):
		"""
		"""
		self.ai = weakref.proxy(ai)
	
	def getPlayerEventObj( self ):
		return self.ai.owner.eventObj
	
	def enter(self):
		"""
		virtual method
		"""
		pass
		
	def leave(self):
		"""
		virtual method
		"""
		pass
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		"""
		pass
