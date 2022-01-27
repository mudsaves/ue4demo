# -*- coding: utf-8 -*-

import csdefine
from AI.Base.AICfgLoader import g_aiCfgLoader

class AIInterface:
	"""
	AI接口
	"""
	def __init__( self ):
		self.thinkSpeed = 1.0
		self.runningAI = False
		self.aiState = csdefine.AIS_NONE
		self.aiFSM = None
		
		fsmKey = self.getAIFsmKey()
		if fsmKey != "":
			self.aiFSM = g_aiCfgLoader.getEntityAIFsm( fsmKey )
		
		if self.aiFSM:
			self.aiState = self.aiFSM.getDefaultAIState()	#设置初始AI状态
			self.startAISys()
	
	def onTimer( self, id, userArg ):
		"""
		"""
		if id == self.thinkTimerID:
			self.think()
	
	def getAIFsmKey( self ):
		"""
		virtual method
		AI状态机key值
		不同的entity有不同的状态机key值，AI接口子类需要重载此方法，设置entity适配的key值
		"""
		return ""
	
	def addEAI( self, id ):
		"""
		添加EAI
		"""
		if id in self.eAIList:
			return
		self.eAIList.append( id )
	
	def removeEAI( self, id ):
		"""
		移除EAI
		"""
		if id not in self.eAIList:
			return
		self.eAIList.remove( id )
	
	def startAISys( self ):
		"""
		开启AI系统
		"""
		self.runningAI = True
		self.think()
	
	def stopAISys( self ):
		"""
		关闭AI系统，包括关闭think和AI事件响应
		"""
		if self.thinkTimerID:
			self.delTimer( self.thinkTimerID )
			self.thinkTimerID = 0
		
		self.runningAI = False
	
	def think( self ):
		"""
		执行心跳
		"""
		self.aiFSM.onThink( self )
		self.thinkTimerID = self.addTimer( self.thinkSpeed, 0, 0 )
	
	def triggerAIEvent( self, eventType, params ):
		"""
		触发AI事件
		"""
		if not self.runningAI:
			return
		self.aiFSM.onTriggerAIEvent( self, eventType, params )
