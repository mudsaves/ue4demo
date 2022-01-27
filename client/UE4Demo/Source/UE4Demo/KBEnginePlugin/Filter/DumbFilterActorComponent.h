// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "FilterActorComponent.h"
#include "DumbFilterActorComponent.generated.h"

/**
 * 一个直接改变对象位置的过滤器，可用于传送等非移动引起的位置位置改变
 */
UCLASS()
class UE4DEMO_API UDumbFilterActorComponent : public UFilterActorComponent
{	
	GENERATED_BODY()

	typedef UFilterActorComponent Supper;

	UDumbFilterActorComponent();

	// Called when the game starts
	virtual void BeginPlay() override;

	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

public:
	virtual void OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID) override;
	virtual void SetPosition(const FVector& position, int32 parentID) override;
	virtual void SetDirection(const FVector& direction, int32 parentID) override;
	virtual void OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID) override;

};
