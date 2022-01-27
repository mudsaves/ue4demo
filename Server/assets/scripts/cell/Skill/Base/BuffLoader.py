# -*- coding: utf-8 -*-

import json
import SmartImport
import KBEngine

class BuffLoader:
	_instance = None
	def __init__( self ):
		assert BuffLoader._instance is None
		BuffLoader._instance = self
		self.buffs = {}
	
	@staticmethod
	def instance():
		if not BuffLoader._instance:
			BuffLoader._instance = BuffLoader()
		return BuffLoader._instance
	
	def loadBuff( self, filePath ):
		"""
		加载配置
		"""
		absFilePath = KBEngine.getResFullPath(filePath)
		file = open( absFilePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		for data in jsFileData:
			if data["Script"] == "Buff":
				buffClass = SmartImport.smartImport( "Skill.Base.Buff:Buff" )
			else:
				buffClass = SmartImport.smartImport( "Skill.Buff." + data["Script"] + ":" + data["Script"] )
			buffIns = buffClass()
			buffIns.init( data )
			self.buffs[ data["id"] ] = buffIns
	
	def getBuff( self, buffID ):
		return self.buffs.get( buffID, None )

g_buffLoader = BuffLoader.instance()