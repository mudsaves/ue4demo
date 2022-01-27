# -*- coding: utf-8 -*-

#ai切换概率(需进行哪项测试，请将对应的测试项的值设为100，其他项值设为0)
aiPer = {
	"FightRoleAI"			: 0,				#玩家竞技
	"FightMonsterAI"		: 0,				#玩家与怪物战斗
	"QuestAI"				: 100,				#单一任务
	"LoopQuestAI"			: 0,				#多任务
	"ContrlMonsterMoveAI"	: 0,				#控制怪物跟随自己移动
}

"""
单一任务测试配置 -------------------------------
"""
QuestAI_questID = 4				#任务ID
QuestAI_isLoop = True			#是否循环刷任务

"""
多任务测试配置 -------------------------------
"""
LoopQuestAI_questID = [4, 5, 6]		#任务列表
LoopQuestAI_isLoop = True			#是否循环刷任务

"""
与玩家战斗测试配置-----------------------------
"""
FightRoleAI_radius = 10			#搜索范围
FightRoleAI_skill = 1			#使用的攻击技能

"""
与怪物战斗测试配置-----------------------------
"""
FightMonsterAI_radius = 10		#搜索范围
FightMonsterAI_skill = 5		#使用的攻击技能

"""
控制怪物跟随自己移动测试配置-----------------------------
"""
ContrlMonsterMoveAI_radius = 10		#走动半径
ContrlMonsterMoveAI_amount = 50		#招怪数量