# -*- coding: utf-8 -*-

import csdefine
import csstatus
import SmartImport
import Skill.Base.ReceiverPicker as ReceiverPicker
import Skill.Base.TargetCondition as TargetCondition

class SkillTask:
	"""
	技能任务类
	"""
	def __init__( self ):
		self.skillIns = None
		self.persistentTime = 0.0
		self.receiverPicker = None
		self.receiverConditions = []
		self.receiverEffects = []
		self.holdEffects = []
	
	def init( self, skillIns, dict ):
		"""
		"""
		self.skillIns = skillIns
		self.persistentTime = dict["persistentTime"]
		
		self.receiverPicker = ReceiverPicker.newInstance( dict["receiverPicker"]["Script"] )
		self.receiverPicker.init( dict["receiverPicker"] )
		
		for conDict in dict["receiverCondition"]:
			conIns = TargetCondition.newInstance( conDict["Script"] )
			conIns.init( conDict )
			self.receiverConditions.append( conIns )
		
		for effectDict in dict["receiverEffects"]:
			effectCls = SmartImport.smartImport( "Skill.Effect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_SKILL )
			effectIns.setSourceParam( skillIns.getID() )
			self.receiverEffects.append( effectIns )
		
		for effectDict in dict["holdEffects"]:
			effectCls = SmartImport.smartImport( "Skill.HoldEffect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_SKILL )
			effectIns.setSourceParam( skillIns.getID() )
			self.holdEffects.append( effectIns )
	
	def getPersistentTime( self ):
		"""
		获取任务持续时间
		"""
		return self.persistentTime
	
	def checkReceiver( self, caster, receiver ):
		"""
		检查受术者是否满足条件
		"""
		for conObj in self.receiverConditions:
			if conObj.check( caster, receiver ) != csstatus.SKILL_GO_ON:
				return False
		return True
	
	def getReceiver( self, caster, target, lastSuccessReceiver ):
		"""
		获取受术者
		"""
		receiverList = self.receiverPicker.pickReceivers( caster, target, lastSuccessReceiver )
		
		result = []
		for receiver in receiverList:
			if not self.checkReceiver( caster, receiver ):
				continue
			result.append( receiver )
		return result
	
	def begin( self, caster, target, lastSuccessReceiver ):
		"""
		开始执行任务
		"""
		# 施法者添加任务持有效果
		for index, effect in enumerate(self.holdEffects):
			if not effect.check( caster, caster ):
				continue
			effectData = effect.newHoldEffectData(caster, caster)
			effectData.index = index
			effectData.casterID = caster.id
			effect.begin( caster, effectData )
			caster.skillTaskEffectDatas.append( effectData )
		
		# 受术者添加效果
		successReceiver = []
		receiverList = self.getReceiver( caster, target, lastSuccessReceiver )
		for e in receiverList:
			for effect in self.receiverEffects:
				if not effect.check( caster, e ):
					continue
				effect.receive( caster, e )	# 对受术者使用的效果，发出去就不管了，因此不需要结束，用receive接口
				successReceiver.append(e)
		
		if self.persistentTime == 0:
			self.skillIns.onTaskTimeEnd( self.index, caster, target, successReceiver )
		else:
			caster.skillTaskTimerParam["skillID"] = self.skillIns.getID()
			caster.skillTaskTimerParam["taskIndex"] = self.index
			caster.skillTaskTimerParam["target"] = target
			caster.skillTaskTimerParam["successReceiver"] = successReceiver
			caster.skillTaskTimerID = caster.addTimer( self.persistentTime, 0.0, 0 )
	
	def end( self, caster ):
		"""
		结束任务
		"""
		# 移除施法者持有效果
		for data in caster.skillTaskEffectDatas:
			effect = self.holdEffects[data.index]
			effect.end( caster, data )
		caster.skillTaskEffectDatas = []
