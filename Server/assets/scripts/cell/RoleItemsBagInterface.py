# -*- coding: utf-8 -*-

import csdefine
from KBEDebug import *
from Item.Base.ItemFactory import g_itemFactory

class RoleItemsBagInterface:
	"""
	玩家背包操作接口
	"""
	def __init__( self ):
		pass
		#self.initItemOrder = -1		#分包发送物品数据给客户端时记录当前发送到哪一个物品了
	
	def onTimer( self, id, userArg ):
		"""
		"""
		if userArg == csdefine.INIT_ITEMS_TIMER:
			self.sendItemsToClient( id )
	
	def clientRequestItems( self, srcEntityID ):
		"""
		Exposed method
		客户端请求物品数据
		"""
		if srcEntityID != self.id:
			return
		self.initItemOrder = 0
		self.addTimer( 0.0, 0.1, csdefine.INIT_ITEMS_TIMER )

	def sendItemsToClient( self, timerID ) :
		"""
		分包发送物品
		"""
		items = self.itemsBag.itemDatas()
		count = len( items )
		
		startOrder = self.initItemOrder
		endOrder = min( count, startOrder + 5 )							# 每次发 5 个
		for order in range( startOrder, endOrder ):						# 一次发一小组物品
			item = items[order]
			self.client.receiveItemOnInit( item )
		
		if endOrder < count:											# 如果还有剩余物品
			self.initItemOrder += 5										# 则索引指针下跳 5 格
		else:															# 如果没有剩余物品
			self.delTimer( timerID )									# 删除更新 timer
			self.initItemOrder = -1										# 删除临时索引指针
	
	def __addItemToOrder( self, order, item ):
		"""
		增加物品最终接口
		加到某空物品格，不为空加不成功（不管是否超过叠加上限）
		return 成功添加的数量
		"""
		if self.itemsBag.addToOrder( order, item ):
			self.client.addItem( item )
			return item.getAmount()
		else:
			return 0
	
	def __removeItemByOrder( self, order ):
		"""
		移除物品最终接口
		return 成功减少的数量
		"""
		item = self.itemsBag.getItem( order )
		if self.itemsBag.removeByOrder( order ):
			self.client.removeItem( order )
			return item.getAmount()
		else:
			return 0
	
	def _addItem( self, item ):
		"""
		增加物品
		找一个空的物品格放入（不管是否超过叠加上限）
		return 成功添加的数量
		"""
		order = self.itemsBag.getFreeOder()
		if order != -1:
			return self.__addItemToOrder( order, item )
		else:
			return 0
	
	def _addItemByStacking( self, item ):
		"""
		增加物品
		尽量将物品放入背包（先找能叠加的物品格，装满了找空的物品格，直到装不下，装不下的丢弃）
		return 成功添加的数量
		"""
		totalAmount = item.getAmount()
		stackableAmount = item.getStackableAmount()
		if stackableAmount > 1:
			if self._stackableItem( item ):		#先进行堆叠
				return totalAmount
		
		order = self.itemsBag.getFreeOder()			#然后找一个空格子
		if order == -1:
			return totalAmount - item.getAmount()
		
		if stackableAmount > item.getAmount():		#剩下的能放到一个格子里
			self.__addItemToOrder( order, item )
			return totalAmount
		
		remainAmount = item.getAmount() - stackableAmount
		item.setAmount( stackableAmount )
		self.__addItemToOrder( order, item )		#先填满这个格子
		
		#剩下的放到别的格子
		while(remainAmount > 0):
			order = self.itemsBag.getFreeOder()
			if order == -1:
				return totalAmount - remainAmount
			
			newItem = g_itemFactory.newItemByCopy( item )
			stackAmount = min( item.getStackableAmount(), remainAmount )
			newItem.setAmount( stackAmount )
			self.__addItemToOrder( order, newItem )
			remainAmount -= stackAmount
		
		if remainAmount > 0:
			return totalAmount - remainAmount
		else:
			return totalAmount
	
	def _removeItem( self, order, amount = 1 ):
		"""
		移除物品
		"""
		item = self.itemsBag.getItem( order )
		if not item:
			return 0
		
		if item.getAmount() <= amount:
			return self.__removeItemByOrder( order )
		else:
			item.setAmount( item.getAmount() - amount, self )
			return amount
	
	def _stackableItem( self, item ):
		"""
		叠加一个物品到包裹
		"""
		totalAmount = item.getAmount()
		orderList = self.itemsBag.findStackableOrder( item )
		remainAmount = totalAmount
		for order in orderList:
			o_item = self.itemsBag.getItem( order )
			stackAmount = min( o_item.getStackableAmount() - o_item.getAmount(), remainAmount )
			o_item.setAmount( o_item.getAmount() + stackAmount, self )
			remainAmount -= stackAmount
			
			if remainAmount <= 0:		#通过叠加放入了所有的item
				item.setAmount( 0 )
				return True
		
		item.setAmount( remainAmount )
		return False	#没叠加完
	
	
	#----------------------------外部接口--------------------------------
	def addItemByID( self, itemID, amount, reason ):
		"""
		"""
		item = g_itemFactory.createItem( itemID, amount )
		item.setOwnerID( self.playerDBID )
		addAmount = self._addItemByStacking( item )
		self.questItemAmountChange( itemID, addAmount )
		DEBUG_MSG("Player(%s) add item. itemID(%s), itemAmount(%s), reason(%s)."%(self.id, itemID, addAmount, reason))
	
	def removeItemByOrder( self, order, amount, reason ):
		"""
		"""
		item = self.itemsBag.getItem( order )
		if not item:
			return
		
		itemID = item.getID()
		remAmount = self._removeItem( order, amount )
		self.questItemAmountChange( itemID, remAmount )
		DEBUG_MSG("Player(%s) remove item. order(%s), itemAmount(%s), reason(%s)."%(self.id, order, remAmount, reason))
	
	def useItem( self, srcEntityID, order, targetObj ):
		"""
		使用物品
		Exposed method
		
		@param order: 物品索引
		@type order: 物品索引
		@param targetObj: 技能施展对象
		@type targetObj: SkillTargetObjEntity 或 SkillTargetObjPosition
		"""
		if self.id != srcEntityID:
			return
		item = self.itemsBag.getItem( order )
		if item:
			item.use( self, targetObj )
	
	def item_onSkillCastOver( self, skillID ):
		"""
		技能释放完毕
		"""
		if self.spellingItem:
			self.spellingItem.onSkillCastOver( self, skillID )
	
	def item_onSkillInterrupted( self, skillID ):
		"""
		技能被打断
		"""
		if self.spellingItem:
			self.spellingItem.onSkillInterrupted( self, skillID )