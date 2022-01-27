#include "Avatar.h"
#include "UE4Demo.h"


KBE_BEGIN_ENTITY_METHOD_MAP(Avatar, Entity)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(Avatar, Entity)
KBE_END_ENTITY_PROPERTY_MAP()

Avatar::Avatar()
{	
}

Avatar::~Avatar()
{

}

void Avatar::OnControlled(bool isControlled)
{
	if (mComponent)
	{
		mComponent->OnControlled(isControlled);
	}
}

void Avatar::OnGotParentEntity()
{
	if (mComponent)
		mComponent->OnGotParentEntity();
}

void Avatar::OnLoseParentEntity()
{
	if (mComponent)
		mComponent->OnLoseParentEntity();
}

void Avatar::OnUpdateVolatileDataByParent()
{
	if (mComponent)
		mComponent->OnUpdateVolatileDataByParent();
}
