# -*- coding: utf-8 -*-

from KBEDebug import *

class CostBase:
	"""
	消耗类，基类
	"""
	def __init__( self ):
		self.amount = 0
	
	def init( self, params ):
		self.amount = int(params["param1"])
	
	def do( self, caster ):
		pass

class CostMoney( CostBase ):
	"""
	"""
	def do( self, caster ):
		#caster.reduceMoney( self.amount )
		DEBUG_MSG("CostMoney amount(%s)."%self.amount)

class CostMP( CostBase ):
	"""
	"""
	def do( self, caster ):
		#caster.reduceMP( self.amount )
		DEBUG_MSG("CostMP amount(%s)."%self.amount)


g_objects = {	"CostMoney": CostMoney,
				"CostMP": CostMP,
			}

def newInstance( clsName ):
	return g_objects.get( clsName )()