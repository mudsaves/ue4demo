# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import random
import time

from Skill.Base.SkillLoader import g_skillLoader
from Skill.PassiveSkill.PassiveSkillLoader import g_passiveSkillLoader
from Skill.Base.BuffLoader import g_buffLoader
from Skill.Base.CooldownTypeLoader import g_cdTypeLoader
from Quest.Base.QuestLoader import g_questLoader
from CombatRelationMgr import g_combatRelationMgr
from Item.Base.ItemFactory import g_itemFactory
from AI.Base.AICfgLoader import g_aiCfgLoader

g_skillLoader.loadSkill( "scripts/data/SkillConfig.json" )
g_passiveSkillLoader.loadSkill( "scripts/data/PassiveSkill.json" )
g_buffLoader.loadBuff( "scripts/data/BuffConfig.json" )
g_cdTypeLoader.loadCooldownType( "scripts/data/CooldownType.json" )
g_questLoader.loadQuest( "scripts/data/QuestConfig.json" )
g_combatRelationMgr.loadSpaceAttackRelCfg( "scripts/data/SpaceAttackRelationConfig.json" )
g_itemFactory.loadItemCfg( "scripts/data/Item" )
g_aiCfgLoader.loadAICfg( "scripts/data/AI" )

def onInit(isReload):
	"""
	KBEngine method.
	当引擎启动后初始化完所有的脚本后这个接口被调用
	"""
	DEBUG_MSG('onInit::isReload:%s' % isReload)
	#初始化随机函数
	random.seed(int((time.time()*100)%256))
	
	KBEngine.loadGeometryMapping( None, "spaces/nav_test", {} )
	
def onGlobalData(key, value):
	"""
	KBEngine method.
	globalData改变 
	"""
	DEBUG_MSG('onGlobalData: %s' % key)
	
def onGlobalDataDel(key):
	"""
	KBEngine method.
	globalData删除 
	"""
	DEBUG_MSG('onDelGlobalData: %s' % key)

def onCellAppData(key, value):
	"""
	KBEngine method.
	cellAppData改变 
	"""
	DEBUG_MSG('onCellAppData: %s' % key)
	
def onCellAppDataDel(key):
	"""
	KBEngine method.
	cellAppData删除 
	"""
	DEBUG_MSG('onCellAppDataDel: %s' % key)
	
def onSpaceData( spaceID, key, value ):
	"""
	KBEngine method.
	spaceData改变
	"""
	pass
	
def onAllSpaceGeometryLoaded( spaceID, isBootstrap, mapping ):
	"""
	KBEngine method.
	space 某部分或所有chunk等数据加载完毕
	具体哪部分需要由cell负责的范围决定
	"""
	pass