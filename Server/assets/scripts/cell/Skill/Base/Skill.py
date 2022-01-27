# -*- coding: utf-8 -*-

import csdefine
import csconst
import csstatus
import Functions
import SmartImport
import Skill.Base.Cost as Cost
import Skill.Base.CasterCondition as CasterCondition
import Skill.Base.TargetCondition as TargetCondition
from Skill.Base.SkillTask import SkillTask
from KBEDebug import *

class Skill:
	"""
	技能类
	"""
	def __init__( self ):
		self.id = 0
		self.name = ""
		self.minDis = -1
		self.maxDix = -1
		self.targetType = csdefine.SKILL_TARGET_NONE
		self.interruptCodeList = [csdefine.SKILL_INTERRUPT_CODE_DIE]		#默认死亡打断一切技能
		self.cooldownList = []
		self.holdEffects = []
		self.useCostList = []
		self.useSuccessCostList = []
		self.casterConList = []
		self.targetConList = []
		self.tasks = []
	
	def init( self, dataDict ):
		"""
		"""
		self.id = dataDict["id"]
		self.name = dataDict["name"]
		self.minDis = dataDict["minDis"]
		self.maxDis = dataDict["maxDis"]
		self.targetType = getattr( csdefine, dataDict["targetType"] )
		self.interruptCodeList.extend( dataDict["interruptCode"] )
		for cooldownList in dataDict["cooldown"]:
			self.cooldownList.append( (cooldownList["cooldownId"], cooldownList["cooldownTime"]) )
		
		for costDict in dataDict["useCost"]:
			costIns = Cost.newInstance( costDict["Script"] )
			costIns.init( costDict )
			self.useCostList.append( costIns )
		
		for costDict in dataDict["useSuccessCost"]:
			costIns = Cost.newInstance( costDict["Script"] )
			costIns.init( costDict )
			self.useSuccessCostList.append( costIns )
		
		for conDict in dataDict["casterCondition"]:
			conIns = CasterCondition.newInstance( conDict["Script"] )
			conIns.init( conDict )
			self.casterConList.append( conIns )
		
		for conDict in dataDict["targetCondition"]:
			conIns = TargetCondition.newInstance( conDict["Script"] )
			conIns.init( conDict )
			self.targetConList.append( conIns )
		
		for effectDict in dataDict["holdEffects"]:
			effectCls = SmartImport.smartImport( "Skill.HoldEffect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_SKILL )
			effectIns.setSourceParam( self.id )
			self.holdEffects.append( effectIns )
		
		for taskDict in dataDict["tasks"]:
			taskIns = SkillTask()
			taskIns.init( self, taskDict )
			taskIns.index = len( self.tasks )
			self.tasks.append( taskIns )
	
	def getID( self ):
		"""
		获取技能ID
		"""
		return self.id
	
	def getTargetType( self ):
		"""
		获取技能施法对象类型
		"""
		return self.targetType
	
	def isPassive( self ):
		"""
		virtual method
		是不是被动技能
		"""
		return False
	
	def useCheck( self, caster, target ):
		"""
		检测释放条件
		
		@param caster: 施法者
		@type caster: realEntity
		@param target: 技能施展对象
		@type target: SkillTargetObjEntity 或 SkillTargetObjPosition
		"""
		if self.isCooldown( caster ):
			return csstatus.SKILL_IN_CD
		
		status = self.checkDistance( caster, target )
		if  status!= csstatus.SKILL_GO_ON:
			return status
		
		status = self.checkCasterCondition( caster )
		if status != csstatus.SKILL_GO_ON:
			return status
		
		status = self.checkTargetCondition( caster, target )
		if status != csstatus.SKILL_GO_ON:
			return status
		
		return csstatus.SKILL_GO_ON

	def isCooldown( self, caster ):
		"""
		技能是否在冷却
		"""
		for id, time in self.cooldownList:
			for cdID, cdData in caster.getCooldown().items():
				if id == cdID and ( cdData["endTime"] - Functions.getTime() > 0.01 * csconst.TIME_ENLARGE_MULTIPLE ):	#允许有0.01的误差
					return True
		return False

	def checkDistance( self, caster, target ):
		"""
		检测施法对象是否在施法范围内
		
		@param caster: 施法者
		@type caster: realEntity
		@param target: 技能施展对象
		@type target: SkillTargetObjEntity 或 SkillTargetObjPosition
		"""
		if self.minDis >= 0 and caster.position.distTo( target.getObjectPosition() ) < self.minDis:
			return csstatus.SKILL_TOO_NEAR
		if self.maxDis >= 0 and caster.position.distTo( target.getObjectPosition() ) > self.maxDis:
			return csstatus.SKILL_TOO_FAR
		return csstatus.SKILL_GO_ON

	def checkCasterCondition( self, caster ):
		"""
		检测施法者条件
		"""
		for con in self.casterConList:
			status = con.check( caster )
			if status != csstatus.SKILL_GO_ON:
				return status
		return csstatus.SKILL_GO_ON

	def checkTargetCondition( self, caster, target ):
		"""
		检测施法目标条件
		"""
		for con in self.targetConList:
			status = con.check( caster, target )
			if status != csstatus.SKILL_GO_ON:
				return status
		return csstatus.SKILL_GO_ON

	def handleUseCost( self, caster ):
		"""
		一旦释放就要消耗的东西
		"""
		for costIns in self.useCostList:
			costIns.do( caster )

	def handleUseSuccessCost( self, caster ):
		"""
		整个技能释放成功才消耗的东西
		"""
		for costIns in self.useSuccessCostList:
			costIns.do( caster )

	def use( self, caster, target ):
		"""
		释放技能
		
		@param caster: 施法者
		@type caster: realEntity
		@param target: 技能施展对象
		@type target: SkillTargetObjEntity 或 SkillTargetObjPosition
		"""
		if len(self.tasks) == 0:		#为了保证流程正确，不允许不配task，况且没有task的技能是没有意义的
			return csstatus.SKILL_STATUS_SYS_ERR
		
		status = self.useCheck( caster, target )
		if status != csstatus.SKILL_GO_ON:
			DEBUG_MSG("Use skill(%s) failure, status(%s)."%(self.id, status))
			return status
		
		self.handleUseCost( caster )	#处理消耗
		caster.addCooldown( self.cooldownList )
		self.beginTask( caster, target )
		return csstatus.SKILL_GO_ON
	
	def beginTask( self, caster, target ):
		"""
		开始执行任务：按顺序执行多个任务
		任务配置持续时间，时间结束才执行下个任务
		"""
		caster.castingSkill = self.id
		
		# 施法者添加持有效果
		for index, effect in enumerate(self.holdEffects):
			if not effect.check( caster, caster ):
				continue
			effectData = effect.newHoldEffectData(caster, caster)
			effectData.index = index
			effectData.casterID = caster.id
			effect.begin( caster, effectData )
			caster.skillEffectDatas.append( effectData )
		
		self.tasks[0].begin( caster, target, [] )

	def onTaskTimeEnd( self, taskIndex, caster, target, successReceiver ):
		"""
		一个任务执行时间到达
		"""
		self.tasks[taskIndex].end( caster )
		if len(self.tasks) == taskIndex+1:					# 所有任务执行完毕
			self.onTasksAllEnd( caster )
		else:
			self.tasks[taskIndex+1].begin( caster, target, successReceiver )	# 否则，开始执行下一个任务

	def onTasksAllEnd( self, caster ):
		"""
		所有任务执行完毕
		"""
		self.handleUseSuccessCost( caster )	# 处理消耗
		
		# 移除施法者持有效果
		for data in caster.skillEffectDatas:
			effect = self.holdEffects[data.index]
			effect.end( caster, data )
		caster.skillEffectDatas = []
		
		caster.castingSkill = 0
		caster.onSkillCastOver( self.id )

	def canInterrupt( self, interruptReason ):
		"""
		技能是否可以被打断
		"""
		return interruptReason in self.interruptCodeList

	def onInterrupt( self, caster, interruptReason ):
		"""
		技能被打断
		"""
		# 移除施法者任务持有效果
		if caster.skillTaskTimerID != 0:
			caster.delTimer( caster.skillTaskTimerID )
			caster.skillTaskTimerID = 0
			taskIndex = caster.skillTaskTimerParam["taskIndex"]
			self.tasks[taskIndex].end( caster )
		
		# 移除施法者持有效果
		for data in caster.skillEffectDatas:
			effect = self.holdEffects[data.index]
			effect.end( caster, data )
		caster.skillEffectDatas = []
		
		caster.castingSkill = 0
		caster.onSkillInterrupted( self.id )
