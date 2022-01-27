# -*- coding: utf-8 -*-

import csdefine
import KBEngine
import json
from Item.Base.ItemBase import ItemBase

class ItemWeapon( ItemBase ):
	"""
	武器
	"""
	def __init__( self ):
		ItemBase.__init__( self )
		self.hardiness = 0	#耐久度
	
	def init( self, itemID, cfgDict ):
		"""
		读取配置数据
		"""
		ItemBase.init( self, itemID, cfgDict )
		self.hardiness = cfgDict["hardiness"]
		self.stackAmount = 1	#覆盖基类中的赋值，武器不支持叠加
	
	def packetExtraData( self ):
		"""
		virtual method
		将动态的自定义属性打包成字典
		"""
		extraDict = ItemBase.packetExtraData( self )
		extraDict["hardiness"] = self.hardiness
		return extraDict
	
	def setHardiness( self, hardiness, owner = None ):
		"""
		"""
		self.hardiness = hardiness
		if owner:
			stream = json.dumps({"type":"int32", "value":hardiness})
			owner.client.onItemAttrUpdated( self.order, "hardiness", stream )
	
	def getHardiness( self ):
		"""
		"""
		return self.hardiness
	
	def wield( self, owner ):
		"""
		装备到身上
		"""
		pass
	
	def unwield( self, owner ):
		"""
		从身上移除
		"""
		pass
	
	def isStackableToItem( self, targetItem ):
		"""
		virtual method
		自己可以堆叠到某物品所在物品格
		"""
		return False	#武器不支持堆叠