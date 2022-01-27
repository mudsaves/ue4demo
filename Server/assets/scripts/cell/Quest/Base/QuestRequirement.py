# -*- coding: utf-8 -*-

import csdefine

class QuestRequirement:
	"""
	接任务条件
	"""
	def __init__( self ):
		pass
	
	def init( self, dataDict ):
		pass
	
	def query( self, player ):
		"""
		"""
		return True

class QRHasBuff( QuestRequirement ):
	"""
	身上有某ID的buff
	"""
	def __init__( self ):
		self.buffID = 0
	
	def init( self, dataDict ):
		self.buffID = int( dataDict["param1"] )
	
	def query( self, player ):
		"""
		"""
		return len( player.getBuffIndexByID( self.buffID ) ) != 0

def newInstance( className ):
	try:
		return eval( className )()
	except:
		return None