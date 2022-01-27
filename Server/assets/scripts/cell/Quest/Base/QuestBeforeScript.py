# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *

class QuestBeforeScript:
	"""
	接任务前要执行的脚本
	"""
	def __init__( self ):
		pass
	
	def init( self, dataDict ):
		pass
	
	def query( self, player ):
		"""
		能否执行
		"""
		return True
	
	def do( self, player ):
		pass

class QBSGiveItem( QuestBeforeScript ):
	"""
	给物品
	"""
	def __init__( self ):
		self.itemID = 0
		self.amount = 0
	
	def init( self, dataDict ):
		self.itemID = int( dataDict["param1"] )
		self.amount = int( dataDict["param2"] )
	
	def query( self, player ):
		"""
		能否执行
		"""
		#return player.itemBag.getEmptyPlaceAmount() >= self.amount
		return True
	
	def do( self, player ):
		#player.addItem( self.itemID, self.amount )
		DEBUG_MSG("Give item before accept quest. itemID(%s), itemAmount(%s)."%( self.itemID, self.amount ))

def newInstance( className ):
	try:
		return eval( className )()
	except:
		return None
