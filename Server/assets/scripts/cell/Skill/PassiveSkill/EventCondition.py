# -*- coding: utf-8 -*-

import csdefine

class EventConditionBase:
	"""
	事件条件基类
	"""
	def __init__( self ):
		pass
	
	def init( self, configData ):
		"""
		"""
		pass
	
	def getLinkEvent( self ):
		"""
		获取条件相关的事件类型
		"""
		return []
	
	def check( self, caster, target, eventParams ):
		"""
		"""
		return False

class DamageAmount( EventConditionBase ):
	"""
	伤害量满足条件
	"""
	def __init__( self ):
		self.operation = 0
		self.damage = 0
	
	def init( self, configData ):
		"""
		"""
		self.operation = int(configData["param1"])
		self.damage = int(configData["param2"])
	
	def getLinkEvent( self ):
		"""
		获取条件相关的事件类型
		"""
		return [ csdefine.SKILL_EVENT_RECEIVE_DAMAGE ]
	
	def check( self, caster, target, eventParams ):
		"""
		"""
		if self.operation == 1:
			return eventParams["damageAmount"] >= self.damage
		elif self.operation == 2:
			return eventParams["damageAmount"] <= self.damage
		elif self.operation == 3:
			return eventParams["damageAmount"] > self.damage
		elif self.operation == 4:
			return eventParams["damageAmount"] < self.damage
		elif self.operation == 5:
			return eventParams["damageAmount"] == self.damage
		return False

class NewStateCheck( EventConditionBase ):
	"""
	新状态是某状态
	"""
	def __init__( self ):
		self.state = 0
	
	def init( self, configData ):
		"""
		"""
		self.state = getattr(csdefine, configData["param1"])
	
	def getLinkEvent( self ):
		"""
		获取条件相关的事件类型
		"""
		return [ csdefine.SKILL_EVENT_STATE_CHANGE ]
	
	def check( self, caster, target, eventParams ):
		"""
		"""
		return eventParams["newState"] == self.state

g_objects = {	"DamageAmount": DamageAmount,
				"NewStateCheck": NewStateCheck,
			}

def newInstance( clsName ):
	return g_objects.get( clsName )()