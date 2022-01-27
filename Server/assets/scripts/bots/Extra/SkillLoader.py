# -*- coding: utf-8 -*-

import json

class SkillLoader:
	"""
	"""
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
		file = open( filePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		for data in jsFileData:
			self.skills[data["id"]] = data
	
	def getSkill( self, skillID ):
		"""
		"""
		return self.skills.get( skillID, {} )
	
	def getSkillCfg( self, skillID, attrName, defaultValue ):
		"""
		"""
		if skillID in self.skills:
			return self.skills[skillID].get( attrName, defaultValue )
		return defaultValue


g_skillLoader = SkillLoader()