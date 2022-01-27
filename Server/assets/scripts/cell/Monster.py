# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import random
import time
import copy
from SkillInterface import SkillInterface
from MonsterCombatInterface import MonsterCombatInterface
from MonsterAIInterface import MonsterAIInterface

class Monster(KBEngine.Entity, SkillInterface, MonsterCombatInterface, MonsterAIInterface):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		SkillInterface.__init__(self)
		MonsterCombatInterface.__init__(self)
		MonsterAIInterface.__init__(self)
		self.srcPosition = copy.copy(self.position)
		self.moveSpeed = 2.0
		self.continueMove = True
		self.moveByNavigate = True # 子对象移动时这个值应该设为False

		self.cloneTimerID = 0
		self.destroyPeriod = 0
		
		self.navPaths = []
		self.navParams = ()

		self.addTimer( 2, 0, 120 )
		
		if self.controllerByID != 0:
			self.addTimer( 3, 0, 130 )
	
	def getRandPos( self, srcPoint, r ):
		"""
		随机位置
		@param srcPoint	:	源位置
		@param range	:	创建圆形范围
		"""
		x = random.random() * r * 2 - r
		z = random.random() * r * 2 - r
		return (srcPoint[0] + x, srcPoint[1], srcPoint[2] + z)
	
	def randMove(self):
		"""
		移动到新的点
		"""
		#INFO_MSG("randMove!")
		if self.parent:
			dest = self.getRandPos(self.srcPosition, 5)
		else:
			dest = self.getRandPos(self.srcPosition, 10)
		
		if self.parent:
			return self.navigateEx(dest, self.moveSpeed, 0.0, 0xffff, 0xffff, True, 0, 0xffff)
		elif self.moveByNavigate:
			return self.navigate(dest, self.moveSpeed, 0.0, 0xffff, 0xffff, True, 0, 0xffff, 0)
		else:
			return self.moveToPoint(dest, self.moveSpeed, 0.0, 0, True, True)
	
	def onMoveOver( self, controllerID, userData ):
		"""
		移动结束
		移动到新的点
		"""
		if userData == 1314:
			if self.navPaths:
				dest = self.navPaths.pop(0)
				self.moveToPoint(dest, *self.navParams)
				return

		if self.continueMove:
			self.randMove()
		
	def onMoveFailure( self, controllerID, userData ):
		"""
		移动失败
		移动到新的点
		"""
		if userData == 1314:
			return
			
		if self.continueMove:
			self.randMove()

	def clone(self, randSpawnRange = 0.0):
		"""
		复制一个自己
		"""
		pos = self.getRandPos(self.position, randSpawnRange)
		return KBEngine.createEntity( self.__class__.__name__, self.spaceID, pos, self.direction, self.__dict__ )

	def cloneAndDestroy(self, createPeriod = 1.0, destroyPeriod = 1.1):
		"""
		"""
		self.destroyPeriod = destroyPeriod
		if self.cloneTimerID > 0:
			self.delTimer(self.cloneTimerID)
		self.cloneTimerID = self.addTimer(createPeriod, createPeriod, 110)

	def setControllerByOnInit( self ):
		"""
		根据初始化时传入的controllerByID设置控制者
		"""
		if self.controllerByID == 0:
			return
		e = KBEngine.entities.get( self.controllerByID, None )
		if e:
			self.controlledBy = e.base

	def onTimer(self, timerID, userData):
		"""
		"""
		if userData == 110:
			ent = self.clone( 3.0 )
			if self.destroyPeriod > 0:
				ent.addTimer( self.destroyPeriod, 0.0, 111 )
		elif userData == 111:
			self.destroy()
		elif userData == 120:
			self.randMove()
		elif userData == 130:
			self.setControllerByOnInit()
		
		SkillInterface.onTimer( self, timerID, userData )
		MonsterCombatInterface.onTimer( self, timerID, userData )
		MonsterAIInterface.onTimer( self, timerID, userData )
	
	def addTrap(self, radius = 10):
		"""
		"""
		return self.addProximity(radius, radius, 0)
		
	def onEnterTrap( self, entityEntering, rangeXZ, rangeY, controllerID, userArg ):
		"""
		"""
		DEBUG_MSG("%s(%s): entity  %s(%s) entered my trap。 controllerID = %s" % (self.__class__.__name__, self.id, entityEntering.__class__.__name__, entityEntering.id, controllerID))
		self.cancelController(controllerID)


	def onLeaveTrap( self, entityLeaving, rangeXZ, rangeY, controllerID, userArg ):
		"""
		"""
		DEBUG_MSG("%s(%s): entity %s(%s) left my trap。 controllerID = %s" % (self.__class__.__name__, self.id, entityLeaving__class__.__name__, entityLeaving.id, controllerID))

	def navigateEx(self, localDest, velocity, distance, maxMoveDistance, maxSearchDistance, faceMovement, layer, flags):
		"""
		"""
		self.navPaths = KBEngine.navigatePathPoints( "spaces/nav_test", self.localPosition, localDest, maxSearchDistance, layer, flags )
		self.navParams = (velocity, distance, 1314, faceMovement, True)
		if not self.navPaths:
			return False
		
		dest = self.navPaths.pop(0)
		self.moveToPoint(dest, *self.navParams)
		return True

	def onWitnessed(self, isWitnessed):
		DEBUG_MSG("Monster::onWitnessed(isWitnessed)");
		#self.allClients.testJson(json.dumps({1 : 11, "1" : "111", "a" : "a", "t" : ("1", 2, "b"), "l" : [123, "456", "ggg"]}));

	def onEnteredAoI(self, entity):
		DEBUG_MSG("onEnteredAoI:%i.", entity.id);