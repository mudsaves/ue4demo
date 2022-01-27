# -*- coding: utf-8 -*-

import time
import copy
import json
import csdefine

from KBEDebug import *
from configObject.Quest import Quest
from Extra.QuestLoader import g_quests

class QuestInterface:
	
	def __init__(self):
		self.questTable={}
		self.hasInitQuest = False
	
	def getQuest( self, questID ):
		"""
		"""
		return self.questTable.get(questID, None)
	
	def getOneQuest( self ):
		"""
		获取身上的一个任务
		"""
		if len(self.questTable) == 0:
			return None
		return list( self.questTable.values() )[0]
	
	def __addQuestData( self, questID, quest ):
		"""
		添加任务数据
		"""
		self.questTable[ questID ] =  quest
	
	def __removeQuestData( self, questID ):
		"""
		移除任务数据
		"""
		if questID not in self.questTable:
			return
		self.questTable[questID].onRemove( self )
		self.questTable.pop( questID )
	
	def abanonAllQuest( self ):
		"""
		放弃所有任务
		"""
		for id, q in self.questTable.items():
			self.cell.requestAbandonQuest( id )
	
	def requestInitQuest(self):
		"""
		向服务器请求任务数据
		"""
		self.cell.clientRequestQuest()
	
	def addQuest(self, questID, dataStream):
		"""
		define method
		clientRequestQuest 回调
		"""
		questCfg = g_quests.getQuest( questID )
		if not questCfg:
			ERROR_MSG("Quest not exist! id:%s"%questID)
			return
		
		quest = Quest.Quest()
		quest.init( questCfg )
		questData = json.loads(dataStream)
		quest.updateFromServerData( questData )
		self.__addQuestData( questID, quest )
	
	def OnQuestInitOver(self):
		"""
		define method
		任务数据接收完毕
		"""
		self.hasInitQuest = True
	
	def onAcceptQuest(self, questID, dataStream):
		"""
		define method
		接任务
		"""
		questCfg = g_quests.getQuest( questID )
		if not questCfg:
			ERROR_MSG("Quest not exist! id:%s"%questID)
			return
		
		quest = Quest.Quest()
		quest.init( questCfg )
		questData = json.loads( dataStream )
		quest.updateFromServerData( questData )
		self.__addQuestData( questID, quest )

	def onSubmitQuest( self, questID ):
		"""
		define method
		交任务
		"""
		if questID in self.questTable:
			self.__removeQuestData( questID )
		self.eventObj.fireEvent( "Event_onSubmitQuest", questID )
		
	def onAbandonQuest( self, questID ):
		"""
		define method
		放弃任务
		"""
		if questID in copy.copy( self.questTable ):
			self.__removeQuestData( questID )
	
	def updateQuestTaskState( self, questID, taskIndex, isComplete, isFail, count ):
		"""
		define method
		任务目标状态改变
		"""
		if questID not in self.questTable:
			ERROR_MSG("not found quest[%d]" %(questID))
			return
		
		self.questTable[questID].updateTaskState(self, taskIndex, isComplete, isFail, count)
