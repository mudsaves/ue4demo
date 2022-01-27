# -*- coding: utf-8 -*-

import csdefine
import csstatus

class TargetConditionBase:
	def init( self, params ):
		pass
	
	def check( self, caster, target ):
		"""
		检查技能施展目标或技能受术者是否满足条件
		
		@param caster: 施法者
		@type caster: realEntity
		@param target: 技能施展目标或者受术者
		@type target: SkillTargetObjEntity 或 SkillTargetObjPosition
		"""
		return csstatus.SKILL_GO_ON

class TargetConditionDead( TargetConditionBase ):
	def check( self, caster, target ):
		if target.getType() != csdefine.SKILL_TARGET_OBJECT_ENTITY:
			return csstatus.SKILL_TARGET_TYPE_ERR
		if target.getObject().state != csdefine.STATE_DEAD:
			return csstatus.SKILL_TARGET_IS_NOT_DEAD
		return csstatus.SKILL_GO_ON

class TargetConditionCanAttack( TargetConditionBase ):
	def check( self, caster, target ):
		if target.getType() != csdefine.SKILL_TARGET_OBJECT_ENTITY:
			return csstatus.SKILL_TARGET_TYPE_ERR
		if not caster.canAttack( target.getObject() ):
			return csstatus.SKILL_TARGET_TYPE_ERR
		return csstatus.SKILL_GO_ON


g_objects = {	"TargetConditionDead": TargetConditionDead,
				"TargetConditionCanAttack": TargetConditionCanAttack,
			}

def newInstance( clsName ):
	return g_objects.get( clsName )()