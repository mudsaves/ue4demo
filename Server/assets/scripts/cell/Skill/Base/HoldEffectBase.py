# -*- coding: utf-8 -*-

from HoldEffectDataType import HoldEffectDataType

class HoldEffectBase:
	"""
	持有效果基类
	"""
	def __init__( self ):
		self.sourceType = 0
	
	def init( self, params ):
		pass
	
	def setSourceType( self, type ):
		"""
		设置效果来源
		"""
		self.sourceType = type
	
	def setSourceParam( self, param ):
		"""
		设置来源参数：如果是技能参数是技能ID，如果是buff参数是buffID
		"""
		self.sourceParam = param
	
	def check( self, caster, receiver ):
		"""
		virtual method.
		检查效果是否能施展
		
		@param caster: 施法者
		@type caster: realEntity
		@param receiver: 受术者
		@type receiver: entity
		"""
		return True
	
	def newHoldEffectData( self, caster, receiver ):
		"""
		返回一个效果数据
		
		@param caster: 施法者
		@type caster: entity
		@param receiver: 受术者
		@type receiver: realEntity
		"""
		return HoldEffectDataType()
	
	def begin( self, receiver, effectData ):
		"""
		virtual method.
		添加效果
		
		@param receiver: 受术者
		@type receiver: realEntity
		@param effectData: 效果数据
		@type effectData: HoldEffectDataType
		"""
		pass
	
	def end( self, receiver, effectData ):
		"""
		virtual method.
		结束效果
		
		@param receiver: 受术者
		@type receiver: realEntity
		@param effectData: 效果数据
		@type effectData: HoldEffectDataType
		"""
		pass
