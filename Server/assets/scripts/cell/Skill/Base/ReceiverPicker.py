# -*- coding: utf-8 -*-

import csdefine
import SkillTargetObjImpl
import random

class ReceiverPickerBase:
	"""
	受术者获取类，基类
	"""
	def init( self, params ):
		"""
		virtual method.
		"""
		pass
	
	def pickReceivers( self, caster, target, lastSuccessReceiver ):
		"""
		virtual method.
		获取受术者
		
		@param caster: 施法者
		@type caster: realEntity
		@param target: 技能施展目标
		@type target: SkillTargetObjEntity 或 SkillTargetObjPosition
		@param lastSuccessReceiver: 上个技能任务的受术者
		@type lastSuccessReceiver: 列表，元素为打包了的受术者
		"""
		return []

class ReceiverPickerCaster( ReceiverPickerBase ):
	"""
	取施法者为受术者
	"""
	def pickReceivers( self, caster, target, lastSuccessReceiver ):
		"""
		"""
		obj = SkillTargetObjImpl.createEntityTargetObj( caster )
		return [ obj ]

class ReceiverPickerTarget( ReceiverPickerBase ):
	"""
	取施法对象为受术者
	"""
	def pickReceivers( self, caster, target, lastSuccessReceiver ):
		"""
		"""
		return [ target ]

class ReceiverPickerLastReceiver( ReceiverPickerBase ):
	"""
	上一个技能任务的受术者
	"""
	def pickReceivers( self, caster, target, lastSuccessReceiver ):
		"""
		"""
		result = []
		for receiverObj in lastSuccessReceiver:
			if receiverObj.getType() == csdefine.SKILL_TARGET_OBJECT_ENTITY and receiverObj.getObject() == None:
				pass
			else:
				result.append( receiverObj )
		return result

class ReceiverPickerCycleEntity( ReceiverPickerBase ):
	"""
	圆形内的所有Account
	"""
	def init( self, params ):
		"""
		"""
		self.radius = float(params["param1"])
	
	def pickReceivers( self, caster, target, lastSuccessReceiver ):
		"""
		"""
		receiverList = []
		entities = caster.entitiesInRange( self.radius )
		for e in entities:
			if e.__class__.__name__ not in [ "Account", "Monster" ]:
				continue
			obj = SkillTargetObjImpl.createEntityTargetObj( e )
			receiverList.append( obj )
		return receiverList

class ReceiverPickerCasterCyclePos( ReceiverPickerBase ):
	"""
	施法者位置附近随机取N个位置
	"""
	def init( self, params ):
		"""
		"""
		self.radius = float(params["param1"])
		self.posAmount = int(params["param2"])
	
	def pickReceivers( self, caster, target, lastSuccessReceiver ):
		"""
		"""
		receiverList = []
		for i in range(self.posAmount):
			x = random.randint( 0, self.radius )
			z = random.randint( 0, self.radius )
			position = (caster.position.x+x, caster.position.y, caster.position.z+z)
			obj = SkillTargetObjImpl.createPositionTargetObj( position )
			receiverList.append( obj )
		return receiverList

class ReceiverPickerCyclePos( ReceiverPickerBase ):
	"""
	目标位置附近随机取N个位置
	"""
	def init( self, params ):
		"""
		"""
		self.radius = float(params["param1"])
		self.posAmount = int(params["param2"])
	
	def pickReceivers( self, caster, target, lastSuccessReceiver ):
		"""
		"""
		receiverList = []
		for i in range(self.posAmount):
			x = random.randint( 0, self.radius )
			z = random.randint( 0, self.radius )
			position = (target.getObjectPosition().x+x, target.getObjectPosition().y, target.getObjectPosition().z+z)
			obj = SkillTargetObjImpl.createPositionTargetObj( position )
			receiverList.append( obj )
		return receiverList


g_objects = {	"ReceiverPickerCaster": ReceiverPickerCaster,
				"ReceiverPickerTarget": ReceiverPickerTarget,
				"ReceiverPickerLastReceiver": ReceiverPickerLastReceiver,
				"ReceiverPickerCycleEntity": ReceiverPickerCycleEntity,
				"ReceiverPickerCasterCyclePos": ReceiverPickerCasterCyclePos,
				"ReceiverPickerCyclePos": ReceiverPickerCyclePos,
			}

def newInstance( clsName ):
	return g_objects.get( clsName )()