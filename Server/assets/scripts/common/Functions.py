# -*- coding: utf-8 -*-
import time
import csconst

def getTime( timeVal = 0.0 ):
	return int( ( time.time() + timeVal ) * csconst.TIME_ENLARGE_MULTIPLE )

def getFloatTime( timeVal ):
	return float( timeVal ) / csconst.TIME_ENLARGE_MULTIPLE

def dayIsOver( timeVal ):
	"""
	检测现在是否已经到达传入时间的下一天
	"""
	tm_year,tm_mon,tm_day,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst = time.localtime( timeVal )
	dayRestTime = (23 - tm_hour)*3600 + (59 - tm_min)*60 + (60 - tm_sec)	# 距离到下一天还有多少秒
	nextDayZeroTime = timeVal + dayRestTime
	return time.time() > nextDayZeroTime

def weekIsOver( timeVal ):
	"""
	检测现在是否已经到达传入时间的下一周
	"""
	tm_year,tm_mon,tm_day,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst = time.localtime( timeVal )
	weekRestTime = (6 - tm_wday)*24*3600 + (23 - tm_hour)*3600 + (59 - tm_min)*60 + (60 - tm_sec)	# 距离到下一周还有多少秒
	nextWeekZeroTime = timeVal + weekRestTime
	return time.time() > nextWeekZeroTime