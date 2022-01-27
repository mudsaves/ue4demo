# -*- coding: utf-8 -*-

import csdefine
import csstatus
import SmartImport
import Skill.Base.ReceiverPicker as ReceiverPicker
import Skill.Base.CasterCondition as CasterCondition
import Skill.Base.TargetCondition as TargetCondition
import Skill.PassiveSkill.EventCondition as EventCondition
from KBEDebug import *

class EventAction:
	"""
	一个事件行为
	"""
	def __init__( self ):
		self.skillIns = None
		self.receiverPicker = None
		self.receiverConditions = []
		self.normalEffects = []
		self.eventEffects = []
	
	def init( self, skillIns, configData ):
		"""
		"""
		self.skillIns = skillIns
		self.receiverPicker = ReceiverPicker.newInstance( configData["receiverPicker"]["Script"] )
		self.receiverPicker.init( configData["receiverPicker"] )
		
		for conDict in configData["receiverCondition"]:
			conIns = TargetCondition.newInstance( conDict["Script"] )
			conIns.init( conDict )
			self.receiverConditions.append( conIns )
		
		for effectDict in configData["normalEffects"]:
			effectCls = SmartImport.smartImport( "Skill.Effect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_SKILL )
			effectIns.setSourceParam( skillIns.getID() )
			self.normalEffects.append( effectIns )
		
		for effectDict in configData["eventEffects"]:
			effectCls = SmartImport.smartImport( "Skill.PassiveSkill.EventEffect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			if skillIns.linkEvent not in effectIns.getLinkEvent():
				ERROR_MSG("Passive skill event effect not match! skillID:%s script:%s."%(skillIns.getID(), effectDict["Script"]))
				continue
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_SKILL )
			effectIns.setSourceParam( skillIns.getID() )
			self.eventEffects.append( effectIns )
	
	def checkReceiver( self, caster, receiver ):
		"""
		检查受术者是否满足条件
		"""
		for conObj in self.receiverConditions:
			if conObj.check( caster, receiver ) != csstatus.SKILL_GO_ON:
				return False
		return True
	
	def getReceiver( self, caster, target ):
		"""
		获取受术者
		"""
		receiverList = self.receiverPicker.pickReceivers( caster, target, [] )
		
		result = []
		for receiver in receiverList:
			if not self.checkReceiver( caster, receiver ):
				continue
			result.append( receiver )
		return result
	
	def do( self, caster, target, eventParam ):
		"""
		"""
		receiverList = self.getReceiver( caster, target )
		for e in receiverList:
			for effect in self.normalEffects:		#执行普通效果
				if not effect.check( caster, e ):
					continue
				effect.receive( caster, e )
			
			for effect in self.eventEffects:		#执行事件相关效果
				if not effect.check( caster, e, eventParam ):
					continue
				effect.receive( caster, e, eventParam )


class EventHit:
	"""
	事件的一种情况
	"""
	def __init__( self ):
		self.skillIns = None
		self.casterCondition = []
		self.targetCondition = []
		self.eventCondition = []
		self.actions = []
	
	def init( self, skillIns, configData ):
		"""
		"""
		self.skillIns = skillIns
		for conDict in configData["casterCondition"]:
			conIns = CasterCondition.newInstance( conDict["Script"] )
			conIns.init( conDict )
			self.casterCondition.append( conIns )
		
		for conDict in configData["targetCondition"]:
			conIns = TargetCondition.newInstance( conDict["Script"] )
			conIns.init( conDict )
			self.targetCondition.append( conIns )
		
		for conDict in configData["eventCondition"]:
			conIns = EventCondition.newInstance( conDict["Script"] )
			if skillIns.linkEvent not in conIns.getLinkEvent():
				ERROR_MSG("Passive skill event condition not match! skillID:%s, script:%s."%(skillIns.getID(), conDict["Script"]))
				continue
			conIns.init( conDict )
			self.eventCondition.append( conIns )
		
		for actDict in configData["actions"]:
			actIns = EventAction()
			actIns.init( skillIns, actDict )
			self.actions.append( actIns )

	def checkCasterCondition( self, caster ):
		"""
		检测施法者条件
		"""
		for con in self.casterCondition:
			if con.check( caster ) != csstatus.SKILL_GO_ON:
				return False
		return True

	def checkTargetCondition( self, caster, target ):
		"""
		检测施法目标条件
		"""
		for con in self.targetCondition:
			if con.check( caster, target ) != csstatus.SKILL_GO_ON:
				return False
		return True

	def checkEventCondition( self, caster, target, eventParams ):
		"""
		检测事件条件
		"""
		for con in self.eventCondition:
			if not con.check( caster, target, eventParams ):
				return False
		return True
	
	def checkCondition( self, caster, target, eventParams ):
		"""
		检测条件
		"""
		casterResult = self.checkCasterCondition( caster )
		targetResult = self.checkTargetCondition( caster, target )
		eventResult = self.checkEventCondition( caster, target, eventParams )
		return casterResult and targetResult and eventResult
	
	def doAction( self, caster, target, eventParams ):
		"""
		执行行为
		"""
		for action in self.actions:
			action.do( caster, target, eventParams )


class PassiveSkill:
	"""
	被动技能
	"""
	def __init__( self ):
		self.id = 0
		self.name = ""
		self.targetType = csdefine.SKILL_TARGET_NONE
		self.holdEffects = []
		self.linkEvent = 0
		self.eventHitList = []
	
	def init( self, configData ):
		self.id = configData["id"]
		self.name = configData["name"]
		self.targetType = getattr( csdefine, configData["targetType"] )
		
		for effectDict in configData["holdEffects"]:
			effectCls = SmartImport.smartImport( "Skill.HoldEffect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_SKILL )
			effectIns.setSourceParam( self.id )
			self.holdEffects.append( effectIns )
		
		self.linkEvent = getattr( csdefine, configData["linkEvent"] )
		
		for hitDict in configData["eventHitList"]:
			hitIns = EventHit()
			hitIns.init( self, hitDict )
			self.eventHitList.append( hitIns )
	
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
		return True
	
	def onAttach( self, entity ):
		"""
		被添加
		"""
		entity.addListenSkillEvent( self.linkEvent, self.id )
		
		dataList = []
		for index, effect in enumerate(self.holdEffects):
			if not effect.check( entity, entity ):
				continue
			effectData = effect.newHoldEffectData( entity, entity )
			effectData.index = index
			effectData.casterID = entity.id
			effect.begin( entity, effectData )
			dataList.append( effectData )
		
		if len(dataList) != 0:
			entity.passiveSkillEffectDatas[self.id] = dataList
	
	def onDetach( self, entity ):
		"""
		被移除
		"""
		entity.removeListenSkillEvent( self.linkEvent, self.id )
		
		if self.id not in entity.passiveSkillEffectDatas:
			return
		
		for data in entity.passiveSkillEffectDatas[self.id]:
			effect = self.holdEffects[data.index]
			effect.end( entity, data )
		
		entity.passiveSkillEffectDatas.pop( self.id )
	
	def use( self, entity, target, eventParams ):
		"""
		@param entity: 被动技能拥有者
		@type entity: real entity
		@param target: 技能施展目标
		@type target: SkillTargetObjEntity
		@param eventType: 事件类型
		@type eventType: csdefine中枚举值
		@param eventParams: 事件相关参数
		@type eventParams: dict
		"""
		for hit in self.eventHitList:
			if hit.checkCondition( entity, target, eventParams ):
				hit.doAction( entity, target, eventParams )