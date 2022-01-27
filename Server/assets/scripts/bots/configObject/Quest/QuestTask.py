# -*- coding: utf-8 -*-

import KBEngine
import Const
import Math
import KBEMath
import csdefine
import KST_Config
import Extra.Extend as Extend

from Functor import Functor
from KBEDebug import *
from Extra.SkillLoader import g_skillLoader

class QuestTask:
	"""
	"""
	def __init__( self ):
		self.questID = 0	#任务ID
		self.index = 0		#目标索引
		self.str1 = ""
		self.str2 = ""
		self.str3 = ""
		self.val1 = 0		#要完成数量
		self.val2 = 0		#已完成数量
		self.val3 = 0
		
		self.doCBID = 0
	
	def init( self, questID, config ):
		"""
		用本地配置初始化目标实例
		"""
		self.questID = questID
		self.index = config["index"]
	
	def updateFromServerData( self, taskData ):
		"""
		用服务器发来的数据更新本地数据
		"""
		self.str1 = taskData["str1"]
		self.str2 = taskData["str2"]
		self.str3 = taskData["str3"]
		self.val1 = taskData["val1"]
		self.val2 = taskData["val2"]
		self.val3 = taskData["val3"]
	
	def addDoCallback( self, player, time ):
		"""
		添加do callback
		"""
		if self.doCBID:
			KBEngine.cancelCallback( self.doCBID )
		
		func = Functor( self.do, player )
		self.doCBID = KBEngine.callback( time, func )
	
	def cancelDoCallback( self ):
		"""
		取消do callback
		"""
		if self.doCBID:
			KBEngine.cancelCallback( self.doCBID )
			self.doCBID = 0
	
	def tryDo( self, player ):
		if self.doCBID:		#此id不为0说明已经在do了
			return
		self.do( player )
	
	def do( self, player ):
		"""
		"""
		self.addDoCallback( player, 5 )
	
	def updateState( self, player, isComplete, isFail, count ):
		"""
		更新状态
		"""
		self.val2 = count
		if isComplete:
			self.onComplete( player )
		
		if isFail:
			self.onFail( player )
	
	def isComplete( self ):
		"""
		是否完成
		"""
		return self.val2 >= self.val1
		
	def onComplete( self, player ):
		"""
		"""
		self.cancelDoCallback()
	
	def onFail( self, player ):
		"""
		"""
		self.cancelDoCallback()
	
	def onRemove( self, player ):
		"""
		"""
		self.cancelDoCallback()

class QTKillMonster( QuestTask ):
	"""
	杀怪
	"""
	def __init__( self ):
		QuestTask.__init__( self )
		self.monsterSpace = ""
		self.monsterPos = None
		
		skillCfg = g_skillLoader.getSkill( Const.DEFAULT_ATTACK_MONSTER_SKILL )
		self.attackDis = skillCfg.get( "minDis", -1 )
		if self.attackDis < 0:	#技能没有距离要求，就取默认值
			self.attackDis = Const.DEFAULT_ATTACK_DIS
	
	def init( self, questID, config ):
		QuestTask.init( self, questID, config )
		tempList = config["param2"].split("#")
		self.monsterSpace = tempList[0]
		self.monsterPos = tempList[1]
	
	def do( self, player ):
		"""
		"""
		QuestTask.do( self, player )
		
		pos = Extend.strToPosition( self.monsterPos )
		kbePos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( pos ) )
		
		spaceID = player.clientapp.getSpaceData("MappingPath")
		#不在目标地图
		if spaceID != self.monsterSpace:
			player.GMCommand( player.id, "goto", "{} {} {} {}".format(self.monsterSpace, pos[0], pos[1], pos[2]) )
			return
		
		#距离太远
		if player.position.distTo( kbePos ) > Const.DEFAULT_KILL_TASK_DIS:
			randPos = Extend.getRandomPosInRange( kbePos, Const.DEFAULT_KILL_TASK_DIS )
			player.moveToPos( randPos )
			return
		
		targetID = 0
		skillCfg = g_skillLoader.getSkill( Const.DEFAULT_ATTACK_MONSTER_SKILL )
		if skillCfg.get( "targetType", "SKILL_TARGET_NONE" ) == "SKILL_TARGET_ENTITY":
			monsters = Extend.entitiesInRange( player, self.attackDis, \
				cnd = lambda entity : True if entity.__class__.__name__ == "Monster" and player.canAttack( entity ) else False)
			
			#找不到怪，再走走
			if len(monsters) == 0:
				randPos = Extend.getRandomPosInRange( kbePos, Const.DEFAULT_KILL_TASK_DIS )
				player.moveToPos( randPos )
				return
			
			targetID = monsters[0].id
		
		player.cell.reqUseSkill( Const.DEFAULT_ATTACK_MONSTER_SKILL, targetID )

class QTGiveItems( QuestTask ):
	"""
	获取物品
	"""
	def __init__( self ):
		QuestTask.__init__( self )
		self.itemID = ""
	
	def init( self, questID, config ):
		QuestTask.init( self, questID, config )
		self.itemID = config["param1"]
		
	def do( self, player ):
		QuestTask.do( self, player )
		player.GMCommand( player.id, "addItem", "{} {}".format(self.itemID, self.val1 ) )

class QTDieLessAmount( QuestTask ):
	"""
	死亡少于N次
	"""
	pass

class QTDirectTrigger( QuestTask ):
	"""
	触发类任务目标
	"""
	def __init__( self ):
		QuestTask.__init__( self )
		self.space = ""
		self.pos = None
	
	def init( self, questID, config ):
		QuestTask.init( self, questID, config )
		if config["param1"] != "":
			tempList = config["param1"].split("#")
			self.space = tempList[0]
			self.pos = tempList[1]
	
	def do( self, player ):
		"""
		"""
		QuestTask.do( self, player )
		
		if self.space == "":
			player.GMCommand( player.id, "completeTask", "{} {} {}".format(self.questID, self.index, self.val1) )
			return
		
		pos = Extend.strToPosition( self.pos )
		kbePos = Math.Vector3( KBEMath.Unreal2KBEnginePosition( pos ) )
		
		spaceID = player.clientapp.getSpaceData("MappingPath")
		#不在目标地图
		if spaceID != self.space:
			player.GMCommand( player.id, "goto", "{} {} {} {}".format(self.space, pos[0], pos[1], pos[2]) )
			return
		
		#距离太远
		if player.position.distTo( kbePos ) > Const.DEFAULT_TRIGGER_TASK_DIS:
			randPos = Extend.getRandomPosInRange( kbePos, Const.DEFAULT_TRIGGER_TASK_DIS )
			player.moveToPos( randPos )
			return
		
		player.GMCommand( player.id, "completeTask", "{} {} {}".format(self.questID, self.index, self.val1))


#目标类型枚举值与目标类map
type2Class_map = {	csdefine.QT_TYPE_KILL_MONSTER			: QTKillMonster,
					csdefine.QT_TYPE_GIVE_ITEM				: QTGiveItems,
					csdefine.QT_TYPE_DIE_LESS_AMOUNT		: QTDieLessAmount,
					csdefine.QT_TYPE_DIRECT_TRIGGER			: QTDirectTrigger,
					}


def newInstanceByType( type ):
	cls = type2Class_map.get( type, None )
	if not cls:
		return None
	return cls()

def newInstanceByCls( className ):
	return eval( className )()