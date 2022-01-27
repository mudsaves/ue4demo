// Fill out your copyright notice in the Description page of Project Settings.
#include "DumbFilterActorComponent.h"
#include "UE4Demo.h"
#include "KBEngine.h"
#include "Component/AvatarActorComponent.h"

UDumbFilterActorComponent::UDumbFilterActorComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = false;	
}

// Called when the game starts
void UDumbFilterActorComponent::BeginPlay()
{
	Super::BeginPlay();

	// ...
}


// Called every frame
void UDumbFilterActorComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	// ...
}

void UDumbFilterActorComponent::OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID)
{
	FVector dir(0, 0, direction.Z); // 我们只想同步Y轴（朝向）
	FQuat quat = FQuat::MakeFromEuler(dir);
	GetOwner()->SetActorLocationAndRotation(position, quat);
}

void UDumbFilterActorComponent::SetPosition(const FVector& position, int32 parentID)
{
	GetOwner()->SetActorLocation(position);
}

void UDumbFilterActorComponent::SetDirection(const FVector& direction, int32 parentID)
{
	FQuat quat = FQuat::MakeFromEuler(direction);
	GetOwner()->SetActorRotation(quat);
}

void UDumbFilterActorComponent::OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID)
{
	//auto entity = GameObjComponent()->entity();
	//auto locPos = entity->LocalPosition();
	//KBE_DEBUG(TEXT("UDumbFilterActorComponent::OnUpdateVolatileDataByParent, parent %d, pos (%f, %f, %f), locPos (%f, %f, %f)"), parentID, position.X, position.Y, position.Z, locPos.X, locPos.Y, locPos.Z);
	auto entity = GameObjComponent()->entity();
	if (entity == nullptr || entity->IsPlayer()) 
	{
		return;
	}
	GetOwner()->SetActorLocation(position);
	FQuat quat = FQuat::MakeFromEuler(direction);
	GetOwner()->SetActorRotation(quat);
}


