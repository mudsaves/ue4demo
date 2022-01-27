# -*- coding: utf-8 -*-

import json
import csdefine
import Functions
import Quest.Base.QuestTask as QuestTask
import Quest.Base.QuestRequirement as QuestRequirement
import Quest.Base.QuestBeforeScript as QuestBeforeScript
import Quest.Base.QuestAfterScript as QuestAfterScript
import Quest.Base.QuestReward as QuestReward
from QuestDataType import QuestDataType

class Quest:
	"""
	任务类
	"""
	def __init__( self ):
		"""
		"""
		self.id = 0
		self.type = csdefine.QUEST_TYPE_NONE
		self.periodType = csdefine.QUEST_PERIOD_NOT_LIMIT
		self.requirements_ = []						# list of QTRequirement; 接任务条件
		self.beforeScript_ = []						# list of QTBeforeScript; 接任务时执行一些脚本
		self.afterScript_ = []						# list of QTAfterScript; 完成任务、放弃任务时执行一些脚本
		self.tasks_ = {}
		self.rewards_ = []
	
	def init( self, dataDict ):
		"""
		"""
		self.id = dataDict["id"]
		self.type = getattr( csdefine, dataDict["type"] )
		self.periodType = getattr( csdefine, dataDict["periodType"] )
		
		for itemDict in dataDict["requirement"]:
			obj = QuestRequirement.newInstance( itemDict["Script"] )
			if not obj:
				continue
			obj.init( itemDict )
			self.requirements_.append( obj )
		
		for itemDict in dataDict["beforeScript"]:
			obj = QuestBeforeScript.newInstance( itemDict["Script"] )
			if not obj:
				continue
			obj.init( itemDict )
			self.beforeScript_.append( obj )
		
		for itemDict in dataDict["afterScript"]:
			obj = QuestAfterScript.newInstance( itemDict["Script"] )
			if not obj:
				continue
			obj.init( itemDict )
			self.afterScript_.append( obj )
		
		for itemDict in dataDict["tasks"]:
			obj = QuestTask.newInstanceByCls( itemDict["Script"] )
			if not obj:
				continue
			obj.init( itemDict )
			self.tasks_[obj.index] = obj
		
		for itemDict in dataDict["rewards"]:
			obj = QuestReward.newInstance( itemDict["Script"] )
			if not obj:
				continue
			obj.init( itemDict )
			self.rewards_.append( obj )
	
	def getType( self ):
		return self.type
	
	def getPeriodType( self ):
		return self.periodType
	
	def checkAcceptable( self, player ):
		"""
		检查是否可接
		"""
		for requirement in self.requirements_:
			if not requirement.query( player ):
				return False
		return True
	
	def newQuestDataObj( self, player ):
		"""
		生成一个任务数据
		"""
		dataObj = QuestDataType()
		dataObj.setQuestID( self.id )
		
		taskDataDict = {}
		for task in self.tasks_.values():
			taskDataObj = task.newTaskDataObj()
			taskDataDict[ taskDataObj.index ] = taskDataObj
			
			taskDataObj.initOnAccept( player )		#接受任务目标时做一些事，比如根据背包内物品数量初始化“收集物品”类任务目标的任务计数、押镖开始时设置押镖标志等
		
		dataObj.setTaskData( taskDataDict )
		return dataObj
	
	def accept( self, player ):
		"""
		接任务
		"""
		for script in self.beforeScript_:
			if not script.query( player ):
				return
		
		for script in self.beforeScript_:
			script.do( player )
		
		data = self.newQuestDataObj( player )
		player.addQuestData( self.id, data )
		
		taskDataList = []
		
		#任务目标时限处理
		tasksDataDict = data.getTaskData()
		for task in tasksDataDict.values():
			taskDataList.append( task.getTaskObjDict() )
			if task.taskTime <= 0:					#没有时间要求
				continue
			if task.isComplete() or task.isFail():	#已成功或已失败
				continue
			task.taskTimerID = player.addQuestTaskTimer( self.id, task.getIndex(), task.taskTime )
			task.taskTime = Functions.getTime( task.taskTime )	#taskTime更正为结束时间（之前是配置里的时长）
		
		self.addTaskNotify( player )
		
		taskStr = json.dumps( {"id":self.id, "tasks":taskDataList} )
		player.client.onAcceptQuest( self.id, taskStr )
	
	def submit( self, player ):
		"""
		交任务
		"""
		for reward in self.rewards_:
			if not reward.check( player ):
				return
		
		for script in self.afterScript_:
			script.onSubmit( player )
		for reward in self.rewards_:
			reward.do( player )
		self.removeTaskNotify( player )
		player.removeQuestData( self.id )
		player.client.onSubmitQuest( self.id )
		if self.getPeriodType() != csdefine.QUEST_PERIOD_NOT_LIMIT:
			player.addQuestLog( self.id )
	
	def abandon( self, player ):
		"""
		放弃任务
		"""
		for script in self.afterScript_:
			script.onAbandon( player )
		self.removeTaskNotify( player )
		
		#取消任务时限倒计时
		for questData in player.questsTable.values():
			tasksDataDict = questData.getTaskData()
			for task in tasksDataDict.values():
				if task.taskTimerID > 0:
					player.delTimer( task.taskTimerID )
					task.taskTimerID = 0
		
		player.removeQuestData( self.id )
		player.client.onAbandonQuest( self.id )
	
	def onReload( self, player, questData ):
		"""
		玩家上线时重载任务
		"""
		#任务目标时限处理
		tasksDataDict = questData.getTaskData()
		for task in tasksDataDict.values():
			if task.taskTime <= 0:
				continue
			if task.isComplete() or task.isFail():
				continue
			if task.taskTime < Functions.getTime():
				task.setFail( self.id, player )
			else:
				restTime = Functions.getFloatTime( task.taskTime - Functions.getTime() )
				task.taskTimerID = player.addQuestTaskTimer( self.id, task.getIndex(), restTime )
		
		self.addTaskNotify( player )		#重新往questTaskEventTable加入相应数据
	
	def addTaskNotify( self, player ):
		"""
		将任务目标事件类型注册到玩家身上
		"""
		for task in self.tasks_.values():
			for eType in task.getEventTypes():
				player.addQuestTaskNotify( eType, self.id )
	
	def removeTaskNotify( self, player ):
		"""
		将任务目标事件类型从玩家身上注销
		"""
		for task in self.tasks_.values():
			for eType in task.getEventTypes():
				player.removeQuestTaskNotify( eType, self.id )
	