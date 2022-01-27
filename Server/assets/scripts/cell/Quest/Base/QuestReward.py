# -*- coding: utf-8 -*-

import json
import csdefine
from KBEDebug import *

class QuestReward:
    """
    任务奖励脚本
    """
    type = csdefine.QUEST_REWARD_NONE
    def __init__( self ):
        pass
    
    def init( self, dataConfig ):
        pass
    
    def getType( self ):
        return self.type
    
    def check( self, player ):
        """
        virtual method
        检查是否能正确执行奖励
        """
        return True

    def do( self, player ):
        """
        virtual method
        给奖励
        """
        pass
    
    def transferForClient( self, player ):
        """
        virtual method
        把当前值转换成客户端需要的数据流
        """
        return ( self.getType(), "" )
    
class QRewardMoney( QuestReward ):
    """
    奖励金钱
    """
    type = csdefine.QUEST_REWARD_MONEY
    def __init__( self ):
        self.amount = 0
    
    def init( self, dataConfig ):
        self.amount = int(dataConfig["param1"])
    
    def do( self, player ):
        """
        """
        DEBUG_MSG("Quest reward money(%s)."%self.amount)
    
    def transferForClient( self, player ):
        """
        virtual method
        把当前值转换成客户端需要的数据流
        """
        stream = json.dumps(self.amount)
        return ( self.getType(), stream )

class QRewardItems( QuestReward ):
    """
    奖励物品
    """
    type = csdefine.QUEST_REWARD_ITEMS
    def __init__( self ):
        self.itemIDList = 0
        self.amountList = 0
    
    def init( self, dataConfig ):
        self.itemIDList = [ int(i) for i in dataConfig["param1"].split("|") ]
        self.amountList = [ int(i) for i in dataConfig["param2"].split("|") ]
    
    def do( self, player ):
        """
        """
        DEBUG_MSG("Quest reward item. id(%s), amount(%s)."%(self.itemIDList, self.amountList))
    
    def transferForClient( self, player ):
        """
        virtual method
        把当前值转换成客户端需要的数据流
        """
        itemList = []
        for index, id in enumerate(self.itemIDList):
            info = (id, self.amountList[index])
            itemList.append( info )
        stream = json.dumps( itemList )
        return ( self.getType(), stream )


def newInstance( className ):
	try:
		return eval( className )()
	except:
		return None