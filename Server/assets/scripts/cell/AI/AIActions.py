# -*- coding: utf-8 -*-

from KBEDebug import *
from AI.Base.AIActionBase import AIActionBase

class AIAction1( AIActionBase ):
	"""
	使用技能
	"""
	def __init__( self ):
		self.skillID = 0
	
	def init( self, cfgData ):
		self.skillID = int(cfgData["param1"])
	
	def do( self, ai, entity ):
		ERROR_MSG("entity(%s):this is action1!"%entity.id)
		entity.useSkill( self.skillID, 0 )

class AIAction2( AIActionBase ):
	"""
	"""
	def __init__( self ):
		self.skillID = 0
	
	def init( self, cfgData ):
		self.skillID = int(cfgData["param1"])
	
	def do( self, ai, entity ):
		ERROR_MSG("entity(%s):this is action2!"%entity.id)
		entity.useSkill( self.skillID, 0 )

class AIAction3( AIActionBase ):
	"""
	"""
	def __init__( self ):
		pass
	
	def init( self, cfgData ):
		pass
	
	def do( self, ai, entity ):
		ERROR_MSG("entity(%s):this is action3!"%entity.id)

class AIAction4( AIActionBase ):
	"""
	"""
	def __init__( self ):
		pass
	
	def init( self, cfgData ):
		pass
	
	def do( self, ai, entity ):
		ERROR_MSG("entity(%s):this is action4!"%entity.id)