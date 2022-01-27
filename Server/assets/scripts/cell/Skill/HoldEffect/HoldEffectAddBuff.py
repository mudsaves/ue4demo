# -*- coding: utf-8 -*-

from Skill.Base.HoldEffectBase import HoldEffectBase
from KBEDebug import *

class HoldEffectAddBuff( HoldEffectBase ):
	"""
	添加buff
	"""
	def __init__( self ):
		HoldEffectBase.__init__( self )
	
	def init( self, params ):
		self.buffID = int(params["param1"])
	
	def begin( self, receiver, effectData ):
		"""
		添加效果
		"""
		buffIndex = receiver.addBuff( effectData.casterID, self.buffID )
		if buffIndex != -1:
			effectData.setTempData( "buffIndex", buffIndex )
	
	def end( self, receiver, effectData ):
		"""
		结束效果
		"""
		buffIndex = effectData.getTempData( "buffIndex", -1 )
		if buffIndex != -1:
			receiver.removeBuff( buffIndex )