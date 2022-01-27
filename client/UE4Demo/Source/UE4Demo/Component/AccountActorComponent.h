// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "AvatarActorComponent.h"
#include "Component/TransFormControlActorComponent.h"
#include "AccountActorComponent.generated.h"


UCLASS( )
class UE4DEMO_API UAccountActorComponent : public UAvatarActorComponent
{
	GENERATED_BODY()

	typedef UAvatarActorComponent Super;

public:	
	// Sets default values for this component's properties
	UAccountActorComponent();

	void __init__(KBEngine::Entity* _entity) override;
	void SetPosition(const FVector& oldVal) override;
	void SetDirection(const FVector& oldVal) override;
	void onUpdateVolatileData(const FVector& position, const FVector& direction) override;

	void SetMoveSpeed() override;
	void OnFilterSpeedChanged(float speed) override;
	virtual void OnControlled(bool isControlled) override;

private:
	UTransFormControlActorComponent* mTransFormControlComp = nullptr;
};
