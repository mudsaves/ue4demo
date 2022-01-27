# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class MapManager(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		self.cellData["position"] = (0.0, 0.0, 0.0)
		self.createCellEntityInNewSpace(None)
		
	def onGetCell( self ):
		"""
		创建cell实体
		"""
		INFO_MSG("MapManager onGetCell Entity")
		
	def createCellEntityOnMap( self, baseMailbox ):
		"""
		define method
		某个base请求在当前地图上创建cellEntity
		"""
		baseMailbox.createCellEntityOnMapCB( self.cell )
