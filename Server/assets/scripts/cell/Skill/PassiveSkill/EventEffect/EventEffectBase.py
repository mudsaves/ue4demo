# -*- coding: utf-8 -*-

import csdefine

class EventEffectBase:
	"""
	事件效果基类
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
	
	def getLinkEvent( self ):
		"""
		获取效果相关的事件类型
		"""
		return []
	
	def check( self, caster, receiverObj, eventParam ):
		"""
		virtual method.
		检查效果是否能施展
		
		@param caster: 施法者
		@type caster: realEntity
		@param receiverObj: 打包了的受术者，可以是entity或位置
		@type receiverObj: SkillTargetObjEntity 或 SkillTargetObjPosition
		"""
		return True
	
	def receive( self, caster, receiverObj, eventParam ):
		"""
		virtual method.
		执行效果
		
		@param caster: 施法者
		@type caster: realEntity
		@param receiverObj: 打包了的受术者，可以是entity或位置
		@type receiverObj: SkillTargetObjEntity 或 SkillTargetObjPosition
		"""
		pass