# -*- coding: utf-8 -*-

import SmartImport

class AIData:
	"""
	一条AI
	"""
	def __init__( self ):
		self.id = 0
		self.conditions = []
		self.actions = []
		self.EAI = []
	
	def init( self, cfgData ):
		self.id = cfgData["id"]
		
		for conDict in cfgData["condition"]:
			conCls = SmartImport.smartImport( "AI.AIConditions" + ":" + conDict["Script"] )
			conIns = conCls()
			conIns.init( conDict )
			self.conditions.append( conIns )
		
		for actDict in cfgData["action"]:
			actCls = SmartImport.smartImport( "AI.AIActions" + ":" + actDict["Script"] )
			actIns = actCls()
			actIns.init( actDict )
			self.actions.append( actIns )
		
		self.EAI = cfgData["EAI"]
	
	def getID( self ):
		return self.id
	
	def do( self, entity ):
		"""
		"""
		for condition in self.conditions:
			if not condition.check( self, entity ):
				return
		
		for action in self.actions:
			action.do( self, entity )
		
		for id in self.EAI:
			entity.addEAI( id )