# -*- coding: utf-8 -*-

import csdefine
import csstatus

class CasterConditionBase:
	def init( self, params ):
		pass
	
	def check( self, caster ):
		return csstatus.SKILL_GO_ON

class CasterConditionLive( CasterConditionBase ):
	def check( self, caster ):
		if caster.state == csdefine.STATE_LIVE:
			return csstatus.SKILL_GO_ON
		else:
			return csstatus.SKILL_CASTER_STATUS_WRONG

class CasterConditionMP( CasterConditionBase ):
	def init( self, params ):
		self.minMP = int(params["param1"])
	
	def check( self, caster ):
		if caster.MP > self.minMP:
			return csstatus.SKILL_GO_ON
		else:
			return csstatus.SKILL_CASTER_STATUS_WRONG


g_objects = {	"CasterConditionLive": CasterConditionLive,
				"CasterConditionMP": CasterConditionMP,
			}

def newInstance( clsName ):
	return g_objects.get( clsName )()