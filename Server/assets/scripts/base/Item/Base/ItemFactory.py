# -*- coding: utf-8 -*-

import os
import json
import SmartImport
import KBEngine
from KBEDebug import *

class ItemFactory:
	"""
	物品工厂
	"""
	_instance = None
	def __init__( self ):
		assert ItemFactory._instance is None
		ItemFactory._instance = self
		self._itemDict = {}		# 已加载的物品配置
		self._itemData = {}		# 所有物品配置
	
	@staticmethod
	def instance():
		if not ItemFactory._instance:
			ItemFactory._instance = ItemFactory()
		return ItemFactory._instance
	
	def loadItemCfg( self, fileDir ):
		"""
		"""
		absPath = KBEngine.getResFullPath(fileDir)
		for f in os.listdir( absPath ):
			if f.startswith("item_"):
				path = os.path.join( fileDir, f )
				self.loadItemFile( path )
	
	def loadItemFile( self, filePath ):
		"""
		"""
		absPath = KBEngine.getResFullPath(filePath)
		file = open( absPath, encoding="utf8" )
		jsFileData = json.loads( file.read() )
		file.close()
		
		self._itemDict.update( jsFileData )
	
	def __getItemDict( self, itemID ):
		"""
		获取物品配置数据
		"""
		itemID = str(itemID)
		itemDict = self._itemDict.get( itemID, None )
		if itemDict is None:
			itemDict = self._itemData.get( itemID, None )
			if itemDict is None:
				ERROR_MSG( "Item %s not found." % itemID )
				return None
			self._itemDict[itemID] = itemDict
		
		return itemDict
	
	def __createItemFromCfg( self, itemID ):
		"""
		根据物品配置创建物品
		@param id: 物品ID
		@type  id: int
		@param amount: 物品数量
		@type  amount: int
		"""
		itemDict = self.__getItemDict( itemID )
		if itemDict is None:
			return None
		
		scriptName = itemDict.get( "Script", "" )
		itemClass = SmartImport.smartImport( "Item." + scriptName + ":" + scriptName )
		item = itemClass()
		item.init( itemID, itemDict )
		return item
	
	def createObjFromDict( self, valDict ):
		"""
		"""
		itemID = valDict["id"]
		obj = self.__createItemFromCfg( itemID )			# 创建新的与之对应的对像
		if obj is None: return None
		obj.loadFromDict( valDict )
		return obj
	
	def createItem( self, itemID, amount ):
		"""
		生成一定数量的某物品
		"""
		item = self.__createItemFromCfg( itemID )
		item.setAmount( amount )
		item.setUID( KBEngine.genUUID64() )
		return item
	
	def newItemByCopy( self, item ):
		"""
		复制一个item，赋予新的UID
		"""
		newItem = self.__createItemFromCfg( item.getID() )
		newItem.copyFromItem( item )
		newItem.setUID( KBEngine.genUUID64() )
		return newItem


g_itemFactory = ItemFactory.instance()