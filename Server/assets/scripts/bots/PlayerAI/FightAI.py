# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import KST_Config

from PlayerAI.Base.AIBase import AIBase
from PlayerAI.Base.AIStateBase import StateDefine as aiStateDefine

from PlayerAI.AIState.StateWait import StateWait
from PlayerAI.AIState.StateFight import StateFight
from PlayerAI.AIState.StateRandomMove import StateRandomMove
from PlayerAI.AIState.StateDeadToRevive import StateDeadToRevive

class FightAIBase( AIBase ):
	"""
	战斗模式AI基类
	"""
	def __init__( self ):
		AIBase.__init__( self )
		
		self.actionStatus[aiStateDefine.Wait] = StateWait(self)
		self.actionStatus[aiStateDefine.RandMove] = StateRandomMove(self, self.getFightRadius())
		self.actionStatus[aiStateDefine.Fight] = StateFight(self, self.getFightRadius(), self.getTargetType(), self.getSkillID())
		self.actionStatus[aiStateDefine.Dead] = StateDeadToRevive(self)
		self.aistate = aiStateDefine.Wait
		
		self.startCBID = 0
	
	def getTargetType( self ):
		"""
		virtual method
		获取战斗对象类型
		"""
		return []
	
	def getFightRadius( self ):
		"""
		获取战斗半径
		virtual method
		"""
		return 0
	
	def getSkillID( self ):
		"""
		获取战斗半径
		virtual method
		"""
		return 0
	
	def attach(self, owner):
		"""
		virtual method
		被附加给角色
		"""
		AIBase.attach(self, owner)
		self.getPlayerEventObj().registerEvent("Event_enterAIDefMap", self)
		self.getPlayerEventObj().registerEvent("Event_onStateChanged", self)
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		事件被触发
		"""
		if name == "Event_enterAIDefMap":
			self.event_onEnterAIDefMap(*argv)
		elif name == "Event_onStateChanged":
			self.event_onStateChanged(*argv)
	
	#---------------------------------事件响应方法 BEGIN-----------------------------
	def event_onEnterAIDefMap( self ):
		"""
		"""
		if self.owner.state == csdefine.STATE_LIVE:
			self.changeAIState(aiStateDefine.RandMove)
		else:
			self.changeAIState(aiStateDefine.Dead)
		
		self.startCBID = KBEngine.callback( 10, self.start )	#10秒后进入战斗
	
	def event_onStateChanged(self, newState, oldState):
		"""
		"""
		if oldState == csdefine.STATE_LIVE and newState == csdefine.STATE_DEAD:		#死亡
			self.changeAIState(aiStateDefine.Dead)
		
		elif oldState == csdefine.STATE_DEAD and newState == csdefine.STATE_LIVE:		#复活
			if self.startCBID > 0:		# 还在准备
				self.changeAIState(aiStateDefine.RandMove)
			else:
				self.changeAIState(aiStateDefine.Fight)
	
	#---------------------------------事件响应方法 END-----------------------------
	
	def start( self ):
		"""
		"""
		self.startCBID = 0
		if self.owner.state == csdefine.STATE_LIVE:
			self.changeAIState(aiStateDefine.Fight)

class FightRoleAI(FightAIBase):
	"""
	与玩家战斗
	"""
	def __init__(self):
		FightAIBase.__init__(self)
	
	def getTargetType( self ):
		"""
		virtual method
		"""
		return ["Account"]
	
	def getFightRadius( self ):
		"""
		virtual method
		"""
		return KST_Config.FightRoleAI_radius
	
	def getSkillID( self ):
		"""
		获取战斗半径
		virtual method
		"""
		return KST_Config.FightRoleAI_skill

class FightMonsterAI(FightAIBase):
	"""
	与怪物战斗
	"""
	def __init__(self):
		FightAIBase.__init__(self)
	
	def getTargetType( self ):
		"""
		virtual method
		"""
		return ["Monster"]
	
	def getFightRadius( self ):
		"""
		virtual method
		"""
		return KST_Config.FightMonsterAI_radius
	
	def getSkillID( self ):
		"""
		获取战斗半径
		virtual method
		"""
		return KST_Config.FightMonsterAI_skill


AIBase.setClass("FightRoleAI", FightRoleAI)
AIBase.setClass("FightMonsterAI", FightMonsterAI)
