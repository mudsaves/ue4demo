# -*- coding: utf-8 -*-

class Item:
	"""
	"""
	def __init__(self):
		self.uid = 0
		self.id = 0
		self.amount = 0
		self.order = 0
		
	def init(self, data):
		self.uid = int(data["uid"])
		self.id = int(data["id"])
		self.amount = int(data["amount"])
		self.order = int(data["order"])
	
	def setItemAttr( self, name, value ):
		"""
		"""
		if not hasattr( self, name ):
			return
		setattr( self, name, value )