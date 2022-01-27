# -*- coding: utf-8 -*-

import csdefine
import KBEngine

class CombatInterface:
	"""
	"""
	def set_state( self, oldState ):
		"""
		state属性被改变
		"""
		player = self.clientapp.player()
		if player:
			if player.id == self.id:
				self.eventObj.fireEvent( "Event_onStateChanged", self.state, oldState )
			else:
				player.eventObj.fireEvent( "Event_onEntityStateChanged", self.id, self.state, oldState )

	def canAttack( self, target ):
		"""
		是否可攻击
		"""
		if self.id == target.id:
			return False
		if self.spaceID != target.spaceID:
			return False
		if not hasattr( target, "state" ):
			return False
		if target.state == csdefine.STATE_DEAD:
			return False
		return True