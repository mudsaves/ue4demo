# -*- coding: utf-8 -*-

import copy
import csdefine
import csconst
import KBEngine
from KBEDebug import *
from CombatRelationMgr import g_combatRelationMgr

class CombatInterface:
	"""
	战斗接口
	"""
	def __init__( self ):
		pass
	
	def onTimer( self, id, userArg ):
		"""
		"""
		if userArg == csdefine.FIGHT_STATE_TIMER:
			self.onFightTimer()
	
	def onFightTimer( self ):
		"""
		virtual method
		战斗状态循环timer
		"""
		invalidEnemy = []
		for id in self.enemyList:
			enemy = KBEngine.entities.get( id, None )
			if not enemy or not self.canAttack( enemy ):	#无效的敌人移掉
				invalidEnemy.append( id )
		
		for id in invalidEnemy:
			self.removeEnemy( id )
	
	def getState( self ):
		return self.state
	
	def canAttack( self, target ):
		"""
		能否攻击目标
		"""
		if self.id == target.id:
			return False
		if self.spaceID != target.spaceID:
			return False
		if not hasattr( target, "state" ):
			return False
		if target.getState() == csdefine.STATE_DEAD:
			return False
		if target.id in self.enemyList:
			return True
		
		key = KBEngine.getSpaceData( self.spaceID, "AttackRelationKey")
		return g_combatRelationMgr.canAttack( key, self, target )
	
	def full( self ):
		"""
		满血
		"""
		self.HP = self.HP_Max
	
	def changeState( self, state ):
		"""
		生存状态改变
		"""
		if self.state == state:
			return
		oldState = self.state
		self.state = state
		
		params = { "oldState": oldState, "newState": self.state }
		self.triggerSkillEvent( 0, csdefine.SKILL_EVENT_STATE_CHANGE, params )
	
	def changeCombatState( self, state ):
		"""
		战斗状态改变
		"""
		if self.combatState == state:
			return
		oldState = self.combatState
		self.combatState = state
		self.onChangeCombatState( oldState, state )
	
	def onChangeCombatState( self, oldState, state ):
		"""
		virtual method
		战斗状态改变时做一些事
		"""
		if state == csdefine.COMBAT_STATE_FIGHT:
			self.fightTimerID = self.addTimer( 1, 1, csdefine.FIGHT_STATE_TIMER )
		
		elif oldState == csdefine.COMBAT_STATE_FIGHT:
			if self.fightTimerID:
				self.delTimer( self.fightTimerID )
				self.fightTimerID = 0
	
	def addEnemy( self, enemyID ):
		"""
		添加敌人
		"""
		if enemyID not in self.enemyList:
			self.enemyList.append( enemyID )
			self.onAddEnemy( enemyID )
	
	def onAddEnemy( self, enemyID ):
		"""
		virtual method
		"""
		pass
	
	def removeEnemy( self, enemyID ):
		"""
		移除敌人
		"""
		if enemyID in self.enemyList:
			self.enemyList.remove( enemyID )
			self.onRemoveEnemy( enemyID )
	
	def onRemoveEnemy( self, enemyID ):
		"""
		virtual method
		"""
		pass
	
	def resetEnemy( self ):
		"""
		重置敌人列表
		"""
		self.enemyList = []
	
	def die( self, attacker ):
		"""
		virtual method
		死亡
		"""
		self.resetEnemy()
		self.changeState( csdefine.STATE_DEAD )
		self.changeCombatState( csdefine.COMBAT_STATE_FREE )
		if attacker:
			attacker.onKillEntity( self )
			DEBUG_MSG("(%s) were killed by (%s)."%(self.id, attacker.id))
		else:
			DEBUG_MSG("(%s) are dead."%self.id)
	
	def onKillEntity( self, entity ):
		"""
		vitual method
		"""
		pass
	
	def addHP( self, val ):
		"""
		加血
		"""
		self.HP = min( self.HP + val, self.HP_Max )
	
	def receiveDamage( self, damage, attacker ):
		"""
		接受伤害
		"""
		if self.HP == 0:
			return 0
		
		damage = min( damage, self.HP )
		self.HP -= damage
		
		attackerID = 0
		if attacker:
			attackerID = attacker.id
		
		if self.HP == 0:
			self.die( attacker )
		else:
			if attackerID and attackerID != self.id:
				self.addEnemy( attackerID )
				attacker.addEnemy( self.id )
		
		params = { "damageAmount": damage }
		self.triggerSkillEvent( attackerID, csdefine.SKILL_EVENT_RECEIVE_DAMAGE, params )
		
		return damage
	
	def beVertigo( self, attacker ):
		"""
		被眩晕
		"""
		if attacker and attacker.id != self.id:
			self.addEnemy( attacker.id )
			attacker.addEnemy( self.id )
	
	def beTaunt( self, attacker ):
		"""
		被嘲讽
		"""
		if attacker and attacker.id != self.id:
			self.addEnemy( attacker.id )
			attacker.addEnemy( self.id )
	
	#--------------------------战斗外部接口--------------------------
	def receiveDamageBySkill( self, val, isPure, skillID, attacker ):
		"""
		接受技能伤害
		"""
		if not isPure:
			pass	#不是直接伤害则要根据攻击力、防御力等计算最终伤害
		
		damage = self.receiveDamage( val, attacker )
		if damage > 0:
			attackerID = attacker.id if attacker!=None else 0
			DEBUG_MSG("%s receive skill damage. val:%s, skillID:%s, attacker:%s."%(self.id, damage, skillID, attackerID))
	
	def receiveDamageByBuff( self, val, isPure, buffID ):
		"""
		接受buff伤害
		"""
		if not isPure:
			pass	#不是直接伤害则要根据攻击力、防御力等计算最终伤害
		
		damage = self.receiveDamage( val, None )
		if damage > 0:
			DEBUG_MSG("%s receive buff damage. val:%s, buffID:%s."%(self.id, damage, buffID))