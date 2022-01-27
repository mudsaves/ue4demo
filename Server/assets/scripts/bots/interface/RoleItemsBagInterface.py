# -*- coding: utf-8 -*-

from configObject.Item.Item import Item

class RoleItemsBagInterface:
	"""
	"""
	def __init__(self):
		self.items = {}
	
	def requestInitItem(self):
		"""
		向服务器请求物品数据
		"""
		self.cell.clientRequestItems()
	
	def receiveItemOnInit( self, itemData ):
		"""
		define method
		请求物品数据回调
		"""
		item = Item()
		item.init( itemData )
		self._addItem( item.order, item )
	
	def _addItem( self, order, item ):
		"""
		添加物品
		"""
		self.items[ order ] = item
	
	def addItem( self, itemData ):
		"""
		define method
		"""
		item = Item()
		item.init( itemData )
		self._addItem( item.order, item )
	
	def removeItem( self, order ):
		"""
		define method
		"""
		if order in self.items:
			self.items.pop( order )
	
	def onItemAttrUpdated( self, order, attrName, attrValue ):
		"""
		define method
		"""
		if order not in self.items:
			return
		self.items[order].setItemAttr( "attrName", attrValue )