# -*- coding: utf-8 -*-

import csdefine
from QuestTaskImpl import QuestTaskDataType

class QuestTask( QuestTaskDataType ):
	"""
	任务目标基类
	"""
	type = csdefine.QT_TYPE_NONE
	def __init__( self ):
		"""
		"""
		QuestTaskDataType.__init__( self )
	
	def init( self, dataDict ):
		"""
		virtual method
		从配置初始化
		"""
		self.index = dataDict["index"]
		self.taskTime = dataDict["taskTime"]
		self.val1 = dataDict["amount"]
	
	def getType( self ):
		"""
		获取任务目标类型枚举值
		"""
		return self.type
	
	def getEventTypes( self ):
		"""
		virtual method
		获取事件类型
		"""
		return []
	
	def initOnAccept( self, player ):
		"""
		vitual method
		玩家接到任务目标时做一些事
		"""
		pass
	
	def addCount( self, questID, player, val ):
		"""
		增加/减少 已完成数量
		"""
		self.val2 = min( self.val1, max(0, self.val2 + val) )
		if self.isComplete():
			self.onComplete( questID, player )
		else:
			self.onCountChange( questID, player )
	
	def setComplete( self, questID, player, isTimeArrive = False ):
		"""
		设置完成
		"""
		self.val2 = self.val1
		self.onComplete( questID, player, isTimeArrive )
	
	def setFail( self, questID, player, isTimeArrive = False ):
		"""
		设置失败
		"""
		self.val2 = -1
		self.onFail( questID, player, isTimeArrive )
	
	def isComplete( self ):
		"""
		是否已完成
		"""
		return self.val2 >= self.val1
	
	def isFail( self ):
		"""
		是否已失败
		"""
		return self.val2 == -1
	
	def onComplete( self, questID, player, isTimeArrive = False ):
		"""
		virtual method
		任务目标完成
		"""
		if isTimeArrive:	#如果是这个原因，此时self.taskTimerID已经是0
			player.cancelQuestTaskTimer( questID, self.index, 0 )
		elif self.taskTimerID > 0:
			player.cancelQuestTaskTimer( questID, self.index, self.taskTimerID )
			self.taskTimerID = 0
		
		player.onQuestTaskStateChange( questID, self.index, self.isComplete(), self.isFail(), self.val2 )
	
	def onFail( self, questID, player, isTimeArrive = False ):
		"""
		virtual method
		任务目标失败
		"""
		if self.taskTimerID > 0:
			player.cancelQuestTaskTimer( questID, self.index, self.taskTimerID )
			self.taskTimerID = 0
		
		player.onQuestTaskStateChange( questID, self.index, self.isComplete(), self.isFail(), self.val2 )
	
	def onCountChange( self, questID, player ):
		"""
		virtual method
		任务目标计数改变
		"""
		player.onQuestTaskStateChange( questID, self.index, self.isComplete(), self.isFail(), self.val2 )
	
	def doTrigger( self, questID, player, eventType, eventParams ):
		"""
		virtual method
		任务目标相关事件被触发了，要做一些事
		eventParams有哪些key请查看QuestInterface中相应事件触发接口
		"""
		pass
	
	def onTimeArrive( self, questID, player ):
		"""
		virtual method
		时限到达
		默认时间到达任务目标失败，如果需要设置为成功请重写此方法
		"""
		self.setFail( questID, player, True )

class QTKillMonster( QuestTask ):
	"""
	杀怪
	"""
	type = csdefine.QT_TYPE_KILL_MONSTER
	def __init__( self ):
		QuestTask.__init__( self )
		#self.str1 = 0		#怪物ID
	
	def init( self, dataDict ):
		"""
		virtual method
		从配置初始化
		"""
		QuestTask.init( self, dataDict )
		self.str1 = dataDict["param1"]
	
	def getEventTypes( self ):
		"""
		virtual method
		获取事件类型
		"""
		return [ csdefine.QT_EVENT_KILL ]
	
	def doTrigger( self, questID, player, eventType, eventParams ):
		"""
		virtual method
		任务目标相关事件被触发了，要做一些事
		eventParams有哪些key请查看QuestInterface中相应事件触发接口
		"""
		if self.isComplete() or self.isFail():
			return
		
		if eventParams["scriptID"] != self.str1:
			return
		
		self.addCount( questID, player, 1 )

class QTGiveItems( QuestTask ):
	"""
	提交物品
	"""
	type = csdefine.QT_TYPE_GIVE_ITEM
	def __init__( self ):
		QuestTask.__init__( self )
		#self.val3 = 0		#物品ID
	
	def init( self, dataDict ):
		"""
		virtual method
		从配置初始化
		"""
		QuestTask.init( self, dataDict )
		self.val3 = int( dataDict["param1"] )
	
	def getEventTypes( self ):
		"""
		virtual method
		获取事件类型
		"""
		return [ csdefine.QT_EVENT_ITEM_AMOUNT_CHANGE ]
	
	def initOnAccept( self, player ):
		"""
		vitual method
		玩家接到任务目标时做一些事
		"""
		self.val2 = 2#player.getItemAmountByID( self.itemID )
	
	def doTrigger( self, questID, player, eventType, eventParams ):
		"""
		virtual method
		任务目标相关事件被触发了，要做一些事
		eventParams有哪些key请查看QuestInterface中相应事件触发接口
		"""
		if self.isFail():
			return
		
		if eventParams["itemID"] != self.val3:
			return
		
		if eventParams["changeAmount"] > 0 and self.isComplete():
			return
		
		if eventParams["changeAmount"] < 0 and self.val2 == 0:
			return
		
		self.addCount( questID, player, eventParams["changeAmount"] )

class QTDieLessAmount( QuestTask ):
	"""
	死亡少于N次
	"""
	type = csdefine.QT_TYPE_DIE_LESS_AMOUNT
	def __init__( self ):
		QuestTask.__init__( self )
		#self.str1 = ""		#死亡次数上限
		#self.val3 = 0		#已死亡次数
	
	def init( self, dataDict ):
		"""
		virtual method
		从配置初始化
		"""
		QuestTask.init( self, dataDict )
		self.str1 = dataDict["param1"]
	
	def getEventTypes( self ):
		"""
		virtual method
		获取事件类型
		"""
		return [ csdefine.QT_EVENT_PLAYER_DIE ]
	
	def doTrigger( self, questID, player, eventType, eventParams ):
		"""
		virtual method
		任务目标相关事件被触发了，要做一些事
		eventParams有哪些key请查看QuestInterface中相应事件触发接口
		"""
		if self.val3 == int(self.str1):		#死亡达到N次
			return
		
		self.val3 += 1
		if self.val3 == int(self.str1):
			self.setFail( questID, player )
	
	def onTimeArrive( self, questID, player ):
		"""
		virtual method
		时限到达
		默认时间到达任务目标失败，如果需要设置为成功请重写此方法
		"""
		self.setComplete( questID, player, True )

class QTDirectTrigger( QuestTask ):
	"""
	触发型任务目标
	"""
	type = csdefine.QT_TYPE_DIRECT_TRIGGER
	def __init__( self ):
		QuestTask.__init__( self )
	
	def init( self, dataDict ):
		"""
		virtual method
		从配置初始化
		"""
		QuestTask.init( self, dataDict )
	
	def getEventTypes( self ):
		"""
		virtual method
		获取事件类型
		"""
		return [ csdefine.QT_EVENT_DIRECT_TRIGGER_TASK ]
	
	def doTrigger( self, questID, player, eventType, eventParams ):
		"""
		virtual method
		任务目标相关事件被触发了，要做一些事
		eventParams有哪些key请查看QuestInterface中相应事件触发接口
		"""
		if self.isComplete() or self.isFail():
			return
		
		if eventParams["questID"] != questID or eventParams["taskIndex"] != self.index:
			return
		
		self.addCount( questID, player, eventParams["count"] )


#目标类型枚举值与目标类map
type2Class_map = {	csdefine.QT_TYPE_KILL_MONSTER			: QTKillMonster,
					csdefine.QT_TYPE_GIVE_ITEM				: QTGiveItems,
					csdefine.QT_TYPE_DIE_LESS_AMOUNT		: QTDieLessAmount,
					csdefine.QT_TYPE_DIRECT_TRIGGER			: QTDirectTrigger,
					}


def newInstanceByType( type ):
	cls = type2Class_map.get( type, None )
	if not cls:
		return None
	return cls()

def newInstanceByCls( className ):
	try:
		return eval( className )()
	except:
		return None
