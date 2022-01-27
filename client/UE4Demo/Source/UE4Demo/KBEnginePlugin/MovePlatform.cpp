#include "MovePlatform.h"
#include "UE4Demo.h"
#include "UEDemoGameInstance.h"
#include "Component/MovePlatformActorComponent.h"
#include "World.h"
#include "DemoStartUp.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MovePlatform, Avatar)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovePlatform, Avatar)
DECLARE_PROPERTY_CHANGED_NOTIFY(moveSpeed, &MovePlatform::set_moveSpeed, float)
KBE_END_ENTITY_PROPERTY_MAP()

MovePlatform::MovePlatform()
{
	//UE_LOG(LogKbeClient, Error, TEXT("MovePlatform entity created"));
}


MovePlatform::~MovePlatform()
{
}

void MovePlatform::OnEnterWorld()
{
	Supper::OnEnterWorld();
	mMoveSpeed = (float)GetDefinedProperty("moveSpeed");

	KBEngine::KBEWorld* kbeWorld = KBEngine::KBEWorld::Instance();
	if (kbeWorld != nullptr)
	{
		kbeWorld->RequestEnterScenes(this);
	}

	//KBEngine::FVariantArray params;
	//params.Add(FVariant(ID()));
	//KBEngine::KBEEvent::Instance()->AsyncFire("OnMonsterEnterWorld2", params);
	//KBEngine::KBEEvent::Instance()->Fire("OnMonsterEnterWorld", params);
}

void MovePlatform::OnEnterScenes()
{
	Supper::OnEnterScenes();

	UUEDemoGameInstance* gameInstance = Cast<UUEDemoGameInstance>(ADemoStartUp::Instance()->GetWorld()->GetGameInstance());
	if (gameInstance != nullptr)
	{
		UWorld* world = ADemoStartUp::Instance()->GetWorld();
		UClass* uls = gameInstance->MovePlatformPawn();

		if (world != nullptr && uls != nullptr)
		{
			Actor(world->SpawnActor<APawn>(uls, FTransform(FQuat::MakeFromEuler(Direction()), Position())));
			if (Actor() != nullptr)
			{
				Actor()->SetActorLabel(FString("Entity(") + FString::FromInt(ID()) + FString(")"));
				Cast<APawn>(Actor())->SpawnDefaultController();
				mComponent = NewObject<UMovePlatformActorComponent>(Cast<APawn>(Actor()), "MovePlatformActorComponent", RF_NoFlags, nullptr, false, nullptr);
				Cast<APawn>(Actor())->AddInstanceComponent(mComponent);
				mComponent->RegisterComponent();
				Cast<UMovePlatformActorComponent>(mComponent)->__init__(this);
			}
		}
	}
}

void MovePlatform::OnLeaveWorld()
{
	Supper::OnLeaveWorld();
	
	KBEngine::KBEWorld* kbeWorld = KBEngine::KBEWorld::Instance();
	if (kbeWorld != nullptr)
	{
		kbeWorld->RequestLeaveScenes(this);
	}

	if (Actor() != nullptr)
	{
		Actor()->Destroy();
		Actor(nullptr);
	}
}

void MovePlatform::OnEnterSpace()
{
	Supper::OnEnterSpace();
}

void MovePlatform::OnLeaveSpace()
{
	Supper::OnLeaveSpace();
}

void MovePlatform::Set_Position(const FVector& oldVal)
{
	Supper::Set_Position(oldVal);

	if (mComponent != nullptr)
	{
		Cast<UMovePlatformActorComponent>(mComponent)->SetPosition(Position());
	}
}

void MovePlatform::Set_Direction(const FVector& oldVal)
{
	Supper::Set_Direction(oldVal);

	if (mComponent != nullptr)
	{
		Cast<UMovePlatformActorComponent>(mComponent)->SetDirection(Direction());
	}
}

void MovePlatform::OnUpdateVolatileData()
{
	Supper::OnUpdateVolatileData();

	if (mComponent != nullptr)
	{
		Cast<UMovePlatformActorComponent>(mComponent)->onUpdateVolatileData(LocalPosition(), LocalDirection());
	}
}

void MovePlatform::set_moveSpeed(const float &nv, const float &ov)
{
	mMoveSpeed = nv;
}