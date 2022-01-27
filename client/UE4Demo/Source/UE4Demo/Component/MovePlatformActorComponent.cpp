// Fill out your copyright notice in the Description page of Project Settings.
#include "MovePlatformActorComponent.h"
#include "UE4Demo.h"
#include "KBEnginePlugin/MovePlatform.h"
#include "KBEnginePlugin/Filter/AvatarFilterActorComponent.h"
#include "Component/AccountActorComponent.h"
#include "Animation/AnimInstance.h"


// Sets default values for this component's properties
UMovePlatformActorComponent::UMovePlatformActorComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = false;

	// ...
}

void UMovePlatformActorComponent::__init__(KBEngine::Entity* _entity)
{
	Super::__init__(_entity);

	entity(_entity);	
	mAvatarFilterComp = NewObject<UAvatarFilterActorComponent>(Cast<APawn>(_entity->Actor()), "AvatarFilter", RF_NoFlags, nullptr, false, nullptr);
	
	if (mAvatarFilterComp)
	{
		filterComponent(mAvatarFilterComp);
		Cast<APawn>(_entity->Actor())->AddInstanceComponent(filterComponent());
		filterComponent()->RegisterComponent();
		filterComponent()->InitFilter(this);
	}
}

void UMovePlatformActorComponent::SetPosition(const FVector& newVal)
{
	Super::SetPosition(newVal);

	if (filterComponent() != nullptr)
	{
		// 对于AvatarFilter来说，任何时候都应该只传递本地坐标
		filterComponent()->SetPosition(entity()->LocalPosition(), entity()->ParentID());
	}
}

void UMovePlatformActorComponent::SetDirection(const FVector& newVal)
{
	Super::SetDirection(newVal);

	if (filterComponent() != nullptr)
	{
		// 对于AvatarFilter来说，任何时候都应该只传递本地坐标
		filterComponent()->SetDirection(entity()->LocalDirection(), entity()->ParentID());
	}
}

void UMovePlatformActorComponent::onUpdateVolatileData(const FVector& position, const FVector& direction)
{
	Super::onUpdateVolatileData(position, direction);
}

void UMovePlatformActorComponent::OnFilterSpeedChanged(float speed)
{
	Super::OnFilterSpeedChanged(speed);
	USkeletalMeshComponent* skeletalMeshComponent = entity()->Actor()->FindComponentByClass<USkeletalMeshComponent>();

	if (speed > 0)
	{
		if (skeletalMeshComponent)
		{
			UAnimInstance* animInstance = skeletalMeshComponent->GetAnimInstance();
			UFunction* functionName = animInstance->FindFunction(TEXT("SetRun"));
			bool value = true;
			if (functionName)
				animInstance->ProcessEvent(functionName, &value);
		}
	}
	else
	{
		if (skeletalMeshComponent)
		{
			UAnimInstance* animInstance = skeletalMeshComponent->GetAnimInstance();
			UFunction* functionName = animInstance->FindFunction(TEXT("SetRun"));
			bool value = false;
			if (functionName)
				animInstance->ProcessEvent(functionName, &value);
		}
	}
}

void UMovePlatformActorComponent::OnControlled(bool isControlled)
{
	if (isControlled)
	{
		if (filterComponent())
		{
			filterComponent()->SetComponentTickEnabled(false);
		}

		if (mDumbFilterComp)
		{
			filterComponent(mDumbFilterComp);
			mDumbFilterComp->SetComponentTickEnabled(true);
		}
		else
		{
			mDumbFilterComp = NewObject<UDumbFilterActorComponent>(GetOwner(), "DumbFilter", RF_NoFlags, nullptr, false, nullptr);
			if (mDumbFilterComp != nullptr)
			{
				filterComponent(mDumbFilterComp);
				GetOwner()->AddInstanceComponent(mDumbFilterComp);
				mDumbFilterComp->RegisterComponent();
				mDumbFilterComp->InitFilter(this);
			}
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
			mTransFormControlComp->SetComponentTickEnabled(false);
		}
	}
	else
	{
		if (mDumbFilterComp)
		{
			mDumbFilterComp->SetComponentTickEnabled(false);
		}

		if (mAvatarFilterComp)
		{
			filterComponent(mAvatarFilterComp);
			filterComponent()->SetComponentTickEnabled(true);
		}

		if (mTransFormControlComp)
		{
			mTransFormControlComp->SetComponentTickEnabled(false);
		}
	}
}

void UMovePlatformActorComponent::OnActorEnterParentHandleBox(AActor* TargetActor)
{
	UAccountActorComponent* pComponent = TargetActor->FindComponentByClass<UAccountActorComponent>();
	if (pComponent != nullptr)
	{
		KBEngine::Entity* accountEntity = pComponent->entity();
		if (accountEntity != nullptr && accountEntity->IsPlayer()) 
		{
			KBEngine::FVariantArray args;
			args.Add(FVariant(entity()->ID()));
			pComponent->entity()->CellCall(TEXT("requestAddParent"), args);
		}
	}
}

void UMovePlatformActorComponent::OnActorLeaveParentHandleBox(AActor* TargetActor)
{
	UAccountActorComponent* pComponent = TargetActor->FindComponentByClass<UAccountActorComponent>();
	if (pComponent != nullptr)
	{
		KBEngine::Entity* accountEntity = pComponent->entity();
		if (accountEntity != nullptr && accountEntity->IsPlayer())
		{
			if (KBEngine::KBEngineApp::app->pBaseApp()->NetworkIsValid())
			{
				KBEngine::FVariantArray args;
				args.Add(FVariant(entity()->ID()));
				pComponent->entity()->CellCall(TEXT("requestRemoveParent"), args);
			}
		}
	}

}
