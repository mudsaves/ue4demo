// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "KBEnginePlugin/Filter/FilterActorComponent.h"
#include "KBEnginePlugin/Filter/DumbFilterActorComponent.h"
#include "KBEnginePlugin/Filter/AvatarFilterActorComponent.h"
#include "Component/TransFormControlActorComponent.h"
#include "AvatarActorComponent.h"
#include "MonsterActorComponent.generated.h"

UCLASS( )
class UE4DEMO_API UMonsterActorComponent : public UAvatarActorComponent
{
	GENERATED_BODY()

	typedef UAvatarActorComponent Super;

public:	
	// Sets default values for this component's properties
	UMonsterActorComponent();

	void __init__(KBEngine::Entity* _entity) override;
	void SetPosition(const FVector& newVal) override;
	void SetDirection(const FVector& newVal) override;
	void onUpdateVolatileData(const FVector& position, const FVector& direction);
	void OnFilterSpeedChanged(float speed) override;
	virtual void OnControlled(bool isControlled) override;

private:
	UDumbFilterActorComponent* mDumbFilterComp = nullptr;
	UAvatarFilterActorComponent* mAvatarFilterComp = nullptr;
	UTransFormControlActorComponent* mTransFormControlComp = nullptr;
};
