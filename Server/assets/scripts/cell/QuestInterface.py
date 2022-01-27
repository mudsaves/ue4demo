# -*- coding: utf-8 -*-

import json
import KBEngine
import csdefine
import Functions

from KBEDebug import *
from Quest.Base.QuestLoader import g_questLoader

class QuestInterface:
	"""
	任务接口
	"""
	def __init__( self ):
		pass
	
	def onTimer( self, id, userArg ):
		"""
		"""
		if userArg == csdefine.QUEST_TASK_TIMER:
			for questData in self.questsTable.values():
				tasksDataDict = questData.getTaskData()
				for task in tasksDataDict.values():
					if task.taskTimerID == id:
						task.taskTimerID = 0
						task.onTimeArrive( questData.getQuestID(), self )
	
	def getQuest( self, questID ):
		"""
		获取任务全局实例
		"""
		return g_questLoader.getQuest( questID )
	
	def questHas( self, questID ):
		"""
		玩家身上有某任务
		"""
		return questID in self.questsTable
	
	def questHasSubmit( self, questID ):
		"""
		某任务是否已做过
		"""
		quest = self.getQuest( questID )
		if quest.getPeriodType() == csdefine.QUEST_PERIOD_NOT_LIMIT:
			return False
		
		if quest.getPeriodType() == csdefine.QUEST_PERIOD_ONCE:
			return questID in self.questLogs
		
		if quest.getPeriodType() == csdefine.QUEST_PERIOD_DAY:
			if questID not in self.questLogs:
				return False
			logTime = Functions.getFloatTime( self.questLogs[questID] )
			return not Functions.dayIsOver( logTime )
		
		if quest.getPeriodType() == csdefine.QUEST_PERIOD_WEEK:
			if questID not in self.questLogs:
				return False
			logTime = Functions.getFloatTime( self.questLogs[questID] )
			return not Functions.weekIsOver( logTime )
		
		return False
	
	def queryQuestState( self, questID ):
		"""
		"""
		quest = self.getQuest( questID )
		if not quest:
			ERROR_MSG( "Quest(%s) not found." %questID )
			return csdefine.QUEST_STATE_NOT_ALLOW
		
		if self.questHas( questID ):	#身上有这个任务
			return self.questsTable[questID].queryState()
		else:
			if self.questHasSubmit( questID ):
				return csdefine.QUEST_STATE_HAS_SUBMIT		# 已做过该任务
			
			if quest.checkAcceptable( self ):
				return csdefine.QUEST_STATE_ALLOW			# 可以接但还未接该任务
			else:
				return csdefine.QUEST_STATE_NOT_ALLOW		# 不够条件接该任务
	
	def clientRequestQuest( self, srcEntityID ):
		"""
		Exposed method
		客户端请求初始化任务数据
		"""
		if self.id != srcEntityID:
			return
		for id, data in self.questsTable.items():
			self.client.addQuest( questID, json.dumps(data) )
		self.client.OnQuestInitOver()
	
	def addQuestLog( self, questID ):
		"""
		添加提交记录
		"""
		self.questLogs[ questID ] = Functions.getTime()
	
	def removeQuestLog( self, questID ):
		"""
		移除提交记录
		"""
		self.questLogs.pop( questID, None )
	
	def addQuestData( self, questID, data ):
		"""
		添加任务数据
		"""
		self.questsTable[questID] = data
	
	def removeQuestData( self, questID ):
		"""
		移除任务数据
		"""
		if questID not in self.questsTable:
			return
		self.questsTable.pop( questID )
	
	def onQuestTaskStateChange( self, questID, taskIndex, isComplete, isFail, count ):
		"""
		玩家某任务目标状态改变
		"""
		self.client.updateQuestTaskState( questID, taskIndex, isComplete, isFail, count )
	
	def requestAcceptQuest( self, srcEntityID, questID ):
		"""
		Exposed method
		客户端请求接任务
		"""
		if self.id != srcEntityID:
			return
		self.acceptQuest( questID )
	
	def acceptQuest( self, questID ):
		"""
		接任务
		"""
		quest = self.getQuest( questID )
		if not quest:
			return
		
		state = self.queryQuestState( questID )
		if state != csdefine.QUEST_STATE_ALLOW:
			return
		
		quest.accept( self )
	
	def requestSubmitQuest( self, srcEntityID, questID ):
		"""
		Exposed method
		客户端请求交任务
		"""
		if self.id != srcEntityID:
			return
		self.submitQuest( questID )
	
	def submitQuest( self, questID ):
		"""
		交任务
		"""
		quest = self.getQuest( questID )
		if not quest:
			return
		
		state = self.queryQuestState( questID )
		if state != csdefine.QUEST_STATE_HAS_COMPLETE:
			return
		
		quest.submit( self )
	
	def requestAbandonQuest( self, srcEntityID, questID ):
		"""
		Exposed method
		客户端请求放弃任务
		"""
		if self.id != srcEntityID:
			return
		self.abandonQuest( questID )
	
	def abandonQuest( self, questID ):
		"""
		放弃任务
		"""
		quest = self.getQuest( questID )
		if not quest:
			return
		
		state = self.queryQuestState( questID )
		if state not in [ csdefine.QUEST_STATE_NOT_COMPLETE, csdefine.QUEST_STATE_HAS_COMPLETE ]:
			return
		
		quest = self.getQuest( questID )
		quest.abandon( self )
	
	def reloadQuest( self ):
		"""
		玩家上线后重新往questTaskEventTable加入相应数据
		"""
		for questID, data in self.questsTable.items():
			quest = self.getQuest( questID )
			if quest:
				quest.onReload( self, data )
	
	def addQuestTaskNotify( self, eventType, questID ):
		"""
		注册任务目标事件类型
		"""
		if eventType not in self.questTaskEventTable:
			self.questTaskEventTable[eventType] = [questID]
		else:
			if questID not in self.questTaskEventTable[eventType]:
				self.questTaskEventTable[eventType].append( questID )
	
	def removeQuestTaskNotify( self, eventType, questID ):
		"""
		注销任务目标事件类型
		"""
		if eventType not in self.questTaskEventTable:
			return
		if questID not in self.questTaskEventTable[eventType]:
			return
		self.questTaskEventTable[eventType].remove( questID )
		if not len( self.questTaskEventTable[eventType] ):
			self.questTaskEventTable.pop( eventType )
	
	def addQuestTaskTimer( self, questID, taskIndex, restTime ):
		"""
		添加任务目标倒计时
		"""
		timerID = self.addTimer( restTime, 0, csdefine.QUEST_TASK_TIMER )
		#self.client.addQuestTaskTimer( questID, taskIndex, restTime )
		return timerID
	
	def cancelQuestTaskTimer( self, questID, taskIndex, timerID ):
		"""
		取消任务目标倒计时
		"""
		if timerID > 0:
			self.delTimer( timerID )
		#self.client.cancelQuestTaskTimer( questID, taskIndex )
	
	def triggerQuestEvent( self, eventType, eventParams ):
		"""
		触发任务事件
		"""
		if eventType not in self.questTaskEventTable:
			return
		for questID in self.questTaskEventTable[eventType]:
			questData = self.questsTable[ questID ]
			questData.triggerEvent( self, eventType, eventParams )
	
	#----------------------各种任务事件-----------------
	def questKillMonster( self, scriptID ):
		"""
		杀怪
		"""
		params = { "scriptID": scriptID }
		self.triggerQuestEvent( csdefine.QT_EVENT_KILL, params )
	
	def questItemAmountChange( self, itemID, changeAmount ):
		"""
		物品数量改变
		"""
		params = { "itemID": itemID, "changeAmount": changeAmount }
		self.triggerQuestEvent( csdefine.QT_EVENT_ITEM_AMOUNT_CHANGE, params )
	
	def questOnPlayerDie( self ):
		"""
		玩家死亡
		"""
		params = {}
		self.triggerQuestEvent( csdefine.QT_EVENT_PLAYER_DIE, params )
	
	def questTaskIncreaseState( self, questID, taskIndex, count = 1 ):
		"""
		通知某任务目标计数加N
		"""
		params = { "questID":questID, "taskIndex":taskIndex, "count":count }
		self.triggerQuestEvent( csdefine.QT_EVENT_DIRECT_TRIGGER_TASK, params )