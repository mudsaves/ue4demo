# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

def __testMonster( params ):
	"""
	刷怪
	
	params = [	("1", 100, (0,0,0), "10001"),
				("2", 100, (-30,0,50), "10001")
				]
	"""
	DEBUG_MSG("------------TestInterface::__testMonster()--------------")
	for tempTuple in params:
		(mapType, amount, pos, fsmKey) = tempTuple
		if mapType == "1":
			KBEngine.globalData["MapManager"].cell.test_createMonster( amount, pos, fsmKey )
		elif mapType == "2":
			KBEngine.globalData["MapManager2"].cell.test_createMonster( amount, pos, fsmKey )


def process( testType, params ):
	if testType == 1:
		__testMonster( params )
