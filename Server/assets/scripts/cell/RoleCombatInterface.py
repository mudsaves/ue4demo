# -*- coding: utf-8 -*-

import csdefine
import csconst
import KBEngine
import Functions
from KBEDebug import *
from CombatInterface import CombatInterface

class RoleCombatInterface( CombatInterface ):
	"""
	玩家战斗接口
	"""
	def __init__( self ):
		CombatInterface.__init__( self )
		self.power = 0				#力量
		self.agile = 0				#敏捷
		self.intelligence = 0		#智力
		self.baseSkill = 0			#普通攻击技能
		self.roleEnemyList = {}		#记录玩家敌人:{玩家ID:最后一次攻击或被攻击的时间}
		self.caculateProperty()
		self.full()
	
	def caculateProperty( self ):
		"""
		计算相关属性
		"""
		self.attack = int(self.power*0.1)
		self.defense = int(self.agile*0.1)
		self.HP_Max = csconst.INIT_HP
	
	def onFightTimer( self ):
		"""
		virtual method
		战斗状态循环timer
		"""
		CombatInterface.onFightTimer( self )
		
		deleteEnemyList = []
		for id, t in self.roleEnemyList.items():
			if Functions.getFloatTime( Functions.getTime() - t ) > csconst.ROLE_ENEMY_PERSIST_TIME:	#超过8秒互相移除敌人列表
				deleteEnemyList.append( id )
		
		for id in deleteEnemyList:
			self.removeEnemy( id )
			enemy = KBEngine.entities.get( id, None )
			if enemy:
				enemy.removeEnemy( self.id )
	
	def addEnemy( self, enemyID ):
		"""
		添加敌人
		"""
		CombatInterface.addEnemy( self, enemyID )
		enemy = KBEngine.entities.get( enemyID )
		if enemy and enemy.__class__.__name__ == "Account":
			self.roleEnemyList[enemyID] = Functions.getTime()
	
	def onAddEnemy( self, enemyID ):
		"""
		virtual method
		"""
		if len(self.enemyList) == 1:
			self.changeCombatState( csdefine.COMBAT_STATE_FIGHT )
	
	def removeEnemy( self, enemyID ):
		"""
		移除敌人
		"""
		CombatInterface.removeEnemy( self, enemyID )
		if enemyID in self.roleEnemyList:
			self.roleEnemyList.pop( enemyID )
	
	def onRemoveEnemy( self, enemyID ):
		"""
		virtual method
		"""
		if len(self.enemyList) == 0:
			self.changeCombatState( csdefine.COMBAT_STATE_FREE )
	
	def die( self, attacker ):
		"""
		virtual method
		死亡
		"""
		CombatInterface.die( self, attacker )
		self.questOnPlayerDie()
	
	def onKillEntity( self, entity ):
		"""
		vitual method
		"""
		if entity.__class__.__name__ == "Monster":
			self.questKillMonster( "" )
	
	#--------------------------战斗外部接口--------------------------
	def revive( self ):
		"""
		复活
		"""
		if self.getState() != csdefine.STATE_DEAD:
			return
		self.changeState( csdefine.STATE_LIVE )
		self.HP = csconst.INIT_HP
	