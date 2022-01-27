# -*- coding: utf-8 -*-

import KBEngine
import KST_Config
import csdefine

from KBEDebug import *
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.Base.AIStateBase import StateDefine as aiStateDefine

from PlayerAI.AIState.StateWait import StateWait
from PlayerAI.AIState.StateQuest import StateQuest
from PlayerAI.AIState.StateDeadToRevive import StateDeadToRevive

class QuestAI( AIBase ):
	"""
	单一任务AI
	"""
	def __init__(self):
		AIBase.__init__(self)
		self.actionStatus[aiStateDefine.Wait] = StateWait(self)
		
		questID = KST_Config.QuestAI_questID
		isLoop = KST_Config.QuestAI_isLoop
		self.actionStatus[aiStateDefine.Quest] = StateQuest(self, questID, isLoop)
		
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
		self.getPlayerEventObj().registerEvent("Event_onHPChanged", self)
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		事件被触发
		"""
		if name == "Event_enterAIDefMap":
			self.event_onEnterAIDefMap(*argv)
		if name == "Event_onStateChanged":
			self.event_onStateChanged(*argv)
		elif name == "Event_onHPChanged":
			self.event_onHPChanged(*argv)
	
	#---------------------------------事件响应方法 BEGIN-----------------------------
	def event_onEnterAIDefMap( self ):
		"""
		"""
		if self.owner.state == csdefine.STATE_LIVE:
			self.changeAIState(aiStateDefine.Quest)
		else:
			self.changeAIState(aiStateDefine.Dead)
	
	def event_onStateChanged(self, newState, oldState):
		"""
		"""
		if oldState == csdefine.STATE_LIVE and newState == csdefine.STATE_DEAD:		#死亡
			self.changeAIState(aiStateDefine.Dead)
		
		elif oldState == csdefine.STATE_DEAD and newState == csdefine.STATE_LIVE:		#复活
			self.changeAIState(aiStateDefine.Quest)
		
	def event_onHPChanged(self, curHP):
		"""
		"""
		if float(curHP / self.owner.HP_Max) <= 0.5:
			self.owner.GMCommand(self.owner.id, "full")
	
	#---------------------------------事件响应方法 END-----------------------------


AIBase.setClass("QuestAI", QuestAI)