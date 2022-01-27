# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *
from AI.Base.AIData import AIData

class AIFsmBase:
	"""
	AI状态机基类
	"""
	STATE_MAPPING = {}
	
	def __init__( self, fsmKey ):
		self.fsmKey = fsmKey
		self._eventAI = {}		#事件AI，{eventType: [AIData1, AIData2,... ]}
		self._stateList = {}	#状态, {state1: AIState1, state2: AIState2}
	
	def init( self, cfgData ):
		"""
		"""
		for typeStr, aiDictList in cfgData["eventAI"].items():
			if not hasattr( csdefine, typeStr ):
				ERROR_MSG("AI event type not exist, [%s]."%typeStr)
				continue
			
			eventType = getattr( csdefine, typeStr )
			self._eventAI[ eventType ] = []
			for aiDict in aiDictList:
				_aiInstance = AIData()
				_aiInstance.init( aiDict )
				self._eventAI[ eventType ].append( _aiInstance )
		
		for state, stateCls in self.STATE_MAPPING.items():
			_stateInstance = stateCls( state )
			self._stateList[ state ] = _stateInstance
		
		for stateStr, aiDictList in cfgData["AIState"].items():
			if not hasattr( csdefine, stateStr ):
				ERROR_MSG("AI state not exist, [%s]."%stateStr)
				continue
			
			state = getattr( csdefine, stateStr )
			if state not in self.STATE_MAPPING:
				ERROR_MSG("AI state not not in FSM, [%s]."%stateStr)
				continue
			
			self._stateList[ state ].init( aiDictList )
	
	def getDefaultAIState( self ):
		"""
		virtual method
		获取默认AI状态
		"""
		return csdefine.AIS_NONE
	
	def changeAIState( self, entity, newState ):
		"""
		切换AI状态
		"""
		if entity.aiState == newState:
			return
		self._stateList[ entity.aiState ].onLeave( entity )
		entity.aiState = newState
		self._stateList[ entity.aiState ].onEnter( entity )
	
	def onThink( self, entity ):
		"""
		AI心跳到达
		"""
		self._stateList[ entity.aiState ].onThink( entity )
	
	def onTriggerAIEvent( self, entity, eventType, params ):
		"""
		某AI事件被触发
		"""
		for aiInstance in self._eventAI.get( eventType, [] ):
			aiInstance.do( entity )
		
		if eventType not in self.getRelativeAIEvent():
			return
		newState = self.getNewAIState( entity, eventType, params )
		if newState != csdefine.AIS_NONE:
			self.changeAIState( entity, newState )
	
	def getRelativeAIEvent( self ):
		"""
		virtual method
		获取会触发状态切换的AI事件
		为了提高效率，只有发生此列表中的事件时，才检测是否切换状态
		"""
		return []
	
	def getNewAIState( self, entity, eventType, params ):
		"""
		virtual method
		根据被触发的AI事件获取新的AI状态
		"""
		return csdefine.AIS_NONE