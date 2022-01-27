# -*- coding: utf-8 -*-

import KBEngine
import Const
import csdefine
import Extra.Extend as Extend
from PlayerAI.Base.AIStateBase import AIStateBase
from Extra.SkillLoader import g_skillLoader

class StateFight(AIStateBase):
	"""
	战斗状态
	有目标就战斗，没目标就随机走动找目标
	"""
	def __init__( self, ai, radius, fightType, skillID ):
		AIStateBase.__init__( self, ai )
		self.findRadius = radius
		self.fightType = fightType
		self.fightTarget = 0
		self.skillID = skillID
		
		skillCfg = g_skillLoader.getSkill( self.skillID )
		self.attackDis = skillCfg.get( "minDis", -1 )
		if self.attackDis < 0:	#技能没有距离要求，就取默认值
			self.attackDis = Const.DEFAULT_ATTACK_DIS
		
		self.findCBID = 0
		self.attackCBID = 0
		self.chaseCBID = 0
	
	def enter( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().registerEvent("Event_onEntityStateChanged", self)
		self.getPlayerEventObj().registerEvent("Event_onEntityLeaveSpace", self)
		self.setTarget()
		self.attackTarget()
		self.chaseTarget()
	
	def leave( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().unregisterEvent("Event_onEntityStateChanged", self)
		self.getPlayerEventObj().unregisterEvent("Event_onEntityLeaveSpace", self)
		
		if self.findCBID:
			KBEngine.cancelCallback( self.findCBID )
			self.findCBID = 0
		
		if self.attackCBID:
			KBEngine.cancelCallback( self.attackCBID )
			self.attackCBID = 0
		
		if self.chaseCBID:
			KBEngine.cancelCallback( self.chaseCBID )
			self.chaseCBID = 0
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		"""
		if name == "Event_onEntityStateChanged":
			self.event_onEntityStateChanged(*argv)
		elif name == "Event_onEntityLeaveSpace":
			self.event_onEntityLeaveSpace(*argv)
	
	#---------------------------------事件响应方法 BEGIN-----------------------------
	def event_onEntityStateChanged( self, entityID, newState, oldState ):
		"""
		entity状态改变
		"""
		if self.fightTarget != entityID:
			return
		if oldState == csdefine.STATE_LIVE and newState == csdefine.STATE_DEAD:		#死亡
			self.fightTarget = 0
	
	def event_onEntityLeaveSpace( self, entityID ):
		"""
		entity离开space
		"""
		if self.fightTarget != entityID:
			return
		self.fightTarget = 0
	
	#---------------------------------事件响应方法 END-----------------------------
	
	def setTarget( self ):
		"""
		设置目标
		"""
		self.findCBID = KBEngine.callback( 3, self.setTarget )
		if not self.fightTarget:
			self.fightTarget = self.__findTarget()
	
	def attackTarget( self ):
		"""
		攻击目标
		"""
		self.attackCBID = KBEngine.callback( 3, self.attackTarget )
		if self.fightTarget:
			entity = self.ai.owner.clientapp.entities.get( self.fightTarget, None )
			if entity and self.ai.owner.position.distTo( entity.position ) <= self.attackDis:
				self.ai.owner.cell.reqUseSkill( self.skillID, self.fightTarget )
	
	def chaseTarget( self ):
		"""
		追逐目标
		"""
		self.attackCBID = KBEngine.callback( 3, self.chaseTarget )
		if self.fightTarget:
			entity = self.ai.owner.clientapp.entities.get( self.fightTarget, None )
			if entity and self.ai.owner.position.distTo( entity.position ) > self.attackDis:
				self.ai.owner.moveToPos( entity.position )
	
	def __findTarget( self ):
		"""
		搜索目标
		"""
		result = None
		minDist = -1
		for e in Extend.entitiesInRange( self.ai.owner, self.findRadius, \
			cnd = lambda entity : True if entity.__class__.__name__ in self.fightType and self.ai.owner.canAttack( entity ) else False ):
			distance = self.ai.owner.position.distTo( e.position )
			if minDist == -1:
				minDist = distance
				result = e.id
				if minDist == 0:
					break

			if distance < minDist:
				minDist = distance
				result = e.id
		
		return result