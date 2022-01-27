# -*- coding: utf-8 -*-

import random
import weakref

import KBEngine
import KBEDebug

import Const
import csdefine
import KST_Config
from PlayerAI.Base.AIStateBase import StateDefine as aiStateDefine

class AIBase:
	"""
	角色AI模式基类
	"""
	_AI_CALSS = {}
	def __init__(self):
		self.owner = None
		self.actionStatus = {}
		self.aistate = -1
		self.hasEnterDefMap = False
	
	@classmethod
	def setClass( SELF, className, classObj ):
		SELF._AI_CALSS[ className ] = classObj
	
	@classmethod
	def getClassObj( SELF, className ):
		if className in SELF._AI_CALSS:
			return SELF._AI_CALSS[ className ]( )
		return None
	
	def getPlayerEventObj( self ):
		return self.owner.eventObj
	
	def attach(self, owner):
		"""
		virtual method
		被附加给角色
		"""
		self.owner = weakref.proxy(owner)
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		事件被触发
		"""
		pass
	
	def changeAIState(self, aistate):
		"""
		改变AI状态
		"""
		if self.aistate == aistate:
			return
		self.actionStatus[self.aistate].leave()
		self.aistate = aistate
		self.actionStatus[self.aistate].enter()
	
	def onSetSpaceData( self ):
		"""
		"""
		currentSpace = self.owner.clientapp.getSpaceData("MappingPath")
		KBEDebug.INFO_MSG("AIBase:onSetSpaceData:[%d]:[%s]" %(self.owner.id, currentSpace))
		
		#还没进入默认地图
		if not self.hasEnterDefMap:
			spaceInfo = Const.DEFUALT_MAP
			if currentSpace != spaceInfo[0]:
				self.owner.GMCommand(self.owner.id, "goto", "{} {}".format(spaceInfo[0], spaceInfo[1]))
			else:
				self.hasEnterDefMap = True
				self.getPlayerEventObj().fireEvent("Event_enterAIDefMap")
	