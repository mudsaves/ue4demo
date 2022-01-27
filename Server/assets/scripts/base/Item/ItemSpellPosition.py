# -*- coding: utf-8 -*-

import csdefine
import csstatus
from Item.Base.ItemBase import ItemBase

class ItemSpellPosition( ItemBase ):
	"""
	对位置使用的技能物品
	"""
	def __init__( self ):
		ItemBase.__init__( self )
		self.skillID = 0
	
	def init( self, itemID, cfgDict ):
		"""
		读取配置数据
		"""
		ItemBase.init( self, itemID, cfgDict )
		self.skillID = cfgDict["skillID"]