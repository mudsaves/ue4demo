# -*- coding: utf-8 -*-

import json
import SmartImport
from KBEDebug import *
import KBEngine

class AttackRelationBase:
	"""
	攻击关系基类
	"""
	@staticmethod
	def canAttack( attacker, target ):
		return False

class RoleAR_Peace( AttackRelationBase ):
	"""
	玩家攻击关系：不能打其他任何entity
	"""
	@staticmethod
	def canAttack( attacker, target ):
		"""
		"""
		return False

class RoleAR_Fight( AttackRelationBase ):
	"""
	玩家攻击关系：能打其他玩家和怪物
	"""
	@staticmethod
	def canAttack( attacker, target ):
		"""
		"""
		if target.__class__.__name__ in ["Account", "Monster"]:
			return True
		return False

class MonsterAR_Peace( AttackRelationBase ):
	"""
	怪物攻击关系：不能打其他任何entity
	"""
	@staticmethod
	def canAttack( attacker, target ):
		"""
		"""
		return False

class MonsterAR_Fight( AttackRelationBase ):
	"""
	怪物攻击关系：能打其他玩家和怪物
	"""
	@staticmethod
	def canAttack( attacker, target ):
		"""
		"""
		if target.__class__.__name__ in ["Account", "Monster"]:
			return True
		return False


class CombatRelationMgr:
	"""
	战斗关系管理器
	"""
	_instance = None
	def __init__( self ):
		assert CombatRelationMgr._instance is None
		CombatRelationMgr._instance = self
		self.spaceAttackRelDict = {}	#地图攻击关系管理实例字典
	
	@staticmethod
	def instance():
		if not CombatRelationMgr._instance:
			CombatRelationMgr._instance = CombatRelationMgr()
		return CombatRelationMgr._instance
	
	def loadSpaceAttackRelCfg( self, filePath ):
		"""
		"""
		absFilePath = KBEngine.getResFullPath(filePath)
		file = open( absFilePath, encoding="utf8" )
		self.spaceAttackRelDict = json.loads( file.read() )
		file.close()
	
	def canAttack( self, spaceRelKey, attacker, target ):
		"""
		"""
		spaceRelDict = self.spaceAttackRelDict.get( spaceRelKey, None )
		if not spaceRelDict:
			return False
		
		relationCls = spaceRelDict.get( attacker.__class__.__name__, None )
		if not relationCls:
			return False
		
		try:
			return eval(relationCls).canAttack( attacker, target )
		except:
			ERROR_MSG("Attack relation class error, (%s)."%relationCls)
			return False

g_combatRelationMgr = CombatRelationMgr()