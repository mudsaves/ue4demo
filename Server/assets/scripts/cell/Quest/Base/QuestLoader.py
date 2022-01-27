# -*- coding: utf-8 -*-

import json
import SmartImport
import KBEngine

class QuestLoader:
	_instance = None
	def __init__( self ):
		assert QuestLoader._instance is None
		QuestLoader._instance = self
		self.quests = {}
	
	@staticmethod
	def instance():
		if not QuestLoader._instance:
			QuestLoader._instance = QuestLoader()
		return QuestLoader._instance
	
	def loadQuest( self, filePath ):
		"""
		加载配置
		"""
		absFilePath = KBEngine.getResFullPath(filePath)
		file = open( absFilePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		for data in jsFileData:
			if data["Script"] == "Quest":
				questClass = SmartImport.smartImport( "Quest.Base.Quest:Quest" )
			else:
				questClass = SmartImport.smartImport( "Quest." + data["Script"] + ":" + data["Script"] )
			questIns = questClass()
			questIns.init( data )
			self.quests[ data["id"] ] = questIns
	
	def getQuest( self, questID ):
		return self.quests.get( questID, None )

g_questLoader = QuestLoader.instance()