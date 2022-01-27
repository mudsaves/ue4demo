# -*- coding: utf-8 -*-

import json
from Skill.Base.Cooldown import Cooldown
import KBEngine

class CooldownTypeLoader:
	_instance = None
	def __init__( self ):
		assert CooldownTypeLoader._instance is None
		CooldownTypeLoader._instance = self
		self.cooldownDict = {}
	
	@staticmethod
	def instance():
		if not CooldownTypeLoader._instance:
			CooldownTypeLoader._instance = CooldownTypeLoader()
		return CooldownTypeLoader._instance
	
	def loadCooldownType( self, filePath ):
		"""
		加载配置
		"""
		absFilePath = KBEngine.getResFullPath(filePath)
		file = open( absFilePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		for data in jsFileData:
			cooldownIns = Cooldown()
			cooldownIns.init( data )
			self.cooldownDict[ data["id"] ] = cooldownIns
	
	def getCooldown( self, cdID ):
		return self.cooldownDict.get( cdID, None )

g_cdTypeLoader = CooldownTypeLoader.instance()