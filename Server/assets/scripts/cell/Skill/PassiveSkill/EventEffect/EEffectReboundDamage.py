# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *
from Skill.PassiveSkill.EventEffect.EventEffectBase import EventEffectBase

class EEffectReboundDamage( EventEffectBase ):
	"""
	反弹伤害
	"""
	def __init__( self ):
		EventEffectBase.__init__( self )
		self.reboundRate = 0.0	#反弹比例
	
	def init( self, params ):
		self.reboundRate = float( params["param1"] )
	
	def getLinkEvent( self ):
		"""
		获取效果相关的事件类型
		"""
		return [ csdefine.SKILL_EVENT_RECEIVE_DAMAGE ]
	
	def receive( self, caster, receiverObj, eventParam ):
		"""
		"""
		damage = int( eventParam["damageAmount"] * self.reboundRate )
		receiverObj.getObject().receiveDamageBySkill( damage, True, self.sourceParam, caster )
		DEBUG_MSG("Rebound damage, casterID:%s, receiverID:%s."%(caster.id, receiverObj.getObject().id))