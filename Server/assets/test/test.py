# -*- coding: utf-8 -*-

import time
import telnetlib
import platform

psNotifyStr = "password:"
welcomeStr = "welcome to"

class TelnetClient:
	def __init__(self,):
		self.tn = telnetlib.Telnet()

	def login_host( self, host_ip, port, password ):
		try:
			self.tn.open( host_ip, port )
		except:
			print('connect failure! ip:[%s] port:[%s]\n'%(host_ip, port))
			return False
		
		welBStr = welcomeStr.encode('ascii')
		psNotifyBStr = psNotifyStr.encode('ascii')
		
		time.sleep(2)	#2秒后读取结果
		connectResult = self.tn.read_very_eager()
		if welBStr in connectResult:	#服务器端没有设置密码
			print('connect success!\n')
			return True
		
		elif psNotifyBStr in connectResult:
			self.tn.write( password.encode('ascii') + b'\r\n' )
			psResult = self.tn.read_until( welBStr, timeout = 10 )
			if welBStr in psResult:
				print('connect success!\n')
				return True
			else:
				print('connect failure,password error! [%s]\n'%password)
				return False
		
		else:
			print('connect failure!\n')
			return False

	# 此函数实现执行传过来的命令
	def execute_some_command( self, command ):
		print("send command >> %s\n"%command)
		self.tn.write( command.encode('ascii') + b'\r\n' )


if __name__ == '__main__':
	try:
		from config import targetIP
		from config import targetPort
		from config import password
		from config import command
	except Exception as e:
		print("config error:",e)
	
	else:
		telnet_client = TelnetClient()
		# 如果登录结果返为True，则执行命令，然后退出
		result = telnet_client.login_host( targetIP, targetPort, password )
		if result:
			telnet_client.execute_some_command( command )
	
	sysstr = platform.system()
	if sysstr == "Windows":
		while(True):
			input("按回车键退出：")
			break
	else:
		time.sleep(2)