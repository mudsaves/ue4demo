#include "EntityDeclare.h"
#include "UE4Demo.h"

#include "KBEngine.h"

#include "Account.h"
#include "Monster.h"
#include "MovePlatform.h"

void EntityDeclare()
{
	ENTITY_DECLARE(TEXT("Account"), Account);
	ENTITY_DECLARE(TEXT("Monster"), Monster);
	ENTITY_DECLARE(TEXT("MovePlatform"), MovePlatform);
}
