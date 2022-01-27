#include "Monster.h"
#include "UE4Demo.h"
#include "UEDemoGameInstance.h"
#include "Component/MonsterActorComponent.h"
#include "World.h"
#include "DemoStartUp.h"

KBE_BEGIN_ENTITY_METHOD_MAP(Monster, Avatar)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(Monster, Avatar)
DECLARE_PROPERTY_CHANGED_NOTIFY(moveSpeed, &Monster::set_moveSpeed, float)
KBE_END_ENTITY_PROPERTY_MAP()

Monster::Monster()
{
	//UE_LOG(LogKbeClient, Error, TEXT("Monster entity created"));
}


Monster::~Monster()
{
}

void Monster::OnEnterWorld()
{
	Supper::OnEnterWorld();
	mMoveSpeed = (float)GetDefinedProperty("moveSpeed");

	KBEngine::KBEWorld* kbeWorld = KBEngine::KBEWorld::Instance();
	if (kbeWorld != nullptr)
	{
		kbeWorld->RequestEnterScenes(this);
	}

	KBEngine::FVariantArray params;
	params.Add(FVariant(ID()));
	KBEngine::KBEEvent::Instance()->AsyncFire("OnMonsterEnterWorld2", params);
	KBEngine::KBEEvent::Instance()->Fire("OnMonsterEnterWorld", params);
}

void Monster::OnEnterScenes()
{
	Supper::OnEnterScenes();

	UUEDemoGameInstance* gameInstance = Cast<UUEDemoGameInstance>(ADemoStartUp::Instance()->GetWorld()->GetGameInstance());
	if (gameInstance != nullptr)
	{
		UWorld* world = ADemoStartUp::Instance()->GetWorld();
		UClass* uls = gameInstance->MonsterPawn();

		if (world != nullptr && uls != nullptr)
		{
			Actor(world->SpawnActor<APawn>(uls, FTransform(FQuat::MakeFromEuler(Direction()), Position())));
			if (Actor() != nullptr)
			{
				Actor()->SetActorLabel(FString("Entity(") + FString::FromInt(ID()) + FString(")"));
				Cast<APawn>(Actor())->SpawnDefaultController();
				mComponent = NewObject<UMonsterActorComponent>(Cast<APawn>(Actor()), "MonsterActorComponent", RF_NoFlags, nullptr, false, nullptr);
				Cast<APawn>(Actor())->AddInstanceComponent(mComponent);
				mComponent->RegisterComponent();
				Cast<UMonsterActorComponent>(mComponent)->__init__(this);
			}
		}
	}
}

void Monster::OnLeaveWorld()
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

void Monster::OnEnterSpace()
{
	Supper::OnEnterSpace();
}

void Monster::OnLeaveSpace()
{
	Supper::OnLeaveSpace();
}

void Monster::Set_Position(const FVector& oldVal)
{
	Supper::Set_Position(oldVal);

	if (mComponent != nullptr)
	{
		Cast<UMonsterActorComponent>(mComponent)->SetPosition(Position());
	}
}

void Monster::Set_Direction(const FVector& oldVal)
{
	Supper::Set_Direction(oldVal);

	if (mComponent != nullptr)
	{
		Cast<UMonsterActorComponent>(mComponent)->SetDirection(Direction());
	}
}

void Monster::OnUpdateVolatileData()
{
	Supper::OnUpdateVolatileData();

	if (mComponent != nullptr)
	{
		Cast<UMonsterActorComponent>(mComponent)->onUpdateVolatileData(LocalPosition(), LocalDirection());
	}
}

void Monster::set_moveSpeed(const float &nv, const float &ov)
{
	mMoveSpeed = nv;
}