# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *

class QuestAfterScript:
	"""
	提交任务或放弃任务时要执行的脚本
	"""
	def __init__( self ):
		pass
	
	def init( self, dataDict ):
		pass

	def onSubmit( self, player ):
		"""
		提交任务执行此接口
		"""
		pass
	
	def onAbandon( self, player ):
		"""
		放弃任务执行此接口
		"""
		pass

class QASRemoveItem( QuestAfterScript ):
	"""
	删除物品
	"""
	def __init__( self ):
		self.itemID = 0
		self.amount = 0
	
	def init( self, dataDict ):
		self.itemID = int( dataDict["param1"] )
		self.amount = int( dataDict["param2"] )
	
	def onSubmit( self, player ):
		"""
		提交任务执行此接口
		"""
		#player.removeItem( self.itemID, self.amount )
		DEBUG_MSG("Remove item on submit quest. itemID(%s), itemAmount(%s)"%( self.itemID, self.amount ))
	
	def onAbandon( self, player ):
		"""
		放弃任务执行此接口
		"""
		#player.removeItem( self.itemID, self.amount )
		DEBUG_MSG("Remove item on abandon quest. itemID(%s), itemAmount(%s)"%( self.itemID, self.amount ))

def newInstance( className ):
	try:
		return eval( className )()
	except:
		return None