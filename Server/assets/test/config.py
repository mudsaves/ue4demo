# -*- coding: utf-8 -*-

targetIP = 'localhost'		#目标机器ip
targetPort = 50000			#目标进程telnet端口
password = 'pwd123456'		#telnet密码

#命令参数
TEST_TYPE = 1
TEST_PARAM = [	('1', 10, (0,0,0), 'test'),
				('2', 10, (-30,0,50), 'test')
				]

#命令
command = "from TestInterface import *; process(%s, %s)"%(TEST_TYPE, TEST_PARAM)