#pragma once

#include "KBEngine.h"
#include "Component/AvatarActorComponent.h"

class Avatar : public KBEngine::Entity
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Entity Supper;

public:
	enum eEntityType : int
	{
		Unknown = 0,
		Player,
		Monster,
		MovePlatform,
	};

public:
	Avatar();
	~Avatar();

	virtual void OnEnterScenes() { }
	virtual void OnControlled(bool isControlled) override;
	virtual void OnGotParentEntity() override;
	virtual void OnLoseParentEntity() override;
	virtual void OnUpdateVolatileDataByParent() override;
	virtual eEntityType EntityType() { return eEntityType::Unknown; }

protected:
	UAvatarActorComponent* mComponent = nullptr;
};