# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *
from Skill.Base.EffectBase import EffectBase

class EffectAddBuff( EffectBase ):
	"""
	添加buff
	"""
	def __init__( self ):
		EffectBase.__init__( self )
	
	def init( self, params ):
		self.buffID = int(params["param1"])
	
	def receive( self, caster, receiverObj ):
		"""
		执行效果
		"""
		receiverObj.getObject().addBuffRemote( caster.id, self.buffID )