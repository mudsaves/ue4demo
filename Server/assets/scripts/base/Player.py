# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Player(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		self.cellData["position"] = (0.0, 0.0, 0.0)
		self.addTimer( 5, 1, 0 )
		
		INFO_MSG("create Player Entity")
		# 在全局的地图空间创建自己的Cell
		cellMailbox = KBEngine.globalData["MapManager"]
		if cellMailbox is not None:
			self.createCellEntity( cellMailbox.cell )
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		pass	
		
	def onGetCell( self ):
		"""
		创建cell实体
		"""
		INFO_MSG("onGetCell Entity")
		
