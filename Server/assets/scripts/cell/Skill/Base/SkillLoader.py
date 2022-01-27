# -*- coding: utf-8 -*-

import json
import SmartImport
import KBEngine

class SkillLoader:
	_instance = None
	def __init__( self ):
		assert SkillLoader._instance is None
		SkillLoader._instance = self
		self.skills = {}
	
	@staticmethod
	def instance():
		if not SkillLoader._instance:
			SkillLoader._instance = SkillLoader()
		return SkillLoader._instance
	
	def loadSkill( self, filePath ):
		"""
		加载配置
		"""
		absFilePath = KBEngine.getResFullPath(filePath)
		file = open( absFilePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		for data in jsFileData:
			if data["Script"] == "Skill":
				skillClass = SmartImport.smartImport( "Skill.Base.Skill:Skill" )
			else:
				skillClass = SmartImport.smartImport( "Skill.Skill." + data["Script"] + ":" + data["Script"] )
			skillIns = skillClass()
			skillIns.init( data )
			self.skills[ data["id"] ] = skillIns
	
	def getSkill( self, skillID ):
		return self.skills.get( skillID, None )

g_skillLoader = SkillLoader.instance()