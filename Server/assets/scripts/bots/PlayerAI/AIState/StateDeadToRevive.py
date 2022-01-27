# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from PlayerAI.Base.AIStateBase import AIStateBase

REVIVE_DELAY_TIME = 3

class StateDeadToRevive( AIStateBase ):
	"""
	死亡然后复活
	"""
	def __init__( self, ai ):
		AIStateBase.__init__( self, ai )
		self.reviveCBID = 0
	
	def enter( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().registerEvent( "Event_onStateChanged", self )
		self.reviveCBID = KBEngine.callback( REVIVE_DELAY_TIME, self.revive )
	
	def leave( self ):
		"""
		virtual method
		"""
		self.getPlayerEventObj().unregisterEvent( "Event_onStateChanged", self )
		
		# 离开之前，对自身进行复活(主动离开的话，应该是进入到新的地图中去了)
		if self.ai.owner.state == csdefine.STATE_DEAD:
			self.ai.owner.GMCommand( self.ai.owner.id, "revive" )
		
		if self.reviveCBID > 0:
			KBEngine.cancelCallback( self.reviveCBID )
			self.reviveCBID = 0
	
	def onEvent( self, name, *argv ):
		"""
		virtual method
		"""
		if name == "Event_onStateChanged":
			self.event_onStateChanged(*argv)
	
	#---------------------------------事件响应方法 BEGIN-----------------------------
	def event_onStateChanged( self, newState, oldState ):
		"""
		"""
		if oldState == csdefine.STATE_LIVE and newState == csdefine.STATE_DEAD:		#死亡
			if self.reviveCBID > 0:
				KBEngine.cancelCallback( self.reviveCBID )
			self.reviveCBID = KBEngine.callback( REVIVE_DELAY_TIME, self.revive )
		
		elif oldState == csdefine.STATE_DEAD and newState == csdefine.STATE_LIVE:		#复活
			if self.reviveCBID > 0:
				KBEngine.cancelCallback( self.reviveCBID )
				self.reviveCBID = 0
	
	#---------------------------------事件响应方法 END-----------------------------

	def revive( self ):
		"""
		"""
		self.reviveCBID = 0
		self.ai.owner.GMCommand( self.ai.owner.id, "revive" )