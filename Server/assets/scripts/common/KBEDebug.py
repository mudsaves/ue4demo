# -*- coding: utf-8 -*-
import sys
import KBEngine

def printMsg(args, isPrintPath):
	for m in args:print (m)

def TRACE_MSG(*args): 
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_NORMAL)
	printMsg(args, False)
	
def DEBUG_MSG(*args): 
	if KBEngine.publish() == 0:
		KBEngine.scriptLogType(KBEngine.LOG_TYPE_DBG)
		printMsg(args, True)
	
def INFO_MSG(*args): 
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_INFO)
	printMsg(args, False)
	
def WARNING_MSG(*args): 
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_WAR)
	printMsg(args, True)

def ERROR_MSG(*args): 
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
	printMsg(args, True)

def EXCEHOOK_MSG( *args ) :
	"""
	输出当前栈帧错误信息，常用于输出异常信息
	
	@param 			args : 输出的信息
	@type 			args : 可变参数列表
	@return				 : None
	"""
	KBEngine.scriptLogType(KBEngine.LOG_TYPE_ERR)
	exceInfo = sys.exc_info()
	if exceInfo is None or exceInfo == ( None, None, None ) :
		ERROR_MSG( "no exception in stack!" )
	else :
		print( "EXCEHOOK_MSG: " )
		for arg in args :
			print( str( arg ) )
		sys.excepthook( *exceInfo )