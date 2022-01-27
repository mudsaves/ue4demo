# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

ACROSS_DELAY_TIMER = 11001
ACROSS_BACK_DELAY_TIMER = 11002

class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.cellData["moveSpeed"] = 3.0
		self.cellData["playerDBID"] = self.databaseID
		self.addTimer( 5, 1, 0 )
		self.player = None
		self.isWaitingAcross = False
		self.isWaitingAcrossBack = False
			
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		#DEBUG_MSG(id, userArg)		
		if userArg == ACROSS_DELAY_TIMER:
			self.onAcrossDelayTimer()
		elif userArg == ACROSS_BACK_DELAY_TIMER:
			self.onAcrossBackDelayTimer()
		
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		self.testVal = 110
		INFO_MSG("change prop[%i]" % (self.testVal))
		
		INFO_MSG("account[%i] entities enable. mailbox:%s" % (self.id, self.client))
		self.client.onDBID(self.databaseID)
		INFO_MSG("account DBID[%i]" % (self.databaseID))
		
		#arg = {}
		#self.player = KBEngine.createEntityLocally( "Player", arg )
		
		#self.createCellEntityInNewSpace(None)
		INFO_MSG("create Player Entity")
		if self.cell is None:
			# 在全局的地图空间创建自己的Cell
			baseMailbox = KBEngine.globalData["MapManager"]
			if baseMailbox is not None:
				baseMailbox.createCellEntityOnMap( self )
	
	def createCellEntityOnMapCB( self, mapCell ):
		"""
		define method
		向map请求创建cellEntity的回调
		"""
		self.createCellEntity( mapCell )
		INFO_MSG("create Player Entity OK")
	
	def onGetCell( self ):
		"""
		创建cell实体
		"""
		INFO_MSG("onGetCell Entity")
		
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		INFO_MSG("destroyCellEntity")
		self.destroyCellEntity()
		
	def onLoseCell( self ):
		"""
		销毁cell实体
		"""
		INFO_MSG("destroy")
		self.destroy()
		
	def onClientDBID(self, dbid):
		"""
			<Exposed/>
			<Arg>	DBID	</Arg> <!-- player dbid -->
		"""
		INFO_MSG("client return DBID[%i]" % (dbid))
		
	def onBaseEvent( self, dat ):
		"""
		"""
		self.client.onClientEvent(dat)
		INFO_MSG("onBaseEvent:", dat)
	
	def onClientGetCell(self):
		"""
		"""
		INFO_MSG("Account::onClientGetCell()")
	
	def testTime( self ):
		print("receive testTime")
		self.client.testBaseTimeCB()
	
	def onAcrossServerReady( self ):
		"""
		KBEngine method
		跨服数据已发往客户端，脚本层可以跨服了
		"""
		self.client.notifyAcrossServer()
	
	def reqLoginOffForAcross( self ):
		"""
		<Exposed/>
		跨服时下线
		"""
		self.isWaitingAcross = True
		
		#做跨服前的处理，比如下坐骑、收摊等，这里用timer回调来演示
		self.addTimer( 2, 0, ACROSS_DELAY_TIMER )
	
	def onAcrossDelayTimer( self ):
		"""
		脚本层已做好跨服准备
		"""
		if self.isWaitingAcross:
			self.isWaitingAcross = False
			self.destroyCellEntity()
	
	def acrossServerBack( self ):
		"""
		跨服状态下回到本服
		"""
		if not self.isAcrossServer:		#isAcrossServer为引擎属性，为True表示处于跨服状态
			ERROR_MSG("Account(%s) not in across server state!"%self.id)
			return
		self.client.notifyAcrossServerBack()
	
	def reqLoginOffForAcrossBack( self ):
		"""
		<Exposed/>
		回到本服前下线
		"""
		self.isWaitingAcrossBack = True
		
		#做跨服前的处理，比如下坐骑、收摊等，这里用timer回调来演示
		self.addTimer( 2, 0, ACROSS_BACK_DELAY_TIMER )
	
	def onAcrossBackDelayTimer( self ):
		"""
		脚本层已做好回到本服的准备
		"""
		if self.isWaitingAcrossBack:
			self.isWaitingAcrossBack = False
			self.destroyCellEntity()

