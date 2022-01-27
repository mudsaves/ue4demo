// Fill out your copyright notice in the Description page of Project Settings.
#include "UE4DemoGameMode.h"
#include "UE4Demo.h"
#include "KBEngine.h"
#include "KBEnginePlugin/World.h"
#include "KBEnginePlugin/DemoStartUp.h"

void AUE4DemoGameMode::GetSeamlessTravelActorList(bool bToEntry, TArray<class AActor*>& ActorList)
{
	Super::GetSeamlessTravelActorList(bToEntry, ActorList);
	//Keep GameMode to new level.
	//ActorList.Add(this);

	//Keep KBEClient to new level.
	ActorList.Add(ADemoStartUp::Instance());
	ActorList.Add(AKBEMain::Instance());

	//Keep Player's actor to new level.
	if (KBEngine::KBEngineApp::app != nullptr)
	{
		KBEngine::Entity* entity = KBEngine::KBEngineApp::app->Player();
		if (entity->Actor() != nullptr)
		{
			ActorList.Add(entity->Actor());
		}
	}
}

/**
* Called after a seamless level transition has been completed on the *new* GameMode.
*/
void AUE4DemoGameMode::PostSeamlessTravel()
{
	KBEngine::KBEWorld* kbeWorld = KBEngine::KBEWorld::Instance();
	if (kbeWorld != nullptr)
	{
		kbeWorld->CheckResourceLoadComplete();
	}

	if (ADemoStartUp::Instance())
	{
		UWorld* World = ADemoStartUp::Instance()->GetWorld();
		APlayerController* controller = UGameplayStatics::GetPlayerController(World, 0);
		if (controller != nullptr)
		{
			if (KBEngine::KBEngineApp::app != nullptr)
			{
				KBEngine::Entity* entity = KBEngine::KBEngineApp::app->Player();
				if (entity->Actor() != nullptr)
				{
					controller->Possess(Cast<APawn>(entity->Actor()));
				}
			}
		}
	}
}

