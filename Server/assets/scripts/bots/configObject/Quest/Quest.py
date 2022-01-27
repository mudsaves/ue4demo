# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *
import configObject.Quest.QuestTask as QuestTask

class Quest:
	
	def __init__(self):
		self.id = 0
		self.tasks = {}
		
	def init(self, configData):
		"""
		用本地配置初始化任务数据
		"""
		self.id = configData["id"]
		
		for tData in configData["tasks"]:
			taskIndex = tData["index"]
			task = QuestTask.newInstanceByCls( tData["Script"] )
			task.init( self.id, tData )
			self.tasks[taskIndex] = task
	
	def getID( self ):
		return self.id
	
	def getFirstUnComTask( self ):
		"""
		获取第一个未完成的任务目标
		"""
		for task in self.tasks.values():
			if not task.isComplete():
				return task
		return None
	
	def isComplete(self):
		"""
		"""
		for id, task in self.tasks.items():
			if not task.isComplete():
				return False
		return True
	
	def updateFromServerData( self, questData ):
		"""
		用服务器发来的数据更新本地数据
		"""
		for tData in questData["tasks"]:
			taskIndex = tData["index"]
			if taskIndex in self.tasks:
				self.tasks[taskIndex].updateFromServerData( tData )
	
	def updateTaskState(self, player, taskIndex, isComplete, isFail, count):
		"""
		"""
		self.tasks[taskIndex].updateState(player, isComplete, isFail, count)
	
	def onRemove( self, player ):
		"""
		"""
		for task in self.tasks.values():
			task.onRemove( player )