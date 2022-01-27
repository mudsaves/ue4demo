# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import KST_Config
import Extra.Extend as Extend

from PlayerAI.Base.AIBase import AIBase
from PlayerAI.Base.AIStateBase import StateDefine as aiStateDefine

from PlayerAI.AIState.StateWait import StateWait
from PlayerAI.AIState.StateRandomMove import StateRandomMove
from PlayerAI.AIState.StateDeadToRevive import StateDeadToRevive

class ContrlMonsterMoveAI( AIBase ):
	"""
	控制一堆怪物跟随自己移动
	"""
	def __init__( self ):
		AIBase.__init__( self )
		
		self.actionStatus[aiStateDefine.Wait] = StateWait(self)
		self.actionStatus[aiStateDefine.RandMove] = StateRandomMove(self, KST_Config.ContrlMonsterMoveAI_radius)
		self.actionStatus[aiStateDefine.Dead] = StateDeadToRevive(self)
		self.aistate = aiStateDefine.Wait
	
	def attach(self, owner):
		"""
		virtual method
		被附加给角色
		"""
		AIBase.attach(self, owner)
		self.getPlayerEventObj().registerEvent("Event_enterAIDefMap", self)
		self.getPlayerEventObj().registerEvent("Event_onStateChanged", self)
		self.getPlayerEventObj().registerEvent("Event_onMoveOver", self)
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		事件被触发
		"""
		if name == "Event_enterAIDefMap":
			self.event_onEnterAIDefMap(*argv)
		elif name == "Event_onStateChanged":
			self.event_onStateChanged(*argv)
		elif name == "Event_onMoveOver":
			self.event_onMoveOver(*argv)
	
	#---------------------------------事件响应方法 BEGIN-----------------------------
	def event_onEnterAIDefMap( self ):
		"""
		"""
		KBEngine.callback( 3, self.start )
	
	def event_onStateChanged(self, newState, oldState):
		"""
		"""
		if oldState == csdefine.STATE_LIVE and newState == csdefine.STATE_DEAD:		#死亡
			self.changeAIState(aiStateDefine.Dead)
		
		elif oldState == csdefine.STATE_DEAD and newState == csdefine.STATE_LIVE:		#复活
			self.changeAIState(aiStateDefine.RandMove)
	
	def event_onMoveOver( self ):
		"""
		"""
		#被我控制的entity跟着我跑
		for e in self.owner.controlledEntities:
			if self.owner.spaceID != e.spaceID:
				continue
			pos = Extend.getRandomPosInRange( self.owner.position, 1 )
			e.moveToPos( pos )
	
	#---------------------------------事件响应方法 END-----------------------------
	
	def start( self ):
		"""
		"""
		self.owner.GMCommand( self.owner.id, "clone_controlled_monster", "{}".format(KST_Config.ContrlMonsterMoveAI_amount) )
		
		if self.owner.state == csdefine.STATE_LIVE:
			self.changeAIState(aiStateDefine.RandMove)
		else:
			self.changeAIState(aiStateDefine.Dead)

AIBase.setClass("ContrlMonsterMoveAI", ContrlMonsterMoveAI)