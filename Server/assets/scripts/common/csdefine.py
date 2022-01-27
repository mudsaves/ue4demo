# -*- coding: utf-8 -*-

#技能对象类型
SKILL_TARGET_NONE = 0		# 无目标
SKILL_TARGET_ENTITY = 1		# entity
SKILL_TARGET_POSITION = 2	# 位置

#技能打包对象类型
SKILL_TARGET_OBJECT_ENTITY = 1		# entity
SKILL_TARGET_OBJECT_POSITION = 2	# 位置

#entity生存状态
STATE_LIVE = 1	#存活
STATE_DEAD = 2	#死亡

#战斗状态
COMBAT_STATE_FREE = 1	#自由状态
COMBAT_STATE_FIGHT = 2	#战斗状态
COMBAT_STATE_RESET = 3	#回走状态

#技能中断码
SKILL_INTERRUPT_CODE_DIE = 1	#死亡

#技能事件类型
SKILL_EVENT_RECEIVE_DAMAGE	= 1	#受到伤害
SKILL_EVENT_STATE_CHANGE	= 2	#状态改变

#效果来源
EFFECT_SOURCE_SKILL = 1	#技能
EFFECT_SOURCE_BUFF = 2	#Buff

#各种timer的userArg
BUFF_LOOP_TIMER = 222
BUFF_END_TIMER = 333
QUEST_TASK_TIMER = 444
FIGHT_STATE_TIMER = 555
INIT_ITEMS_TIMER = 666

#任务状态
QUEST_STATE_NOT_ALLOW			= 0		# 不够条件接任务
QUEST_STATE_ALLOW				= 1		# 可接
QUEST_STATE_NOT_COMPLETE		= 2		# 已接未完成
QUEST_STATE_HAS_COMPLETE		= 3		# 已完成可提交
QUEST_STATE_HAS_SUBMIT			= 4		# 已提交（已做过）

#任务周期
QUEST_PERIOD_NOT_LIMIT	= 0		#无限制
QUEST_PERIOD_ONCE		= 1		#只能做一次
QUEST_PERIOD_DAY		= 2		#一天一次
QUEST_PERIOD_WEEK		= 3		#一周一次

#任务类型
QUEST_TYPE_NONE			= 0		#默认值
QUEST_TYPE_NORMAL		= 1		#普通任务
QUEST_TYPE_POTENTIAL	= 2		#潜能任务
QUEST_TYPE_TONG			= 3		#帮会任务

#任务目标类型
QT_TYPE_NONE			= 0		#默认值
QT_TYPE_KILL_MONSTER	= 1		#杀怪
QT_TYPE_GIVE_ITEM		= 2		#提交物品
QT_TYPE_DIE_LESS_AMOUNT	= 3		#死亡次数少于N次
QT_TYPE_DIRECT_TRIGGER	= 4		#触发型任务目标

#任务事件类型
QT_EVENT_KILL					= 1		#杀怪
QT_EVENT_ITEM_AMOUNT_CHANGE		= 2		#物品数量改变
QT_EVENT_PLAYER_DIE				= 3		#角色死亡
QT_EVENT_DIRECT_TRIGGER_TASK	= 4		#通知某任务目标计数加1

#任务奖励类型
QUEST_REWARD_NONE           = 0 #默认值
QUEST_REWARD_MONEY          = 1 #金钱
QUEST_REWARD_ITEMS          = 2 #物品

#物品增加原因
ADD_ITEM_GM					= 1	#GM指令

#物品减少原因
DELETE_ITEM_USE				= 1	#使用物品

#使用物品时，物品移除时机
ITEM_REM_MOMENT_NO			= 1	#不移除
ITEM_REM_MOMENT_USE			= 2	#物品使用成功就移除
ITEM_REM_MOMENT_SKILL_OVER	= 3	#物品技能释放完毕移除

#AI状态
AIS_NONE			= 0	#空值
AIS_MONSTER_FREE	= 1	#怪物自由
AIS_MONSTER_FIGHT	= 2	#怪物战斗
AIS_MONSTER_RESET	= 3	#怪物回走状态

#AI事件
AI_EVENT_DIE				= 1	#entity死亡
AI_EVENT_COM_STATE_CHANGE	= 2	#entity战斗状态改变