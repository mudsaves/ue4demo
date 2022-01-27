# -*- coding: utf-8 -*-

import os
import json
import SmartImport
from KBEDebug import *
import KBEngine

class AICfgLoader:
	"""
	AI配置加载类
	"""
	_instance = None
	def __init__( self ):
		assert AICfgLoader._instance is None
		AICfgLoader._instance = self
		self.key2FsmDict = {}
	
	@staticmethod
	def instance():
		if not AICfgLoader._instance:
			AICfgLoader._instance = AICfgLoader()
		return AICfgLoader._instance
	
	def loadAICfg( self, fileDir ):
		"""
		"""
		absPath = KBEngine.getResFullPath(fileDir)
		for f in os.listdir( absPath ):
			if f.startswith("AI_"):
				path = os.path.join( fileDir, f )
				self.loadAIFile( path )
	
	def loadAIFile( self, filePath ):
		"""
		"""
		absFilePath = KBEngine.getResFullPath(filePath)
		file = open( absFilePath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		fsmKey = jsFileData["FsmKey"]
		if fsmKey in self.key2FsmDict:
			ERROR_MSG("AI fsm key is exist.[%s]."%fsmKey)
			return
		
		fsmCls = SmartImport.smartImport( "AI.AIFsm" + ":" + jsFileData["FsmScript"] )
		fsmInstance = fsmCls( fsmKey )
		fsmInstance.init( jsFileData )
		self.key2FsmDict[ fsmKey ] = fsmInstance
	
	def getEntityAIFsm( self, key ):
		"""
		"""
		return self.key2FsmDict.get(key, None)

g_aiCfgLoader = AICfgLoader.instance()