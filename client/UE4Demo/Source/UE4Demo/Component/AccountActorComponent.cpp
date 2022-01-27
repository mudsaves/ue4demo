// Fill out your copyright notice in the Description page of Project Settings.
#include "AccountActorComponent.h"
#include "UE4Demo.h"
#include "KBEnginePlugin/Account.h"
#include "KBEnginePlugin/Filter/DumbFilterActorComponent.h"
#include "KBEnginePlugin/Filter/AvatarFilterActorComponent.h"


// Sets default values for this component's properties
UAccountActorComponent::UAccountActorComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = false;

	// ...
}

void UAccountActorComponent::__init__(KBEngine::Entity* _entity)
{
	Super::__init__(_entity);
	entity(_entity);

	if (_entity->IsPlayer())
	{
		int id = _entity->ID();
		filterComponent(NewObject<UDumbFilterActorComponent>(GetOwner(), "DumbFilter", RF_NoFlags, nullptr, false, nullptr));
		if (filterComponent() != nullptr)
		{
			GetOwner()->AddInstanceComponent(filterComponent());
			filterComponent()->RegisterComponent();
			filterComponent()->InitFilter(this);
		}

		mTransFormControlComp = NewObject<UTransFormControlActorComponent>(GetOwner(), "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
		if (mTransFormControlComp != nullptr)
		{
			GetOwner()->AddInstanceComponent(mTransFormControlComp);
			mTransFormControlComp->RegisterComponent();
			mTransFormControlComp->Init(entity());
		}
	}
	else
	{
		filterComponent(NewObject<UAvatarFilterActorComponent>(GetOwner(), "AvatarFilter", RF_NoFlags, nullptr, false, nullptr));
		if (filterComponent() != nullptr)
		{
			GetOwner()->AddInstanceComponent(filterComponent());
			filterComponent()->RegisterComponent();
			filterComponent()->InitFilter(this);
		}
	}

	SetMoveSpeed();
}
//
void UAccountActorComponent::SetPosition(const FVector& oldVal)
{
	Super::SetPosition(oldVal);

	if (filterComponent() != nullptr)
	{
		filterComponent()->SetPosition(oldVal, entity()->ParentID());
	}
}

void UAccountActorComponent::SetDirection(const FVector& oldVal)
{
	Super::SetDirection(oldVal);

	if (filterComponent() != nullptr)
	{
		filterComponent()->SetDirection(oldVal, entity()->ParentID());
	}
}

void UAccountActorComponent::onUpdateVolatileData(const FVector& position, const FVector& direction)
{
	Super::onUpdateVolatileData(position, direction);
}

void UAccountActorComponent::SetMoveSpeed()
{
	Super::SetMoveSpeed();

	UActorComponent* component = entity()->Actor()->GetComponentByClass(UCharacterMovementComponent::StaticClass());
	UCharacterMovementComponent* movementComponent = Cast<UCharacterMovementComponent>(component);
	if (movementComponent != nullptr)
	{
		movementComponent->MaxWalkSpeed = static_cast<Account*>(entity())->MoveSpeed();
	}
}

void UAccountActorComponent::OnFilterSpeedChanged(float speed)
{
	Super::OnFilterSpeedChanged(speed);

	//开始播放run动画
	if (speed > 0)
	{
		if (entity()->Actor() != nullptr)
		{
			//Cast<ACharacter>(entity()->Actor())->GetMesh()->Play(true);
		}
	}
	//停止run动画
	else
	{
		if (entity()->Actor() != nullptr)
		{
			//Cast<ACharacter>(entity()->Actor())->GetMesh()->Stop();
		}
	}
}

void UAccountActorComponent::OnControlled(bool isControlled)
{
	if (this->filterComponent())
	{
		this->filterComponent()->DestroyComponent();
		this->filterComponent(nullptr);
	}
	
	if (entity()->IsPlayer())
	{
		if (isControlled)
		{
			filterComponent(NewObject<UAvatarFilterActorComponent>(GetOwner(), "AvatarFilter", RF_NoFlags, nullptr, false, nullptr));
			if (filterComponent() != nullptr)
			{
				GetOwner()->AddInstanceComponent(filterComponent());
				filterComponent()->RegisterComponent();
				filterComponent()->InitFilter(this);
			}

			if (mTransFormControlComp)
			{
				mTransFormControlComp->SetComponentTickEnabled(false);
			}
		}
		else
		{
			filterComponent(NewObject<UDumbFilterActorComponent>(GetOwner(), "DumbFilter", RF_NoFlags, nullptr, false, nullptr));
			if (filterComponent() != nullptr)
			{
				GetOwner()->AddInstanceComponent(filterComponent());
				filterComponent()->RegisterComponent();
				filterComponent()->InitFilter(this);
			}

			if (mTransFormControlComp)
			{
				mTransFormControlComp->SetComponentTickEnabled(true);
			}
		}
	}
	else
	{
		if (isControlled)
		{
			filterComponent(NewObject<UDumbFilterActorComponent>(GetOwner(), "DumbFilter", RF_NoFlags, nullptr, false, nullptr));
			if (filterComponent() != nullptr)
			{
				GetOwner()->AddInstanceComponent(filterComponent());
				filterComponent()->RegisterComponent();
				filterComponent()->InitFilter(this);
			}

			if (mTransFormControlComp == nullptr)
			{
				mTransFormControlComp = NewObject<UTransFormControlActorComponent>(GetOwner(), "TransFormControl", RF_NoFlags, nullptr, false, nullptr);
				if (mTransFormControlComp != nullptr)
				{
					GetOwner()->AddInstanceComponent(mTransFormControlComp);
					mTransFormControlComp->RegisterComponent();
					mTransFormControlComp->Init(entity());
				}
			}
			else
			{
				mTransFormControlComp->SetComponentTickEnabled(true);
			}
		}
		else
		{
			filterComponent(NewObject<UAvatarFilterActorComponent>(GetOwner(), "AvatarFilter", RF_NoFlags, nullptr, false, nullptr));
			if (filterComponent() != nullptr)
			{
				GetOwner()->AddInstanceComponent(filterComponent());
				filterComponent()->RegisterComponent();
				filterComponent()->InitFilter(this);
			}

			if (mTransFormControlComp)
			{
				mTransFormControlComp->SetComponentTickEnabled(false);
			}
		}
	}
}