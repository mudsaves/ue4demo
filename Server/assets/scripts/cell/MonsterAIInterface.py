# -*- coding: utf-8 -*-

import csdefine
from AIInterface import AIInterface

class MonsterAIInterface( AIInterface ):
	"""
	"""
	def getAIFsmKey( self ):
		"""
		virtual method
		AI状态机key值
		不同的entity有不同的状态机key值，AI接口子类需要重载此方法，设置entity适配的key值
		"""
		return ""
		#return "10001"	#暂时都用key为10001的这个状态机，以后如果monster有scriptID了，这里应该返回str(self.scriptID)
	