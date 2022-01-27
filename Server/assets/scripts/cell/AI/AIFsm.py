# -*- coding: utf-8 -*-

import csdefine
import AI.AIState as AIState
from AI.Base.AIFsmBase import AIFsmBase

class AIFsm_Monster( AIFsmBase ):
	"""
	普通怪物AI状态机
	"""
	STATE_MAPPING = {	csdefine.AIS_MONSTER_FREE: AIState.AIState_MonsterFree,
						csdefine.AIS_MONSTER_FIGHT: AIState.AIState_MonsterFight,
						csdefine.AIS_MONSTER_RESET: AIState.AIState_MonsterReset
					}
	
	def getDefaultAIState( self ):
		"""
		virtual method
		获取默认AI状态
		"""
		return csdefine.AIS_MONSTER_FREE
	
	def getRelativeAIEvent( self ):
		"""
		virtual method
		获取状态机关心的AI事件
		为了提高效率，只有发生此列表中的事件时，才检测是否切换状态
		"""
		return [csdefine.AI_EVENT_COM_STATE_CHANGE]
	
	def getNewAIState( self, entity, eventType, params ):
		"""
		virtual method
		根据被触发的AI事件获取新的AI状态
		"""
		if eventType == csdefine.AI_EVENT_COM_STATE_CHANGE:
			if params["newState"] == csdefine.COMBAT_STATE_FREE:	#变为自由状态
				return csdefine.AIS_MONSTER_FREE
			if params["newState"] == csdefine.COMBAT_STATE_FIGHT:	#变为战斗状态
				return csdefine.AIS_MONSTER_FIGHT
			if params["newState"] == csdefine.COMBAT_STATE_RESET:	#变为回走状态
				return csdefine.AIS_MONSTER_RESET
		
		return csdefine.AIS_NONE
	