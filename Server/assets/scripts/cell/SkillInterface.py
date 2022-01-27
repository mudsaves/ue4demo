# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import csdefine
import csstatus
import Functions
import SkillTargetObjImpl

from BuffsPacketImpl import BuffsPacketImpl
from CooldownsPacketImpl import CooldownsPacketImpl
from Skill.Base.SkillLoader import g_skillLoader
from Skill.PassiveSkill.PassiveSkillLoader import g_passiveSkillLoader
from Skill.Base.BuffLoader import g_buffLoader
from Skill.Base.CooldownTypeLoader import g_cdTypeLoader

MAX_BUFF_INDEX = 65535

class SkillInterface:
	"""
	技能接口
	"""
	def __init__( self ):
		pass
	
	def onTimer( self, id, userArg ):
		"""
		"""
		if id == self.skillTaskTimerID:
			self.skillTaskTimerID = 0
			self.onSkillTaskTimeEnd()
		
		if userArg == csdefine.BUFF_LOOP_TIMER:
			self.onBuffLoopTimer( id )
		elif userArg == csdefine.BUFF_END_TIMER:
			self.onBuffEndTimer( id )
	
	def getSkill( self, skillID ):
		"""
		获取技能全局实例
		"""
		return g_skillLoader.getSkill( skillID )
	
	def getPassiveSkill( self, skillID ):
		"""
		获取被动技能全局实例
		"""
		return g_passiveSkillLoader.getSkill( skillID )
	
	#-------------------------------技能相关-----------------------------
	def isCastingSkill( self ):
		return self.castingSkill != 0
	
	def interruptSkill( self, reason ):
		"""
		尝试打断当前技能
		"""
		if self.castingSkill == 0:
			return
		skillIns = self.getSkill( self.castingSkill )
		if skillIns.canInterrupt( reason ):
			skillIns.onInterrupt( self, reason )
	
	def reqUseSkill( self, srcEntityID, skillID, targetID ):
		"""
		Exposed method
		"""
		if self.id != srcEntityID:
			return
		self.useSkill( skillID, targetID )
	
	def useSkill( self, skillID, targetID ):
		"""
		define method
		"""
		DEBUG_MSG("Entity(%s) use skill(%s) to target(%s)."%(self.id, skillID, targetID))
		if self.isCastingSkill():
			return csstatus.SKILL_IS_CASTING
		
		skillIns = self.getSkill( skillID )
		
		targetObj = None
		if skillIns.getTargetType() == csdefine.SKILL_TARGET_NONE:	#如果是无目标技能，则把自己作为目标
			targetObj = SkillTargetObjImpl.createEntityTargetObj( self )
		
		elif skillIns.getTargetType() == csdefine.SKILL_TARGET_ENTITY:
			entity = KBEngine.entities.get( targetID )
			if entity:
				targetObj = SkillTargetObjImpl.createEntityTargetObj( entity )
		
		elif skillIns.getTargetType() == csdefine.SKILL_TARGET_POSITION:
			entity = KBEngine.entities.get( targetID )
			if entity:
				targetObj = SkillTargetObjImpl.createPositionTargetObj( entity.position )
		
		if not targetObj:
			return csstatus.SKILL_TARGET_TYPE_ERR
		
		return skillIns.use( self, targetObj )
	
	def useSkillToPosition( self, skillID, position ):
		"""
		define method
		"""
		DEBUG_MSG("Entity(%s) use position skill(%s) to target(%s)."%(self.id, skillID, position))
		if self.isCastingSkill():
			return csstatus.SKILL_IS_CASTING
		
		skillIns = self.getSkill( skillID )
		if skillIns.getTargetType() != csdefine.SKILL_TARGET_POSITION:
			ERROR_MSG("Skill(%s) target type is not position."%skillID)
			return csstatus.SKILL_TARGET_TYPE_ERR
		
		targetObj = SkillTargetObjImpl.createPositionTargetObj( position )
		return skillIns.use( self, targetObj )
	
	def onSkillTaskTimeEnd( self ):
		"""
		技能任务持续时间到达
		"""
		skillID = self.skillTaskTimerParam["skillID"]
		taskIndex = self.skillTaskTimerParam["taskIndex"]
		target = self.skillTaskTimerParam["target"]
		successReceiver = self.skillTaskTimerParam["successReceiver"]
		self.getSkill(skillID).onTaskTimeEnd( taskIndex, self, target, successReceiver )
	
	def onSkillCastOver( self, skillID ):
		"""
		virtual method
		技能释放完毕
		"""
		pass
	
	def onSkillInterrupted( self, skillID ):
		"""
		virtual method
		技能被打断
		"""
		pass
	
	def refreshCooldownData( self ):
		"""
		刷新cd数据
		"""
		remainData = CooldownsPacketImpl()
		for cdID, cdData in self.skillCooldowns.items():
			if cdData["endTime"] > Functions.getTime():
				remainData[cdID] = cdData
		self.skillCooldowns = remainData
	
	def addCooldown( self, cooldownList ):
		"""
		添加一组cd
		cooldownList格式:[(cdID,cdTime)]
		"""
		self.refreshCooldownData()	#先刷新一下，防止有残留数据
		
		for cdID, cdTime in cooldownList:
			cooldown = g_cdTypeLoader.getCooldown( cdID )
			if not cooldown:
				ERROR_MSG("Cooldown id(%s) not exist!"%cdID)
				continue
			
			newEndTime = Functions.getTime(cdTime)
			if cdID not in self.skillCooldowns:
				self.skillCooldowns[ cdID ] = { "endTime": newEndTime, "timeFlag":0 }
			else:
				cdData = self.skillCooldowns[ cdID ]
				if newEndTime > cdData["endTime"]:
					cdData["endTime"] = newEndTime
	
	def getCooldown( self ):
		"""
		获取冷却时间
		"""
		return self.skillCooldowns

	def calculateCooldownsOnDestroy( self ):
		"""
		销毁时计算cooldowns数据,针对下线是否保存及继续计时的处理
		"""
		dels = []
		for cdID, data in self.skillCooldowns.items():
			try:
				cooldown = g_cdTypeLoader.getCooldown( cdID )
			except KeyError:
				dels.append( cdID ) 	# cooldown 类型不存在则删除，此情况的可能是手动修改了数据库或废弃了已存在的旧的cooldown
				continue
			
			if data["endTime"] < Functions.getTime():
				dels.append( cdID )	# 删除已过时的cooldown
				continue
			
			if cooldown.isSave():
				data["endTime"] = cooldown.calculateOnSave( data["endTime"] )
				data["timeFlag"] = 1	#用来标记endTime是经过计算的
			else:
				dels.append( cdID )	# 不保存的cooldown全部删除
		
		for cdID in dels:
			self.skillCooldowns.pop( cdID )

	def calculateCooldownsOnInit( self ):
		"""
		初始化时重新计算cooldowns数据，针对下线是否保存及继续计时的处理
		"""
		dels = []
		for cdID, data in self.skillCooldowns.items():
			try:
				cooldown = g_cdTypeLoader.getCooldown( cdID )
			except KeyError:
				dels.append( cdID ) 	# cooldown 类型不存在则删除，此情况的可能是手动修改了数据库或废弃了已存在的旧的cooldown
				continue
			
			if data["timeFlag"] == 1:
				data["timeFlag"] = 0
				data["endTime"] = cooldown.calculateOnLoad( data["endTime"] )
			# 在coolDown数据恢复之后进行判断，删除已过时的coolDown
			if data["endTime"] < Functions.getTime():
				dels.append( cdID )
		
		for cdID in dels:
			self.skillCooldowns.pop( cdID )
	
	#-------------------------------被动技能相关-----------------------------
	def gainPassiveSkill( self, skillID ):
		"""
		添加被动技能
		"""
		if skillID in self.passiveSkillList:	#后续流程需保证身上没有两个相同ID的被动技能
			return
		self.passiveSkillList.append( skillID )
		skillIns = self.getPassiveSkill( skillID )
		skillIns.onAttach( self )
	
	def removePassiveSkill( self, skillID ):
		"""
		"""
		if skillID not in self.passiveSkillList:
			return
		self.passiveSkillList.remove( skillID )
		skillIns = self.getPassiveSkill( skillID )
		skillIns.onDetach( self )
	
	def addListenSkillEvent( self, eventType, skillID ):
		"""
		注册技能事件
		"""
		if eventType not in self.skillEventTable:
			self.skillEventTable[eventType] = [ skillID ]
		else:
			self.skillEventTable[eventType].append( skillID )
	
	def removeListenSkillEvent( self, eventType, skillID ):
		"""
		注销技能事件
		"""
		if eventType not in self.skillEventTable:
			return
		if skillID not in self.skillEventTable[eventType]:
			return
		self.skillEventTable[eventType].remove( skillID )
		if len(self.skillEventTable[eventType]) == 0:
			self.skillEventTable.pop( eventType )
	
	def attachPassiveSkillOnInit( self ):
		"""
		上线时重新加载被动技能
		"""
		for skillID in self.passiveSkillList:
			skillIns = self.getPassiveSkill( skillID )
			if not skillIns:
				ERROR_DEBUG("Reload passive skill error! skillID:%s."%skillID)
				continue
			skillIns.onAttach( self )
	
	def detachPassiveSkillOnDestroy( self ):
		"""
		下线时卸载被动技能效果
		"""
		for skillID in self.passiveSkillList:
			skillIns = self.getPassiveSkill( skillID )
			if not skillIns:
				continue
			skillIns.onDetach( self )
	
	def triggerSkillEvent( self, triggerID, eventType, eventParams ):
		"""
		触发被动技能事件
		"""
		if eventType not in self.skillEventTable:
			return
		
		for skillID in self.skillEventTable[eventType]:
			skillIns = self.getPassiveSkill( skillID )
			
			targetObj = None
			if skillIns.getTargetType() == csdefine.SKILL_TARGET_NONE:			#如果是无目标技能，则把自己作为目标
				targetObj = SkillTargetObjImpl.createEntityTargetObj( self )
			elif skillIns.getTargetType() == csdefine.SKILL_TARGET_ENTITY:		#否则取触发者为技能施展目标
				entity = KBEngine.entities.get( triggerID )
				if entity:
					targetObj = SkillTargetObjImpl.createEntityTargetObj( entity )
			
			if not targetObj:
				continue
			
			skillIns.use( self, targetObj, eventParams )
	
	#-------------------------------Buff相关-----------------------------
	def newBuffIndex( self ):
		"""
		产生一个新的buffindex
		合法index范围：0~MAX_BUFF_INDEX-1
		"""
		index = (self.lastBuffIndex + 1) % MAX_BUFF_INDEX
		while(True):
			if index not in self.attrBuffs:
				break
			
			if index == self.lastBuffIndex:		#从0到MAX_BUFF_INDEX-1都被占着，说明buff数量达到MAX_BUFF_INDEX，理论上来说身上不可能有这么多buff，所以报个错
				ERROR_MSG("Buff amount is more than %s!" % MAX_BUFF_INDEX)
				return -1
			
			index = (index + 1) % MAX_BUFF_INDEX
		
		self.lastBuffIndex = index
		return self.lastBuffIndex
	
	def getBuff( self, buffID ):
		"""
		获取buff实例
		"""
		return g_buffLoader.getBuff( buffID )
	
	def getBuffDataByIndex( self, buffIndex ):
		"""
		根据buffIndex获取buffData
		"""
		return self.attrBuffs.get( buffIndex, None )
	
	def getBuffIndexByID( self, buffID ):
		"""
		根据ID获取buffIndex
		"""
		result = []
		for buffData in self.attrBuffs.values():
			if buffData["buff"].getID() == buffID:
				result.append( buffData["index"] )
		return result
	
	def getBuffDataByID( self, buffID ):
		"""
		根据ID获取buffData
		"""
		result = []
		for buffData in self.attrBuffs.values():
			if buffData["buff"].getID() == buffID:
				result.append( buffData )
		return result
	
	def addBuffRemote( self, casterID, buffID ):
		"""
		define method
		远程加buff
		"""
		self.addBuff( casterID, buffID )
	
	def addBuff( self, casterID, buffID ):
		"""
		添加buff最终接口
		"""
		buffIns = self.getBuff( buffID )
		if not buffIns.validCheck( self, casterID ):
			return -1
		
		appendIndex = self.appendBuff( casterID, buffIns )
		if appendIndex != -1:		# append成功
			return appendIndex
		
		index = self.newBuffIndex()
		if index == -1:
			return -1
		
		buffData = buffIns.getNewBuffData( self, casterID )
		buffData["index"] = index
		self.attrBuffs[ index ] = buffData
		buffIns.begin( self, buffData )
		
		return index
	
	def appendBuff( self, casterID, buffIns ):
		"""
		尝试对已有buff进行追加
		只能追加到现有的一个buff上
		"""
		for buffData in self.attrBuffs.values():
			if buffData["buff"].appendCheck( self, buffData, casterID, buffIns ):
				buffData["buff"].doAppend( self, buffData, casterID, buffIns )
				return buffData["index"]
		return -1
	
	def removeBuff( self, buffIndex ):
		"""
		移除buff最终接口
		"""
		buffData = self.attrBuffs.get( buffIndex, None )
		if not buffData:
			return
		buffData["buff"].end( self, buffData )
		self.attrBuffs.pop( buffIndex )
	
	def onBuffLoopTimer( self, timerID ):
		"""
		某个buff的loop timer 到达
		"""
		__buffData = None
		for buffData in self.attrBuffs.values():
			if buffData["loopTimerID"] == timerID:
				__buffData = buffData
				break
		
		if __buffData:
			result = __buffData["buff"].doLoop( self, __buffData )
			if not result:
				self.removeBuff( __buffData["index"] )
	
	def onBuffEndTimer( self, timerID ):
		"""
		某个buff的end timer 到达
		"""
		__buffData = None
		for buffData in self.attrBuffs.values():
			if buffData["endTimerID"] == timerID:
				__buffData = buffData
				break
		
		if __buffData:
			self.removeBuff( __buffData["index"] )
	
	def calculateBuffsOnDestroy( self ):
		"""
		玩家销毁时计算buff数据，针对下线是否保存及继续计时的处理
		"""
		removeList = []
		for buffData in self.attrBuffs.values():
			if buffData["buff"].isSave() :
				if buffData["endTime"] != -1:	#不是无限时间
					buffData["endTime"] = buffData["buff"].calculateOnDestroy( buffData["endTime"] )
					buffData["timeFlag"] = 1	#用来标记endTime是经过计算的
			else :
				removeList.append( buffData["index"] )
		
		for idx in removeList:
			self.removeBuff( idx )
	
	def calculateBuffsOnInit( self ):
		"""
		初始化时重新计算buff数据，针对下线是否保存及继续计时的处理
		"""
		newAttrBuffs = BuffsPacketImpl()
		for buffData in self.attrBuffs.values():
			if not buffData["buff"]:
				continue
			
			if buffData["endTime"] != -1:	#不是无限时间
				if buffData["timeFlag"] == 1:
					buffData["timeFlag"] = 0
					buffData["endTime"] = buffData["buff"].calculateOnInit( buffData["endTime"] )
				
				if buffData["endTime"] <= Functions.getTime():		#超时了就不加了
					continue
			
			buffData["index"] = self.newBuffIndex()
			newAttrBuffs[ buffData["index"] ] = buffData
		
		self.attrBuffs = newAttrBuffs
	
	def reloadBuff( self ):
		"""
		重载buff
		"""
		for buffData in self.attrBuffs.values():
			buffData["buff"].reload( self, buffData )
