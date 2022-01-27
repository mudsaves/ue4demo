# -*- coding: utf-8 -*-

import KBEngine
import Extra.Extend as Extend
from PlayerAI.Base.AIStateBase import AIStateBase

class StateRandomMove(AIStateBase):
	"""
	随机走动
	"""
	def __init__( self, ai, radius ):
		AIStateBase.__init__( self, ai )
		self.walkRadius = radius
		self.moveControlID = 0
	
	def enter( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().registerEvent("Event_onMoveOver", self)
		self.getPlayerEventObj().registerEvent("Event_onMoveFailure", self)
		
		pos = self.__randTargetPos()
		self.moveControlID = self.ai.owner.moveToPos( pos )
	
	def leave( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().unregisterEvent("Event_onMoveOver", self)
		self.getPlayerEventObj().unregisterEvent("Event_onMoveFailure", self)
		
		if self.moveControlID:
			self.ai.owner.cancelController(self.moveControlID)
			self.moveControlID = 0
	
	def onEvent(self, name, *argv):
		"""
		virtual method
		"""
		if name == "Event_onMoveOver":
			self.event_onMoveOver(*argv)
		if name == "Event_onMoveFailure":
			self.event_onMoveFailure(*argv)
	
	#---------------------------------事件响应方法 BEGIN-----------------------------
	def event_onMoveOver( self ):
		"""
		移动结束
		"""
		pos = self.__randTargetPos()
		self.moveControlID = self.ai.owner.moveToPos( pos )
	
	def event_onMoveFailure( self ):
		"""
		移动失败
		"""
		pos = self.__randTargetPos()
		self.moveControlID = self.ai.owner.moveToPos( pos )
	
	#---------------------------------事件响应方法 END-----------------------------
	
	def __randTargetPos( self ):
		"""
		随机一个目标点
		"""
		return Extend.getRandomPosInRange( self.ai.owner.position, self.walkRadius )