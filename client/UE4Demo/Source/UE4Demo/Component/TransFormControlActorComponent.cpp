// Fill out your copyright notice in the Description page of Project Settings.
#include "TransFormControlActorComponent.h"
#include "UE4Demo.h"


// Sets default values for this component's properties
UTransFormControlActorComponent::UTransFormControlActorComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}

// Called every frame
void UTransFormControlActorComponent::TickComponent( float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction )
{
	Super::TickComponent( DeltaTime, TickType, ThisTickFunction );

	if (mEntity)
	{
		//每tick都把坐标同步到底层，以便底层能同步最新的位置信息到其它人身上
		FVector direction = FVector::ZeroVector;
		direction.Z = GetOwner()->GetActorRotation().Euler().Z;
		mEntity->UpdateVolatileDataToServer(GetOwner()->GetActorLocation(), direction);
	}
}

