// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameFramework/GameMode.h"
#include "UE4DemoGameMode.generated.h"

/**
 * 
 */
UCLASS()
class UE4DEMO_API AUE4DemoGameMode : public AGameMode
{
	GENERATED_BODY()
	
	
	virtual void GetSeamlessTravelActorList(bool bToEntry, TArray<class AActor*>& ActorList) override;
	virtual void PostSeamlessTravel() override;
	
};
