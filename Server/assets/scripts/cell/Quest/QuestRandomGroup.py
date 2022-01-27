# -*- coding: utf-8 -*-

import random
from Quest.Base.Quest import Quest

class QuestRandomGroup( Quest ):
	"""
	随机组任务
	"""
	def __init__( self ):
		Quest.__init__( self )
		self.childIDs = []
	
	def init( self, dataDict ):
		Quest.init( self, dataDict )
		if dataDict["param1"] != "":
			self.childIDs = [ int(i) for i in dataDict["param1"].split("|") ]
	
	def accept( self, player ):
		"""
		接任务
		"""
		if not len(self.childIDs):
			return
		questID = random.choice( self.childIDs )
		player.acceptQuest( questID )