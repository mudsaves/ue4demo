# -*- coding: utf-8 -*-

from KBEDebug import *
from Skill.Base.Buff import Buff

class BuffAddMP( Buff ):
	"""
	加MP
	"""
	def __init__( self ):
		Buff.__init__( self )
		self.mp = 0
		self.loopMP = 0
	
	def init( self, dataDict ):
		"""
		"""
		Buff.init( self, dataDict )
		self.mp = dataDict["param1"]
		self.loopMP = dataDict["param2"]
	
	def begin( self, receiver, buffData ):
		"""
		"""
		Buff.begin( self, receiver, buffData )
		DEBUG_MSG("Buff(%s) begin. entity:%s, mp:%s."%(self.id, receiver.id, self.mp))
	
	def reload( self, receiver, buffData ):
		"""
		重载
		"""
		Buff.reload( self, receiver, buffData )
		DEBUG_MSG("Buff(%s) reload. entity:%s."%(self.id, receiver.id))
	
	def doLoop( self, receiver, buffData ):
		"""
		"""
		Buff.doLoop( self, receiver, buffData )
		DEBUG_MSG("Buff(%s) doLoop. entity:%s. loopMP:%s."%(self.id, receiver.id, self.loopMP))
		return True
	
	def end( self, receiver, buffData ):
		"""
		"""
		Buff.end( self, receiver, buffData )
		DEBUG_MSG("Buff(%s) end. entity:%s."%(self.id, receiver.id))