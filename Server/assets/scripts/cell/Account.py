# -*- coding: utf-8 -*-
import KBEngine
import GMCommand
from KBEDebug import *
from RoleSkillInterface import RoleSkillInterface
from QuestInterface import QuestInterface
from RoleCombatInterface import RoleCombatInterface
from RoleItemsBagInterface import RoleItemsBagInterface

import json

class Account(KBEngine.Entity, RoleSkillInterface, QuestInterface, RoleCombatInterface, RoleItemsBagInterface):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		RoleSkillInterface.__init__(self)
		QuestInterface.__init__(self)
		RoleCombatInterface.__init__(self)
		RoleItemsBagInterface.__init__(self)
		self.addTimer( 5, 1, 0 )
		self.index = 0
		self.calculateCooldownsOnInit()
		self.calculateBuffsOnInit()
		self.reloadBuff()
		self.attachPassiveSkillOnInit()		#必须在reloadBuff后执行，因为加载被动技能可能会加buff
		self.reloadQuest()
		INFO_MSG("position:", self.position.x, self.position.y, self.position.z)
		#self.moveToPoint( (100,0,0), 10, 2, 0, True, True )
	
	def onDestroy( self ):
		self.detachPassiveSkillOnDestroy()
		self.calculateBuffsOnDestroy()
		self.calculateCooldownsOnDestroy()
	
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		if userArg == 0:
			pass
			self.index = self.index + 1
			if self.index > 250:
				self.index = 0
			self.floatValue = self.index * 0.1
			self.uint8Value = self.index
			self.uint16Value = self.index
			self.uint32Value = self.index
			self.int8Value = self.index
			self.int16Value = self.index
			self.int32Value = self.index
			self.strValue = "str%d"%self.index
			self.vectorValue = (float(self.index), float(self.index), float(self.index))
			self.vector2Value = (float(self.index), float(self.index))
			self.client.onClientEvent(self.index)
			
			d = {"uid":123456789012345678, "id":1234567890, "amount":123,"flag":[11,22,33,44,55],"misc":"test - string"}
			d1 = {"parent":113, "items":[d,]}

			self.client.testFixedDict(d)
			self.client.testFixedDictT1(d1)
			self.client.testOther1(123.456, d, "测试字符串", [111, 112, 113, 114, 115])
			self.client.testJson(json.dumps({1 : 11, "1" : "111", "a" : "a", "t" : ("1", 2, "b"), "l" : [123, "456", "ggg"]}));
			self.client.testForNoParam()
			
		elif userArg == 1:
			ERROR_MSG( "Account::requestTeleport()" )
			cellMailbox2 = KBEngine.globalData["MapManager2"]
			self.teleport(cellMailbox2.cell,self.position,(0.0, 0.0, 0.0))
		
		RoleSkillInterface.onTimer(self, id, userArg)
		QuestInterface.onTimer(self, id, userArg)
		RoleCombatInterface.onTimer(self, id, userArg)
		RoleItemsBagInterface.onTimer(self, id, userArg)
	
	def onCellEvent( self, id, dat ):
		"""
		"""
		self.client.onClientEvent(dat)
		INFO_MSG("onCellEvent:", id, dat)
		
	def onMove( self, controllerID, userData ):
		"""
		onMove
		"""
		INFO_MSG("position:", self.position.x, self.position.y, self.position.z)
		
	def onMoveOver( self, controllerID, userData ):
		"""
		onMoveOver
		"""
		INFO_MSG("onMoveOver", userData)
		#self.moveToPoint( (0,0,0), 10, 2, 0, True, True )
		
		
	def onMoveFailure( self, controllerID, userData ):
		"""
		onMoveFailure
		"""
		INFO_MSG("onMoveFailure", userData)

	def onEnteredAoI( self, entity ):
		"""
		enter
		"""
		INFO_MSG("onEnteredAoI", entity)

	def requestTeleport( self, id ):
		"""
		Exposed method.
		"""
		MetaClass = KBEngine.getSpaceData(self.spaceID, "MetaClass")
		if (MetaClass == "1"):
			cellMailbox = KBEngine.globalData["MapManager2"]
			self.teleport(cellMailbox.cell,self.position,(0.0, 0.0, 0.0))
		elif(MetaClass == "2"):
			cellMailbox = KBEngine.globalData["MapManager"]
			self.teleport(cellMailbox.cell,self.position,(0.0, 0.0, 0.0))

	def requestAddParent( self, id, parentID ):
		"""
		Exposed method
		"""
		if self.parent and self.parent.id == parentID:
			return
		entity = KBEngine.entities.get( parentID, None )
		if entity:
			self.parent = entity

	def requestRemoveParent( self, id, parentID ):
		"""
		Exposed method
		"""
		if not self.parent or self.parent.id != parentID:
			return
		self.parent = None

	def onCellEvent2( self, entityID, testInt, testString, testITEM ):
		"""
		"""
		ERROR_MSG( "Account::onCellEvent2(), entity: %s, int: %s, str: %s, ITEM: %s" % (entityID, testInt, testString, testITEM) )
		print("Account::onCellEvent2(), entity: %s, int: %s, str: %s, ITEM: %s" % (entityID, testInt, testString, testITEM))

	def clientReqGMCommand( self, srcEntityID, dstEntityID, cmd, args ):
		"""
		客户端请求执行gm指令
		<Exposed method>
		"""
		if self.id != srcEntityID:
			return
		GMCommand.executeGMCommand(self, int(dstEntityID), cmd, args)
	
	def testTime( self, srcEntityID ):
		print("receive testTime")
		self.client.testCellTimeCB()
