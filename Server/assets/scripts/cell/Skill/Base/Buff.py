# -*- coding: utf-8 -*-

import csdefine
import Functions
import SmartImport
import SkillTargetObjImpl

class Buff:
	"""
	buff基类
	"""
	def __init__( self ):
		self.id = 0
		self.name = ""
		self._persistTime = 0	#持有时间：等于0 buff无效，小于0 持有无限时间
		self._loopTime = 0
		self._alwayCalc = False
		self._isSave = False
		self.holdEffects = []
		self.loopEffects = []
	
	def init( self, dataDict ):
		"""
		"""
		self.id = dataDict["id"]
		self.name = dataDict["name"]
		self._persistTime = dataDict["persistTime"]
		self._loopTime = dataDict["loopTime"]
		self._alwayCalc = dataDict["alwayCalc"]
		self._isSave = dataDict["save"]
		
		for effectDict in dataDict["holdEffects"]:
			effectCls = SmartImport.smartImport( "Skill.HoldEffect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_BUFF )
			effectIns.setSourceParam( self.id )
			self.holdEffects.append( effectIns )
		
		for effectDict in dataDict["loopEffects"]:
			effectCls = SmartImport.smartImport( "Skill.Effect." + effectDict["Script"] + ":" + effectDict["Script"] )
			effectIns = effectCls()
			effectIns.init( effectDict )
			effectIns.setSourceType( csdefine.EFFECT_SOURCE_BUFF )
			effectIns.setSourceParam( self.id )
			self.loopEffects.append( effectIns )
	
	def getID( self ):
		return self.id
	
	def getPersistTime( self ):
		return self._persistTime
	
	def isSave( self ):
		return self._isSave
	
	def getNewObj( self ):
		"""
		返回一个自身的拷贝
		"""
		obj = self.__class__()
		obj.__dict__.update( self.__dict__ )
		return obj
	
	def getNewBuffData( self, receiver, casterID ):
		"""
		创建一个buffData字典
		"""
		buffData = {}
		buffData["buff"] = self.getNewObj()
		buffData["casterID"] = casterID
		buffData["endTime"] = 0
		buffData["timeFlag"] = 0
		buffData["endTimerID"] = 0
		buffData["loopTimerID"] = 0
		return buffData
	
	def validCheck( self, receiver, casterID ):
		"""
		virtual method.
		是否可以添加
		
		@param receiver: buff持有者
		@type receiver: realEntity
		@param casterID: 施法者ID
		@type casterID: int32
		"""
		if self._persistTime == 0:
			return False
		return True
	
	def appendCheck( self, receiver, buffData, casterID, newBuffIns ):
		"""
		virtual method.
		是否可以追加
		
		@param receiver: buff持有者
		@type receiver: realEntity
		@param buffData: 原buff的buffData
		@type buffData: BUFF_DATA
		@param casterID: 新buff的施法者ID
		@type casterID: int32
		@param newBuffIns: 新buff实例
		@type newBuffIns: Buff
		"""
		if self.id != newBuffIns.getID():		#暂定相同ID才能叠加
			return False
		return True
	
	def doAppend( self, receiver, buffData, casterID, newBuffIns ):
		"""
		已经存在相同ID的BUFF，则进行追加操作
		
		@param receiver: buff持有者
		@type receiver: realEntity
		@param buffData: 原buff的buffData
		@type buffData: BUFF_DATA
		@param casterID: 新buff的施法者ID
		@type casterID: int32
		@param newBuffIns: 新buff实例
		@type newBuffIns: Buff
		"""
		#时间叠加
		if buffData["endTime"] == -1:				#原buff是无限时间，什么都不做
			pass
		elif newBuffIns.getPersistTime() < 0:		#新buff是无限时间，原buff改成无限时间
			receiver.delTimer( buffData["endTimerID"] )
			buffData["endTimerID"] = 0
			buffData["endTime"] = -1
		else:										#否则，原buff时间延长
			remainTime = Functions.getFloatTime( buffData["endTime"] - Functions.getTime() )
			remainTime += newBuffIns.getPersistTime()
			buffData["endTime"] = Functions.getTime( remainTime )
			receiver.delTimer( buffData["endTimerID"] )
			buffData["endTimerID"] = receiver.addTimer( remainTime, 0, csdefine.BUFF_END_TIMER )
	
	def begin( self, receiver, buffData ):
		"""
		virtual method.
		buff开始
		
		@param receiver: buff持有者
		@type receiver: realEntity
		@param buffData: 原buff的buffData
		@type buffData: BUFF_DATA
		"""
		if self._persistTime < 0:	#无限时间
			buffData["endTime"] = -1
		else:
			buffData["endTime"] = Functions.getTime( self._persistTime )
			buffData["endTimerID"] = receiver.addTimer( self._persistTime, 0, csdefine.BUFF_END_TIMER )
		
		if self._loopTime > 0:
			buffData["loopTimerID"] = receiver.addTimer( self._loopTime, self._loopTime, csdefine.BUFF_LOOP_TIMER )
		
		for index, effect in enumerate(self.holdEffects):
			if not effect.check( receiver, receiver ):
				continue
			effectData = effect.newHoldEffectData(receiver, receiver)
			effectData.index = index
			effectData.casterID = buffData["casterID"]
			effect.begin( receiver, effectData )
			
			if buffData["index"] not in receiver.buffEffectDatas:
				receiver.buffEffectDatas[ buffData["index"] ] = [ effectData ]
			else:
				receiver.buffEffectDatas[ buffData["index"] ].append( effectData )
	
	def reload( self, receiver, buffData ):
		"""
		virtual method.
		buff上线重载
		
		@param receiver: buff持有者
		@type receiver: realEntity
		@param buffData: 原buff的buffData
		@type buffData: BUFF_DATA
		"""
		if buffData["endTime"] != -1:	#不是无限时间
			remainTime = Functions.getFloatTime( buffData["endTime"] - Functions.getTime() )
			buffData["endTimerID"] = receiver.addTimer( remainTime, 0, csdefine.BUFF_END_TIMER )
		
		if self._loopTime > 0:
			buffData["loopTimerID"] = receiver.addTimer( self._loopTime, self._loopTime, csdefine.BUFF_LOOP_TIMER )
		
		for index, effect in enumerate(self.holdEffects):
			effectData = effect.newHoldEffectData(receiver, receiver)
			effectData.index = index
			effectData.casterID = buffData["casterID"]
			effect.begin( receiver, effectData )
			
			if buffData["index"] not in receiver.buffEffectDatas:
				receiver.buffEffectDatas[ buffData["index"] ] = [ effectData ]
			else:
				receiver.buffEffectDatas[ buffData["index"] ].append( effectData )
	
	def doLoop( self, receiver, buffData ):
		"""
		virtual method.
		buff循环执行
		
		@param receiver: buff持有者
		@type receiver: realEntity
		@param buffData: 原buff的buffData
		@type buffData: BUFF_DATA
		"""
		receiverObj = SkillTargetObjImpl.createEntityTargetObj( receiver )
		for effect in self.loopEffects:
			if not effect.check( receiver, receiverObj ):
				continue
			effect.receive( receiver, receiverObj )
		
		return True
	
	def end( self, receiver, buffData ):
		"""
		virtual method.
		buff结束
		
		@param receiver: buff持有者
		@type receiver: realEntity
		@param buffData: 原buff的buffData
		@type buffData: BUFF_DATA
		"""
		if buffData["endTimerID"] != 0:
			receiver.delTimer( buffData["endTimerID"] )
			buffData["endTimerID"] = 0
		if buffData["loopTimerID"] != 0:
			receiver.delTimer( buffData["loopTimerID"] )
			buffData["loopTimerID"] = 0
		
		for data in receiver.buffEffectDatas.get( buffData["index"], [] ):
			effect = self.holdEffects[data.index]
			effect.end( receiver, data )
		
		receiver.buffEffectDatas.pop( buffData["index"], [] )
	
	def calculateOnDestroy( self, timeVal ):
		"""
		销毁时计算buff时间
		"""
		if not self._alwayCalc :
			# 下线后不计时，需要将值处理成剩余时间
			timeVal -= Functions.getTime()
		return timeVal
	
	def calculateOnInit( self, timeVal ):
		"""
		初始化时重新计算buff时间
		"""
		if not self._alwayCalc:
			# 下线后不计时，需要将剩余时间重新处理成buff时间
			timeVal += Functions.getTime()
		return timeVal
	
	def addToDict( self ):
		"""
		virtual method.
		打包自身需要传输的数据，数据必须是一个dict，具体参数详看BuffTypeImpl；
		此接口默认返回：{ "param": None }，即表示无动态数据。
		"""
		return { "param": None }
	
	def createFromDict( self, dict ):
		"""
		virtual method.
		根据给定的字典数据创建一个与自身相同id号的Buff。详细字典数据格式请参数BuffTypeImpl
		"""
		obj = self.__class__()
		obj.__dict__.update( self.__dict__ )
		return obj