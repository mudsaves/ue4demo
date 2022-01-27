# -*- coding: utf-8 -*-

import random, math
import Math

def strToPosition( position ):
	"""
	将字符串解析成坐标
	字符串格式为"0 0 0"
	"""
	pos = position.split(" ")
	return Math.Vector3(float(pos[0]), float(pos[1]), float(pos[2]))

def getRandomPosInRange(center, range):
	"""
	"""
	r = random.uniform( 1, range ) #最少走1米
	b = 360.0 * random.random()
	x = r * math.cos(b)
	z = r * math.sin(b)
	return Math.Vector3(center.x + x, center.y, center.z + z)

def entitiesInRange( entity, rng, cnd = lambda ent : True ) :
	"""
	搜索 entity 身边或指定点周边的所有 entity
	@type			rng : float
	@patam			rng : 搜索的半径
	@type			cnd : functor/method
	@param			cnd : 条件函数，它必须包含一个参数以表示遍历到的 entity，如果调用 cnd 返回 True，则表示参数 ent 是符合条件的 entity
	@return				: 返回所有要求的 entity
	@rtype				: list
	"""
	entities = []
	for id,e in entity.clientapp.entities.items() :
		if id == entity.id:
			continue
		dist = e.position.distTo( entity.position )
		if dist <= rng and cnd( e ):
			entities.append( e )
	return entities