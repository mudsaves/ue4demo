// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Components/ActorComponent.h"
#include "KBEngine.h"
#include "FilterActorComponent.generated.h"

class UAvatarActorComponent;

UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class UE4DEMO_API UFilterActorComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	UFilterActorComponent();

	// Called when the game starts
	virtual void BeginPlay() override;
	
	// Called every frame
	virtual void TickComponent( float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction ) override;

	virtual void OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID) { }
	virtual void OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID) { }
	virtual void SetPosition(const FVector& position, int32 parentID) { }
	virtual void SetDirection(const FVector& direction, int32 parentID) { }
	virtual void SpeedChangedNotify(float speed) { }
	virtual void InitFilter(UAvatarActorComponent* _comp) { GameObjComponent(_comp); }
	virtual void OnGotParentEntity(KBEngine::Entity* parentEnt) { }
	virtual void OnLoseParentEntity() { }



	FORCEINLINE UAvatarActorComponent* GameObjComponent()
	{
		return mActorComponent;
	}

	FORCEINLINE void GameObjComponent(UAvatarActorComponent* _comp)
	{
		mActorComponent = _comp;
	}

private:
	UAvatarActorComponent* mActorComponent = nullptr;
};
