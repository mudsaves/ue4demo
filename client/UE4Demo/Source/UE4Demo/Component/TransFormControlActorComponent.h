// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "Components/ActorComponent.h"
#include "TransFormControlActorComponent.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class UE4DEMO_API UTransFormControlActorComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	UTransFormControlActorComponent();
	
	// Called every frame
	virtual void TickComponent( float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction ) override;

	FORCEINLINE void Init(KBEngine::Entity* _entity)
	{
		mEntity = _entity;
	}

private:		
	KBEngine::Entity* mEntity = nullptr;
};
