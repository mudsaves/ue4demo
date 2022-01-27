# -*- coding: utf-8 -*-

import time, random
import KBEngine
from KBEDebug import *
from Extra.KSTEvent import KSTEvent
from interface.CombatInterface import CombatInterface

class Monster(
	KBEngine.Entity,
	CombatInterface
	):
	def __init__(self):
		"""
		"""
		KBEngine.Entity.__init__(self)
		CombatInterface.__init__(self)
		self.eventObj = KSTEvent()
	
	def onLeaveSpace( self ):
		"""
		"""
		player = self.clientapp.player()
		if player:
			player.eventObj.fireEvent("Event_onEntityLeaveSpace", self.id)
	
	def onControlled( self, isControlled ):
		"""
		KBEngine回调
		被控制或失去控制
		"""
		player = self.clientapp.player()
		if player:
			if isControlled:
				player.addControlledEntity( self )
			else:
				player.removeControlledEntity( self )
	
	def moveToPos(self, pos):
		"""
		"""
		return self.moveToPoint( pos, self.moveSpeed, 0.0, 0, True, True )