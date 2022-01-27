# -*- coding: utf-8 -*-

import KBEngine
from PlayerAI.Base.AIStateBase import AIStateBase

class StateQuest( AIStateBase ):
	"""
	做某个任务
	"""
	def __init__( self, ai, questID, isLoop ):
		AIStateBase.__init__( self, ai )
		self.cfgQuestID = questID	#任务ID
		self.cfgIsLoop = isLoop		#是否重复做任务
		self.firstStart = True
		self.lastSubmitQuest = 0
		self.startCBID = 0
		self.processCBID = 0
	
	def enter( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().registerEvent( "Event_onSubmitQuest", self )
		
		if not self.ai.owner.hasInitQuest:
			self.startCBID = KBEngine.callback( 3, self.start )
		else:
			self.start()
	
	def leave( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().unregisterEvent( "Event_onSubmitQuest", self )
		
		if self.startCBID:
			KBEngine.cancelCallback( self.startCBID )
			self.startCBID = 0
		
		if self.processCBID:
			KBEngine.cancelCallback( self.processCBID )
			self.processCBID = 0
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		"""
		if name == "Event_onSubmitQuest":
			self.event_onSubmitQuest(*argv)
	
	#---------------------------------事件响应方法 BEGIN-----------------------------
	def event_onSubmitQuest( self, questID ):
		"""
		"""
		if questID != self.lastSubmitQuest:
			self.lastSubmitQuest = questID
	
	#---------------------------------事件响应方法 END-----------------------------
	
	def start( self ):
		"""
		开始
		"""
		if self.firstStart:		#是首次进入此状态
			self.firstStart = False
			self.ai.owner.abanonAllQuest()
			self.processCBID = KBEngine.callback( 3, self.process )
		else:
			self.process()
	
	def process( self ):
		"""
		循环执行此方法
		"""
		self.processCBID = KBEngine.callback( 5, self.process )
		quest = self.ai.owner.getOneQuest()
		if quest:
			if quest.isComplete():
				self.ai.owner.cell.requestSubmitQuest( quest.getID() )
			else:
				task = quest.getFirstUnComTask()
				task.tryDo( self.ai.owner )
		else:
			questID = self.getNextQuest()
			if questID:
				self.ai.owner.GMCommand( self.ai.owner.id, "remove_completed_quest", str(questID) )
				self.ai.owner.cell.requestAcceptQuest( questID )
	
	def getNextQuest( self ):
		"""
		"""
		if self.lastSubmitQuest == 0:
			return self.cfgQuestID
		
		elif self.cfgQuestID != self.lastSubmitQuest:
			return self.cfgQuestID
		
		elif self.cfgIsLoop:
			return self.cfgQuestID
		
		else:
			return 0