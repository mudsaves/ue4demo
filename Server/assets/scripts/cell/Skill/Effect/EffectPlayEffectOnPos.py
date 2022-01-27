# -*- coding: utf-8 -*-

from KBEDebug import *
from Skill.Base.EffectBase import EffectBase

class EffectPlayEffectOnPos( EffectBase ):
	"""
	在目标位置放光效
	"""
	def __init__( self ):
		EffectBase.__init__( self )
	
	def init( self, params ):
		self.effectID = params["param1"]
	
	def receive( self, caster, receiverObj ):
		"""
		执行效果
		"""
		DEBUG_MSG("EffectPlayEffectOnPos receive. caster(%s), receiver(%s), effectID(%s)."%(caster.id,receiverObj.getObjectPosition(), self.effectID))