// Fill out your copyright notice in the Description page of Project Settings.
#include "UEDemoGameInstance.h"
#include "UE4Demo.h"




void UUEDemoGameInstance::Init()
{
	mAccountPawn = LoadClass<APawn>(NULL, TEXT("Blueprint'/Game/BluePrints/BP_Player.BP_Player_C'"));
	mMonsterPawn = LoadClass<APawn>(NULL, TEXT("Blueprint'/Game/BluePrints/BP_Monster.BP_Monster_C'"));
	mMovePlatformPawn = LoadClass<APawn>(NULL, TEXT("Blueprint'/Game/BluePrints/MovePlatform.MovePlatform_C'"));
}
