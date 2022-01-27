# -*- coding: utf-8 -*-

from AI.Base.AIData import AIData

class AIStateBase:
	"""
	AI状态基类
	"""
	def __init__( self, state ):
		self.state = state		#记录一下对应的枚举值
		self.aiList = []
	
	def init( self, cfgData ):
		"""
		"""
		for aiDict in cfgData:
			_aiInstance = AIData()
			_aiInstance.init( aiDict )
			self.aiList.append( _aiInstance )
	
	def onThink( self, entity ):
		"""
		AI心跳到达
		"""
		for aiIns in self.aiList:
			if entity.aiState != self.state:	#entity ai状态发生了变化
				break
			if aiIns.getID() in entity.eAIList:
				continue
			aiIns.do( entity )
	
	def onEnter( self, entity ):
		"""
		virtual method
		进入此状态
		注：只有切换状态时会执行此接口
		"""
		pass
	
	def onLeave( self, entity ):
		"""
		virtual method
		离开此状态
		注：只有切换状态时会执行此接口
		"""
		pass