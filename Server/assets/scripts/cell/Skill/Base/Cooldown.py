# -*- coding: utf-8 -*-

import Functions

class Cooldown:
	"""
	CD类
	"""
	def __init__( self ):
		self.id = 0
		self._isSave = False		#是否下线保存
		self._alwayCalc = False		#下线是否继续计时
	
	def init( self, dataDict ):
		self._isSave = dataDict["save"]
		self._alwayCalc = dataDict["alwayCalc"]
	
	def isSave( self ):
		return self._isSave
	
	def calculateOnSave( self, timeVal ):
		"""
		销毁时计算cd时间
		"""
		if not self._alwayCalc :
			# 下线后不计时，需要将值处理成剩余时间
			timeVal -= Functions.getTime()
		return timeVal
	
	def calculateOnLoad( self, timeVal ):
		"""
		初始化时重新计算cd时间
		"""
		if not self._alwayCalc:
			# 下线后不计时，需要将剩余时间重新处理成buff时间
			timeVal += Functions.getTime()
		return timeVal
