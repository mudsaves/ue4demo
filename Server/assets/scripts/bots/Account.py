# -*- coding: utf-8 -*-

import random
import KBEngine
import kbengine
import KST_Config
import time

from KBEDebug import *
from Extra.KSTEvent import KSTEvent
from interface.SkillInterface import SkillInterface
from interface.QuestInterface import QuestInterface
from interface.CombatInterface import CombatInterface
from interface.RoleItemsBagInterface import RoleItemsBagInterface

class Account(
	KBEngine.Entity,
	SkillInterface,
	QuestInterface,
	CombatInterface,
	RoleItemsBagInterface
	):
	def __init__(self):
		"""
		"""
		KBEngine.Entity.__init__(self)
		SkillInterface.__init__(self)
		QuestInterface.__init__(self)
		CombatInterface.__init__(self)
		RoleItemsBagInterface.__init__(self)
		self.eventObj = KSTEvent()
		self.ai = None
		self.controlledEntities = []
		self.testCell_time = 0.0
		self.testBase_time = 0.0
		
		DEBUG_MSG( "account entity %s created" % self.id )
	
	def onLeaveSpace( self ):
		"""
		离开space
		"""
		player = self.clientapp.player()
		if player:
			player.eventObj.fireEvent( "Event_onEntityLeaveSpace", self.id )
	
	def onDBID( self, dbid ):
		pass
	
	def onClientEvent( self, arg ):
		pass
	
	def testFixedDict( self, item ):
		pass
	
	def testFixedDictT1( self, item1 ):
		pass
	
	def testOther1( self, arg1, arg2, arg3, arg4 ):
		pass
	
	def testJson( self, arg ):
		pass
	
	def testForNoParam( self ):
		pass
	
	def testCellTime( self ):
		t = time.time()
		self.testCell_time = t
		print("testCellTime", t)
		self.cell.testTime()
	
	def testCellTimeCB( self ):
		t = time.time()
		print("testCellTimeCB", t, t-self.testCell_time)
	
	def testBaseTime( self ):
		t = time.time()
		self.testBase_time = t
		print("testBaseTime", t)
		self.base.testTime()
	
	def testBaseTimeCB( self ):
		t = time.time()
		print("testBaseTimeCB", t, t-self.testBase_time)


	def notifyAcrossServer( self ):
		"""
		define method
		"""
		pass

	def notifyAcrossServerBack( self ):
		"""
		define method
		"""
		pass

from PlayerAI.QuestAI import QuestAI
from PlayerAI.LoopQuestAI import LoopQuestAI
from PlayerAI.FightAI import FightRoleAI
from PlayerAI.FightAI import FightMonsterAI
from PlayerAI.ContrlMonsterMoveAI import ContrlMonsterMoveAI

class PlayerAccount( Account ):
	"""
	"""
	def __init__(self):
		Account.__init__(self)
	
	def onBecomePlayer( self ):
		"""
		KBEngine method.
		当这个entity被引擎定义为角色时被调用
		"""
		kbengine.playerRole.append( self )
		DEBUG_MSG("Login server Roles: %d" %(len(kbengine.playerRole)))
		self.requestClientData()
		self.attachDefaultAI()
	
	def onDestroy(self):
		"""
		"""
		for role in kbengine.playerRole:
			if role.id == self.id:
				kbengine.playerRole.remove( self )
	
	def requestClientData( self ):
		"""
		向服务器请求客户端数据
		"""
		self.requestInitQuest()
		self.requestInitItem()
	
	def attachDefaultAI( self ):
		"""
		"""
		per = random.randint(1, 100)
		ainame = ""
		for k, v in KST_Config.aiPer.items():
			if per <= v:
				ainame = k
				break
			else:
				per = per - v
				
		if ainame == "":
			ERROR_MSG("player check ai error")
			return
		
		from PlayerAI.Base.AIBase import AIBase
		self.ai = AIBase.getClassObj(ainame)
		if self.ai is None:
			ERROR_MSG("not found ai[%s]" %(ainame))
			return
	
		self.ai.attach( self )
	
	def onEnterWorld( self ):
		"""
		"""
		KBEngine.callback( 2, self.onSetSpaceData )
	
	def onLeaveWorld( self ):
		"""
		"""
		pass
		
	def onEnterSpace( self ):
		"""
		"""
		pass
		
	def onLeaveSpace( self ):
		"""
		"""
		pass
	
	def onSetSpaceData(self):
		"""
		"""
		if self.ai:
			self.ai.onSetSpaceData()
	
	def onMoveOver( self, controllerID, userData ):
		"""
		"""
		self.eventObj.fireEvent( "Event_onMoveOver" )
	
	def onMoverFailure( self, controllerID, userData ):
		"""
		"""
		pass
	
	def moveToPos(self, pos):
		"""
		"""
		return self.moveToPoint( pos, self.moveSpeed, 0.0, 0, True, True )
	
	def GMCommand( self, targetID, cmd, *params ):
		""" 使用GM命令 """
		if params:
			strParams = " ".join(params) 
		else:
			strParams = ""
		self.cell.clientReqGMCommand( targetID, cmd, strParams )
	
	def addControlledEntity( self, entity ):
		"""
		添加被自己控制的entity
		"""
		self.controlledEntities.append( entity )
	
	def removeControlledEntity( self, entity ):
		"""
		从控制列表中移除entity
		"""
		for e in self.controlledEntities:
			if e.id == entity.id:
				self.controlledEntities.remove( e )
				break

