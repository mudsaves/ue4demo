# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import random
import time
from AI.Base.AICfgLoader import g_aiCfgLoader

class MapManager(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		# 创建一个打开的门的实体与"thing"实体的位置一样
		direction = ( 0.0, 0.0, 0.0 )
		properties = { "modelID":1, "moveSpeed":1.0 }

		KBEngine.setSpaceData(self.spaceID, "MetaClass", self.mapType)
		KBEngine.setSpaceData(self.spaceID, "MappingPath", self.mappingPath)
		KBEngine.setSpaceData(self.spaceID, "AttackRelationKey", self.attackRelationKey)
		
		if len(self.mappingPath):
			KBEngine.addSpaceGeometryMapping( self.spaceID, None, "spaces/" + self.mappingPath )
		else:
			WARNING_MSG( "space %s has no geometry mapping." % (self.eMetaClass) )

		
		for i in range( 5 ):
			pos = self.getRandPos(self.position, 10)
			INFO_MSG("Create Monster pos: %s, %s, %s"%(pos[0],pos[1],pos[2]))
			KBEngine.createEntity( "Monster", self.spaceID, pos, direction, properties )

		# 创建移动平台对象以及站立在其上的怪物
		pos = self.getRandPos(self.position, 10)
		movePlatform = KBEngine.createEntity( "MovePlatform", self.spaceID, (20.0, 5.0,20.0), direction, {} )
		mon = KBEngine.createEntity( "Monster", self.spaceID, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), properties )
		mon.parent = movePlatform
		mon.localPosition = (1.0, 1.5, 1.2)

	def getRandPos( self, srcPoint, r ):
		"""
		随机位置
		@param srcPoint	:	源位置
		@param range	:	创建圆形范围
		"""
		x = int(( random.random() * r * 2) - r)
		z = int(( random.random() * r * 2) - r)
		return (srcPoint[0] + x, 0.3, srcPoint[2] + z)
	
	def test_createMonster( self, amount, pos, fsmKey ):
		"""
		define method
		测试用刷怪接口
		
		@param amount		:	创建数量
		@param pos			:	entity创建的中心位置
		@param fsmKey		:	monster的AI状态机的key
		"""
		aiFSM = None
		if fsmKey != "":
			aiFSM = g_aiCfgLoader.getEntityAIFsm( fsmKey )
			if not aiFSM:
				ERROR_MSG("fsmKey(%s) error!"%fsmKey)
		
		properties = { "modelID":1, "moveSpeed":1.0 }
		for i in range( amount ):
			position = self.getRandPos(pos, 10)
			entity = KBEngine.createEntity( "Monster", self.spaceID, position, ( 0.0, 0.0, 0.0 ), properties )
			
			if aiFSM:
				entity.aiFSM = aiFSM
				entity.aiState = aiFSM.getDefaultAIState()	#设置初始AI状态
				entity.startAISys()

