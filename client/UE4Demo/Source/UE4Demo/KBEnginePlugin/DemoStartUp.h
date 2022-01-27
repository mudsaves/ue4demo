// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "KBEngine.h"
#include "GameFramework/Actor.h"
#include "DemoStartUp.generated.h"

UCLASS()
class UE4DEMO_API ADemoStartUp : public AActor
{
	GENERATED_BODY()

	static ADemoStartUp* instance;

public:
	static ADemoStartUp* Instance()
	{
		return ADemoStartUp::instance;
	}

	// Sets default values for this actor's properties
	ADemoStartUp();
	~ADemoStartUp();

	virtual void PreInitializeComponents() override;

	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	virtual void Tick(float DeltaSeconds) override;

private:
	void LoginServer();

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool AutoConnectServer = false;	

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString LoginName = "TEST";

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString PassWord = "123456";
};
