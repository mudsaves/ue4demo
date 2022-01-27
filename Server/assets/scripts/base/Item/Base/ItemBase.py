# -*- coding: utf-8 -*-

import json
import csdefine

class ItemBase:
	"""
	物品基类
	不做具体的物品类使用
	"""
	def __init__( self ):
		#动态生成的数据
		self.uid = 0					# 全局唯一性ID
		self.ownerID = 0				# 物品拥有者ID
		self.order = -1					# 物品放置的位置
		self.amount = 1					# 当前数量，默认值为1
		self.tmpExtra = {}				# 额外的动态属性,此属性不存盘，只在运行时有效
		
		#不会改变的属性
		self.id = 0						# 物品ID
		self.reqLevel = 1				# 使用等级下限
		self.stackAmount = 1			# 可叠加数
	
	def init( self, itemID, cfgDict ):
		"""
		读取配置数据
		"""
		self.id = itemID
		self.reqLevel = cfgDict["reqLevel"]
		self.stackAmount = cfgDict["stackAmount"]
	
	def addToDict( self ):
		"""
		按define格式打包成dict
		"""
		return { 	"id" 		: self.id,
					"uid"		: self.uid,
					"ownerID"	: self.ownerID,
					"order"		: self.order,
					"amount" 	: self.amount,
					"extra" 	: json.dumps( self.packetExtraData() ),
					"tmpExtra" 	: json.dumps( self.tmpExtra ),
				}
	
	def loadFromDict( self, valDict ):
		"""
		从dict恢复数据
		"""
		self.id = valDict["id"]
		self.uid = valDict["uid"]
		self.ownerID = valDict["ownerID"]
		self.order = valDict["order"]
		self.amount = valDict["amount"]
		
		if valDict.has_key( "tmpExtra" ) and len( valDict["tmpExtra"] ):
			self.tmpExtra = json.loads( valDict["tmpExtra"] )
		
		if valDict.has_key( "extra" ):
			extraDict = json.loads( valDict["extra"] )
			self.loadFromExtraData( extraDict )
	
	def packetExtraData( self ):
		"""
		virtual method
		将动态的自定义属性打包成字典
		"""
		#extraDict = {}
		#extraDict["propertyName"] = self.propertyName
		#return extraDict
		return {}
	
	def loadFromExtraData( self, extraDict ):
		"""
		从extraDict读取属性
		"""
		for key, value in extraDict.items():
			setattr( self, key, value )
	
	def copyFromItem( self, srcItem ):
		"""
		复制其他item
		将动态数据复制过来
		"""
		self.uid = srcItem.uid
		self.ownerID = srcItem.ownerID
		self.order = srcItem.order
		self.amount = srcItem.amount
		self.tmpExtra = srcItem.tmpExtra
		
		extraDict = srcItem.packetExtraData()
		self.loadFromExtraData( extraDict )		#将自定义属性copy过来
	
	def getID( self ):
		return self.id
	
	def getReqLevel( self ):
		return self.reqLevel
	
	def getStackableAmount( self ):
		return self.stackAmount
	
	def getUID( self ):
		return self.uid
	
	def setUID( self, uid ):
		self.uid = uid
	
	def getOwnerID( self ):
		return self.ownerID
	
	def setOwnerID( self, dbid ):
		self.ownerID = dbid
	
	def getOrder( self ):
		return self.order
	
	def setOrder( self, order ):
		self.order = order
	
	def getAmount( self ):
		return self.amount
	
	def setAmount( self, amount, owner = None ):
		self.amount = amount
		if owner:
			stream = json.dumps({"type":"int32", "value":amount})
			owner.client.onItemAttrUpdated( self.order, "amount", stream )
	
	def queryTemp( self, attrName, default = None ):
		"""
		获取一个临时数据

		@param attrName: 想要获取的值的属性名称
		@type  attrName: String
		@param  default: 如果指定属性的值不存在，返回什么，默为返回None
		@type   default: any
		"""
		if attrName in self.tmpExtra:
			return self.tmpExtra[attrName]
		return default
	
	def setTemp( self, attrName, value, owner = None ):
		"""
		设置临时数据
		@param attrName: 属性名
		@type attrName: String
		@param value: 值
		@type value: python
		@param owner: 物品拥有者
		@type owner: Entity
		@return: None
		"""
		self.tmpExtra[attrName] = value
	
	def isStackableToItem( self, targetItem ):
		"""
		virtual method
		自己可以堆叠到某物品所在物品格
		"""
		return self.id == targetItem.id