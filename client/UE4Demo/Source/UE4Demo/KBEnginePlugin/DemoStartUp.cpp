// Fill out your copyright notice in the Description page of Project Settings.
#include "DemoStartUp.h"
#include "UE4Demo.h"
#include "LoginServerMgr.h"


ADemoStartUp* ADemoStartUp::instance = nullptr;

// Sets default values
ADemoStartUp::ADemoStartUp()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
}

ADemoStartUp::~ADemoStartUp()
{
	ADemoStartUp::instance = nullptr;
}

void ADemoStartUp::PreInitializeComponents()
{
	Super::PreInitializeComponents();

	KBE_ASSERT(!ADemoStartUp::instance);

	ADemoStartUp::instance = this;
}

// Called when the game starts or when spawned
void ADemoStartUp::BeginPlay()
{
	Super::BeginPlay();
	
	if (AutoConnectServer)
	{
		LoginServer();
	}
}

void ADemoStartUp::LoginServer()
{
	if (LoginServerMgr::Instance())
	{
		TArray<uint8> datas;
		LoginServerMgr::Instance()->LoginServer(LoginName, PassWord, datas);
	}
}

void ADemoStartUp::EndPlay(const EEndPlayReason::Type EndPlayReason)
{	
	Super::EndPlay(EndPlayReason);	
	ADemoStartUp::instance = nullptr;
}

void ADemoStartUp::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (LoginServerMgr::Instance())
		LoginServerMgr::Instance()->Process();
}

