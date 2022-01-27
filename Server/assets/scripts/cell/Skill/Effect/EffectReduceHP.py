# -*- coding: utf-8 -*-

import csdefine
from Skill.Base.EffectBase import EffectBase

class EffectReduceHP( EffectBase ):
	"""
	减HP
	"""
	def __init__( self ):
		EffectBase.__init__( self )
		self.hp = 0
	
	def init( self, params ):
		self.hp = int(params["param1"])
	
	def receive( self, caster, receiverObj ):
		"""
		"""
		if self.sourceType == csdefine.EFFECT_SOURCE_SKILL:
			receiverObj.getObject().receiveDamageBySkill( self.hp, True, self.sourceParam, caster )
		elif self.sourceType == csdefine.EFFECT_SOURCE_BUFF:
			receiverObj.getObject().receiveDamageByBuff( self.hp, True, self.sourceParam )