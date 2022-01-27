# -*- coding: utf-8 -*-

import csdefine
import csconst
from CombatInterface import CombatInterface

class MonsterCombatInterface( CombatInterface ):
	"""
	怪物战斗接口
	"""
	def __init__( self ):
		CombatInterface.__init__( self )
		self.baseSkill = 0				#普通攻击技能
		self.caculateProperty()
		self.full()
	
	def caculateProperty( self ):
		"""
		计算相关属性
		"""
		self.HP_Max = csconst.INIT_HP
	
	def die( self, attacker ):
		"""
		virtual method
		死亡
		"""
		CombatInterface.die( self, attacker )
		self.triggerAIEvent( csdefine.AI_EVENT_DIE, {} )	#必须先触发事件再关闭AI系统，否则死亡AI事件里配的AI无法执行
		self.stopAISys()
		self.addTimer( 2, 0.0, 111 )
	
	def onChangeCombatState( self, oldState, state ):
		"""
		virtual method
		战斗状态改变时做一些事
		"""
		CombatInterface.onChangeCombatState( self, oldState, state )
		params = { "oldState": oldState, "newState": state }
		self.triggerAIEvent( csdefine.AI_EVENT_COM_STATE_CHANGE, params )
	
	def onAddEnemy( self, enemyID ):
		"""
		virtual method
		"""
		if len(self.enemyList) == 1:
			self.changeCombatState( csdefine.COMBAT_STATE_FIGHT )
	
	def onRemoveEnemy( self, enemyID ):
		"""
		virtual method
		"""
		if len(self.enemyList) == 0:
			self.changeCombatState( csdefine.COMBAT_STATE_RESET )