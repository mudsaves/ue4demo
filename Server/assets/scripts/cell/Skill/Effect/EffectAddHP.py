# -*- coding: utf-8 -*-

import csdefine
from Skill.Base.EffectBase import EffectBase

class EffectAddHP( EffectBase ):
	"""
	加HP
	"""
	def __init__( self ):
		EffectBase.__init__( self )
		self.hp = 0
	
	def init( self, params ):
		self.hp = int(params["param1"])
	
	def receive( self, caster, receiverObj ):
		"""
		"""
		receiverObj.getObject().addHP( self.hp )