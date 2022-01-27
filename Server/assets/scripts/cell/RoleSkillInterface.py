# -*- coding: utf-8 -*-

import csdefine
import KBEngine
import Functions
from KBEDebug import *
from SkillInterface import SkillInterface

class RoleSkillInterface( SkillInterface ):
	"""
	玩家技能接口
	"""
	def __init__( self ):
		SkillInterface.__init__( self )
		#self.skillList = []		#主动技能列表
	
	def gainSkill( self, skillID ):
		"""
		获得某技能
		"""
		skill = self.getSkill( skillID )
		if skill.isPassive():
			self.gainPassiveSkill( skillID )
		else:
			if skillID not in self.skillList:
				self.skillList.append( skillID )
	
	def forgetSkill( self, skillID ):
		"""
		忘记某技能
		"""
		if skillID in self.passiveSkillList:
			self.removePassiveSkill( skillID )
		elif skillID in self.skillList:
			self.skillList.remove( skillID )
	
	def onSkillCastOver( self, skillID ):
		"""
		virtual method
		技能释放完毕
		"""
		self.item_onSkillCastOver( skillID )
	
	def onSkillInterrupted( self, skillID ):
		"""
		virtual method
		技能被打断
		"""
		self.item_onSkillInterrupted( skillID )