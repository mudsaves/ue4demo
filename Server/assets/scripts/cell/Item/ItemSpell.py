# -*- coding: utf-8 -*-

import csdefine
import csstatus
from KBEDebug import *
from Item.Base.ItemBase import ItemBase

class ItemSpell( ItemBase ):
	"""
	技能物品
	"""
	def __init__( self ):
		ItemBase.__init__( self )
		self.skillID = 0
	
	def init( self, itemID, cfgDict ):
		"""
		读取配置数据
		"""
		ItemBase.init( self, itemID, cfgDict )
		self.skillID = cfgDict["skillID"]
	
	def use( self, owner, targetObj ):
		"""
		virtual method
		使用接口
		"""
		if self.skillID == 0:
			ERROR_MSG("Item skillID is None. itemID:%s."%self.getID())
			return
		
		if targetObj.getType() != csdefine.SKILL_TARGET_OBJECT_ENTITY:
			ERROR_MSG("Item use target type error. itemID:%s."%self.getID())
			return
		
		target = targetObj.getObject()
		if not target:
			DEBUG_MSG("Item use lose target. itemID:%s, ownerID:%s."%(self.getID(), owner.id))
			return
		
		status = owner.useSkill( self.skillID, target.id )
		if status != csstatus.SKILL_GO_ON:
			return
		
		owner.spellingItem = self
		self.onUse( owner )
	
	def onSkillCastOver( self, owner, skillID ):
		"""
		技能释放完毕
		"""
		if skillID != self.skillID:	#加个验证，因为以后可能允许同时放多个技能
			return
		owner.spellingItem = None
		
		if self.removeMomentType == csdefine.ITEM_REM_MOMENT_SKILL_OVER:
			owner.removeItemByOrder( self.order, 1, csdefine.DELETE_ITEM_USE )
	
	def onSkillInterrupted( self, owner, skillID ):
		"""
		技能被打断
		"""
		if skillID != self.skillID:	#加个验证，因为以后可能允许同时放多个技能
			return
		owner.spellingItem = None