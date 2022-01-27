# -*- coding: utf-8 -*-

import json
import SmartImport
import KBEngine

class PassiveSkillLoader:
	_instance = None
	def __init__( self ):
		assert PassiveSkillLoader._instance is None
		PassiveSkillLoader._instance = self
		self.skills = {}
	
	@staticmethod
	def instance():
		if not PassiveSkillLoader._instance:
			PassiveSkillLoader._instance = PassiveSkillLoader()
		return PassiveSkillLoader._instance
	
	def loadSkill( self, filePath ):
		"""
		加载配置
		"""
		absFilePath = KBEngine.getResFullPath(filePath)
		file = open( absFilePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		for data in jsFileData:
			skillClass = SmartImport.smartImport( "Skill.PassiveSkill." + data["Script"] + ":" + data["Script"] )
			skillIns = skillClass()
			skillIns.init( data )
			self.skills[ data["id"] ] = skillIns
	
	def getSkill( self, skillID ):
		return self.skills.get( skillID, None )

g_passiveSkillLoader = PassiveSkillLoader.instance()