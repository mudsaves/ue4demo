# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *
from Skill.PassiveSkill.EventEffect.EventEffectBase import EventEffectBase

class EEffectTransDamage( EventEffectBase ):
	"""
	伤害转化为治疗
	"""
	def __init__( self ):
		EventEffectBase.__init__( self )
		self.transRate = 0.0	#转化比例
	
	def init( self, params ):
		self.transRate = float( params["param1"] )
	
	def getLinkEvent( self ):
		"""
		获取效果相关的事件类型
		"""
		return [ csdefine.SKILL_EVENT_RECEIVE_DAMAGE ]
	
	def receive( self, caster, receiverObj, eventParam ):
		"""
		"""
		hp = int( eventParam["damageAmount"] * self.transRate )
		receiverObj.getObject().addHP( hp )
		DEBUG_MSG("Transport damage, casterID:%s, receiverID:%s."%(caster.id, receiverObj.getObject().id))