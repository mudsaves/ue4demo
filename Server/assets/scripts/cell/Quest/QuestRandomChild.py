# -*- coding: utf-8 -*-

from Quest.Base.Quest import Quest

class QuestRandomChild( Quest ):
	"""
	随机子任务
	"""
	def __init__( self ):
		Quest.__init__( self )
		self.groupIDs = []
	
	def init( self, dataDict ):
		Quest.init( self, dataDict )
		if dataDict["param1"] != "":
			self.groupIDs = [ i for i in dataDict["param1"].split("|") ]