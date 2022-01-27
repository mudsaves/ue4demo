// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Engine/GameInstance.h"
#include "UEDemoGameInstance.generated.h"

/**
 * 
 */
UCLASS()
class UE4DEMO_API UUEDemoGameInstance : public UGameInstance
{
	GENERATED_BODY()
	
	virtual void Init() override;

public:
	UClass* AccountPawn() { return mAccountPawn; }
	UClass* MonsterPawn() { return mMonsterPawn; }
	UClass* MovePlatformPawn() { return mMovePlatformPawn; }

private:
	UClass* mAccountPawn = nullptr;
	UClass* mMonsterPawn = nullptr;
	UClass* mMovePlatformPawn = nullptr;
};
