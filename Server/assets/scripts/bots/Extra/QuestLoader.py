# -*- coding: utf-8 -*-

import json

class QuestLoader:
	"""
	"""
	_instance = None
	def __init__( self ):
		assert QuestLoader._instance is None
		QuestLoader._instance = self
		self._quests = {}
	
	@staticmethod
	def instance():
		if not QuestLoader._instance:
			QuestLoader._instance = QuestLoader()
		return QuestLoader._instance
	
	def loadQuest(self, filePath):
		"""
		"""
		file = open( filePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		for q in jsFileData:
			self._quests[q["id"]] = q
	
	def getQuest( self, questID ):
		"""
		"""
		return self._quests.get(questID, None)


g_quests = QuestLoader.instance()