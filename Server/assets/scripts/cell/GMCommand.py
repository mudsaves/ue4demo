# -*-coding: utf-8 -*-

import KBEMath
import KBEngine
import csdefine
from KBEDebug import *

g_gmCommandDict = {}

def gmCommandGotoSpace( srcEntity, dstEntity, args ):
	"""
	传送
	"""
	argList = args.split(None)
	argLen = len(argList)
	if argLen != 4:
		return
	if KBEngine.getSpaceData(srcEntity.spaceID, "MappingPath") == argList[0]:
		return
	position  = KBEMath.Unreal2KBEnginePosition( (float(argList[1]) , float(argList[2]) , float(argList[3])) )
	srcEntity.position = position
	srcEntity.requestTeleport( srcEntity.id )

def gmCommandFull( srcEntity, dstEntity, args ):
	"""
	满血
	"""
	srcEntity.full()

def gmCommandRevive( srcEntity, dstEntity, args ):
	"""
	复活
	"""
	srcEntity.revive()

def gmCommandAddItem( srcEntity, dstEntity, args ):
	"""
	添加物品
	"""
	argList = args.split(None)
	argLen = len(argList)
	
	itemID = 0
	amount = 1
	if argLen >= 1:
		itemID = int(argList[0])
	if argLen >= 2:
		amount = int(argList[1])
	
	if itemID:
		srcEntity.addItemByID( itemID, amount, csdefine.ADD_ITEM_GM )

def gmCommandCompleteTask( srcEntity, dstEntity, args ):
	"""
	任务目标增加完成数量
	"""
	argList = args.split(None)
	argLen = len(argList)
	
	questID = 0
	taskIndex = 0
	count = 1
	if argLen >= 1:
		questID = int(argList[0])
	if argLen >= 2:
		taskIndex = int(argList[1])
	if argLen >= 3:
		count = int(argList[2])
	
	srcEntity.questTaskIncreaseState( questID, taskIndex, count )

def gmCommandRemoveCompleteQuest( srcEntity, dstEntity, args ):
	"""
	移除某任务的提交记录
	"""
	argList = args.split(None)
	argLen = len(argList)
	
	questID = 0
	if argLen >= 1:
		questID = int(argList[0])
	
	srcEntity.removeQuestLog( questID )

def gmCommandCloneControlledMonster( srcEntity, dstEntity, args ):
	"""
	创建一堆由自己客户端控制的monster
	"""
	argList = args.split(None)
	amount = int(argList[0])
	
	direction = ( 0.0, 0.0, 0.0 )
	properties = { "modelID":1, "moveSpeed":1.0, "controllerByID":srcEntity.id }
	eList = []
	for i in range(amount):
		KBEngine.createEntity( "Monster", srcEntity.spaceID, srcEntity.position, direction, properties )

def ADD_COMMAND( cmd, func ):
	"""
	@param cmd:string
	@param cmd:GM命令
	@param grade:int
	@param grade:当前GM命令的权限执行等级
	@param func:string
	@param func:GM命令对应的执行函数
	"""
	assert cmd not in g_gmCommandDict
	g_gmCommandDict[cmd] = func

# 增加命令字典
# **********************************begin of ADD_COMMAND**********************************
ADD_COMMAND( "goto",							gmCommandGotoSpace )
ADD_COMMAND( "full",							gmCommandFull )
ADD_COMMAND( "revive",							gmCommandRevive )
ADD_COMMAND( "addItem",							gmCommandAddItem )
ADD_COMMAND( "completeTask",					gmCommandCompleteTask )
ADD_COMMAND( "remove_completed_quest",			gmCommandRemoveCompleteQuest )
ADD_COMMAND( "clone_controlled_monster",		gmCommandCloneControlledMonster )

# **********************************end of ADD_COMMAND************************************

def executeGMCommand( srcEntity, dstEntityID, command, args ):
	"""
	执行一条GM命令
	@param	srcEntity:		Entity
	@param	srcEntity:		GM命令使用者
	@param	dstEntityID:	OBJECT_ID
	@param	dstEntityID:	目标entityID
	@param	command:		STRING
	@param	command:		GM命令
	@param	args:			STRING
	@param	args:			命令参数表,根据不同命令有不同的格式,各命令自行解释
	"""
	dstEntity = KBEngine.entities.get( dstEntityID, None )
	if dstEntityID == srcEntity.id or dstEntity == None:
		dstEntity = srcEntity
	if not command in g_gmCommandDict:
		ERROR_MSG("Command not exist!")					#GM命令没有定义
		return
	
	INFO_MSG("Use GM command. player:%s, command:%s."%(srcEntity.id, command))
	func = g_gmCommandDict[command]
	func( srcEntity, dstEntity, args )					#执行指令函数