// Fill out your copyright notice in the Description page of Project Settings.
#include "AvatarActorComponent.h"
#include "UE4Demo.h"



// Sets default values for this component's properties
UAvatarActorComponent::UAvatarActorComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


// Called when the game starts
void UAvatarActorComponent::BeginPlay()
{
	Super::BeginPlay();

	// ...
	
}


// Called every frame
void UAvatarActorComponent::TickComponent( float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction )
{
	Super::TickComponent( DeltaTime, TickType, ThisTickFunction );

	// ...
}

void UAvatarActorComponent::OnGotParentEntity()
{
	if (filterComponent())
		filterComponent()->OnGotParentEntity(entity()->Parent());
}

void UAvatarActorComponent::OnLoseParentEntity()
{
	if (filterComponent())
		filterComponent()->OnLoseParentEntity();
}

void UAvatarActorComponent::onUpdateVolatileData(const FVector& position, const FVector& direction)
{
	// 如果不在地上
	if (!entity()->IsOnGround())
	{
		if (filterComponent() != nullptr)
		{
			// 对于AvatarFilter来说，任何时候都应该只传递本地坐标
			filterComponent()->OnUpdateVolatileData(entity()->LocalPosition(), entity()->LocalDirection(), entity()->ParentID());
		}
		return;
	}

	// 在地上
	// 高度需要根据Entity自己的Actor的当前高度重新碰撞得到
	auto pos = GetOwner()->GetActorLocation();
	FVector newPos(position.X, position.Y, pos.Z);

	FHitResult hitResult(ForceInit);
	FCollisionQueryParams ccq(FName(TEXT("MovePositionTrace")), true, NULL);
	ccq.bTraceComplex = true;
	ccq.bReturnPhysicalMaterial = false;
	ccq.AddIgnoredActor(GetOwner());

	FVector posB(newPos.X, newPos.Y, newPos.Z + 120.0);  // 把高度提高1.2米
	FVector posE(newPos.X, newPos.Y, newPos.Z - 500.0);  // 把高度降低5米

	if (GetWorld()->LineTraceSingleByChannel(hitResult, posB, posE, ECC_WorldStatic, ccq))
		newPos = hitResult.Location;

	if (filterComponent() != nullptr)
	{
		filterComponent()->OnUpdateVolatileData(newPos, direction, entity()->ParentID());
	}
}

void UAvatarActorComponent::OnUpdateVolatileDataByParent()
{
	if (filterComponent())
		filterComponent()->OnUpdateVolatileDataByParent(entity()->Position(), entity()->Direction(), entity()->ParentID());
}

void UAvatarActorComponent::FixOnGroundPosition(FVector& position, bool ignoreNotOnGround)
{
	// 如果不在地上
	if (ignoreNotOnGround && !entity()->IsOnGround())
		return;

	FVector newPos;
	if (entity()->IsOnGround()) 
	{
		// 在地上
		// 高度需要根据Entity自己的Actor的当前高度重新碰撞得到
		auto pos = GetOwner()->GetActorLocation();
		newPos = FVector(position.X, position.Y, pos.Z);
	}
	else 
	{
		newPos = FVector(position.X, position.Y, position.Z);
	}

	FHitResult hitResult(ForceInit);
	FCollisionQueryParams ccq(FName(TEXT("MovePositionTrace")), true, NULL);
	ccq.bTraceComplex = true;
	ccq.bReturnPhysicalMaterial = false;
	ccq.AddIgnoredActor(GetOwner());

	FVector posB(newPos.X, newPos.Y, newPos.Z + 120.0);  // 把高度提高1.2米
	FVector posE(newPos.X, newPos.Y, newPos.Z - 500.0);  // 把高度降低5米

	if (GetWorld()->LineTraceSingleByChannel(hitResult, posB, posE, ECC_WorldStatic, ccq))
		newPos = hitResult.Location;
		newPos.Z += 100;  // 因为怪物的中心点在腰上，因此对于2米高的怪物而言，需要提高1米

	position = newPos;
}
