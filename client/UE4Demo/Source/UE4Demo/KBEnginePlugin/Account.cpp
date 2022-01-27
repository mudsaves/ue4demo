#include "Account.h"
#include "UE4Demo.h"
#include "Alias.h"
#include "UEDemoGameInstance.h"
#include "Component/AccountActorComponent.h"
#include "World.h"
#include "DemoStartUp.h"
#include "Json.h"
#include "LoginServerMgr.h"


KBE_BEGIN_ENTITY_METHOD_MAP(Account, Avatar)
	DECLARE_REMOTE_METHOD(onDBID,        &Account::onDBID, uint64)
	DECLARE_REMOTE_METHOD(onClientEvent, &Account::onClientEvent, int32)
	DECLARE_REMOTE_METHOD(testFixedDict, &Account::testFixedDict, const FVariant&)
	DECLARE_REMOTE_METHOD(testFixedDictT1, &Account::testFixedDictT1, const FVariant&)
	DECLARE_REMOTE_METHOD(testOther1, &Account::testOther1, float, FVariant, const FString&, const FVariant&)
	DECLARE_REMOTE_METHOD(testJson, &Account::testJson, FString)
	DECLARE_REMOTE_METHOD(testJson, &Account::testForNoParam)
	DECLARE_REMOTE_METHOD(notifyAcrossServer, &Account::notifyAcrossServer)
	DECLARE_REMOTE_METHOD(notifyAcrossServerBack, &Account::notifyAcrossServerBack)
	KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(Account, Avatar)
	DECLARE_PROPERTY_CHANGED_NOTIFY(moveSpeed, &Account::set_moveSpeed, float)
	DECLARE_PROPERTY_CHANGED_NOTIFY(testVal, &Account::set_testVal, uint32)
	DECLARE_PROPERTY_CHANGED_NOTIFY(floatValue, &Account::set_floatValue, float)
	DECLARE_PROPERTY_CHANGED_NOTIFY(strValue, &Account::set_strValue, FString)
	DECLARE_PROPERTY_CHANGED_NOTIFY(vector2Value, &Account::set_vector2Value, FVector2D)
	DECLARE_PROPERTY_CHANGED_NOTIFY(vectorValue, &Account::set_vector3Value, FVector)
	DECLARE_PROPERTY_CHANGED_NOTIFY(arrayof, &Account::set_arrayof, KBEngine::FVariantArray)
KBE_END_ENTITY_PROPERTY_MAP()



void Event_OnMonsterEnterWorldFun1(const KBEngine::FVariantArray& args);
void Event_OnMonsterEnterWorldFun2(const KBEngine::FVariantArray& args);


Account::Account()
{
	//FVariant arg(0);		
	//addDefinedProperty("testVal", arg);
	//UE_LOG(LogKbeClient, Error, TEXT("Account entity created"));

	auto* ent = KBEngine::KBEEvent::Instance();
	ent->Register(TEXT("OnMonsterEnterWorld"), this, &Account::Event_OnMonsterEnterWorld);
	ent->Register(TEXT("OnMonsterEnterWorld2"), &Event_OnMonsterEnterWorldFun1);
	ent->Register(TEXT("OnMonsterEnterWorld2"), &Event_OnMonsterEnterWorldFun2);
	ent->Register(TEXT("OnMonsterEnterWorld"), this, &Account::Event_OnMonsterEnterWorld); // 再次注册一次，仅仅是为了测试功能，演示用法
	ent->Register(TEXT("OnMonsterEnterWorld"), this, &Account::Event_OnMonsterEnterWorld2); // 再次注册一次，仅仅是为了测试功能，演示用法
}


Account::~Account()
{
	KBE_DEBUG(TEXT("Account::~Account()"));
	//KBEngine::KBEEvent::Instance()->Deregister(this);  // no efficiency
	KBEngine::KBEEvent::Instance()->Deregister(TEXT("OnMonsterEnterWorld2"), &Event_OnMonsterEnterWorldFun1);
	KBEngine::KBEEvent::Instance()->Deregister(TEXT("OnMonsterEnterWorld2"), &Event_OnMonsterEnterWorldFun2);
	KBEngine::KBEEvent::Instance()->Deregister(TEXT("OnMonsterEnterWorld"), this, &Account::Event_OnMonsterEnterWorld);
	KBEngine::KBEEvent::Instance()->Deregister(TEXT("OnMonsterEnterWorld"), this, &Account::Event_OnMonsterEnterWorld);
	KBEngine::KBEEvent::Instance()->Deregister(TEXT("OnMonsterEnterWorld"), this, &Account::Event_OnMonsterEnterWorld2);
}

void Account::OnEnterWorld()
{
	Supper::OnEnterWorld();
	
	mMoveSpeed = (float)GetDefinedProperty("moveSpeed");

	//我们在这里之所以要通过KBEWorld来进行，是因为UE4中，通过代码创建Actor时，需要GetWorld()，如果此时还在旧的场景中，创建出来的Actor会随着旧场景的销毁而销毁。
	//另外还有一种方法：Actor及时创建，但是如果是创建在旧的场景中，通过加入到传送Actor的list列表中，类似像主角一样传送过去（未测试过）
	//对于NPC，也是一样
	KBEngine::KBEWorld* kbeWorld = KBEngine::KBEWorld::Instance();
	if (kbeWorld != nullptr)
	{
		kbeWorld->RequestEnterScenes(this);
	}

	if (IsPlayer())
	{
		KBEngine::FVariantArray args;
		args.Add(FVariant(3343));
		BaseCall(TEXT("onBaseEvent"), args);
		CellCall(TEXT("onCellEvent"), args);

		args.Empty();
		args.Add(FVariant(4434));
		args.Add(FVariant(TEXT("测试")));
		
		ALIAS_ITEM item;
		item.amount = 1;
		item.flag.Add(11);
		item.flag.Add(12);
		item.id = 2;
		//item.misc = FString(TEXT("ITEM测试"));
		item.misc = FString(TEXT("ITEM - test"));
		item.uid = 3;
		KBEngine::FVariantMap out;
		item.ToFVariantMap(out);
		args.Add(FVariant(out));
		CellCall(TEXT("onCellEvent2"), args);

		/*
		// 测试复合数据类型
		KBEngine::FVariantArray args3;		// 参数列表，只会有一个array of dict

		// 构建 dict {"ddd": double}
		KBEngine::FVariantMap doubleDict1;
		KBEngine::FVariantMap doubleDict2;
		doubleDict1.Add(TEXT("ddd"), FVariant(123.44444));
		doubleDict2.Add(TEXT("ddd"), FVariant(996.66666));

		// 构建array of dict
		KBEngine::FVariantArray arrayofdict;
		arrayofdict.Add(FVariant(doubleDict1));
		arrayofdict.Add(FVariant(doubleDict2));

		args3.Add(FVariant(arrayofdict));
		CellCall(TEXT("onCellEvent3"), args3);
		*/
	}

	// KBEngine::KBEngineApp::app->FindEntity()用法示例
	//Entity* ent = KBEngine::KBEngineApp::app->FindEntity(123);

	// KBEngine::KBEngineApp::app->Entities()用法示例
	//auto* entities = KBEngine::KBEngineApp::app->Entities();
	//if (entities)
	//{
	//	Entity *const *p = entities->Find(123456);
	//	Entity* ent2 = p ? *p : nullptr;
	//}
}

void Account::OnEnterScenes()
{
	Supper::OnEnterScenes();

	UUEDemoGameInstance* gameInstance = Cast<UUEDemoGameInstance>(ADemoStartUp::Instance()->GetWorld()->GetGameInstance());
	if (gameInstance != nullptr)
	{
		UWorld* world = ADemoStartUp::Instance()->GetWorld();
		UClass* uls = gameInstance->AccountPawn();
		if (world != nullptr && uls != nullptr)
		{
			Actor(world->SpawnActor<APawn>(uls, FTransform(FQuat::MakeFromEuler(Direction()), Position())));
			if (Actor() != nullptr)
			{
				if (IsPlayer())
				{
					Actor()->SetActorLabel(FString("Player(") + FString::FromInt(ID()) + FString(")"));
					APlayerController* controller = UGameplayStatics::GetPlayerController(world, 0);
					if (controller != nullptr)
					{
						controller->Possess(Cast<APawn>(Actor()));
					}
				}
				else
				{
					Actor()->SetActorLabel(FString("PlayerEntity(") + FString::FromInt(ID()) + FString(")"));
					Cast<APawn>(Actor())->SpawnDefaultController();
				}

				mComponent = NewObject<UAccountActorComponent>(Cast<APawn>(Actor()), "AccountActorComponent");
				Cast<APawn>(Actor())->AddInstanceComponent(mComponent);
				Cast<UAccountActorComponent>(mComponent)->__init__(this);
				mComponent->RegisterComponent();

				Actor()->Tags.AddUnique(TEXT("Account"));
			}
		}
	}
}

void Account::OnLeaveWorld()
{
	Supper::OnLeaveWorld();

	//这里这样写，主要是防止在加载的过程中，其他玩家离开了，但是，由于在world中，我已经缓存了该请求，得把该请求给清理掉，对于NPC也是一样
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

void Account::notifyAcrossServer()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("reqLoginOffForAcross"), args);

	LoginServerMgr::Instance()->OnLoginOffForAcrossLogin();
}

void Account::notifyAcrossServerBack()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("reqLoginOffForAcrossBack"), args);

	LoginServerMgr::Instance()->OnLoginOffForAcrossLoginBack();
}

void Account::OnEnterSpace()
{
	Supper::OnEnterSpace();
}

void Account::OnLeaveSpace()
{
	Supper::OnLeaveSpace();
}

void Account::Set_Position(const FVector& oldVal)
{
	Supper::Set_Position(oldVal);

	if (mComponent != nullptr)
	{
		Cast<UAccountActorComponent>(mComponent)->SetPosition(Position());
	}
}

void Account::Set_Direction(const FVector& oldVal)
{
	Supper::Set_Direction(oldVal);

	if (mComponent != nullptr)
	{
		Cast<UAccountActorComponent>(mComponent)->SetDirection(Direction());
	}
}

void Account::OnUpdateVolatileData()
{
	Supper::OnUpdateVolatileData();

	if (mComponent != nullptr)
	{
		Cast<UAccountActorComponent>(mComponent)->onUpdateVolatileData(LocalPosition(), LocalDirection());
	}
}

void Account::onDBID(uint64 dbid)
{
	KBE_INFO(TEXT("Account::onDBID(), %d"), dbid);
}

void Account::onClientEvent(int32 val)
{
	KBE_INFO(TEXT("Account::onClientEvent(), %d"), val);
}

void Account::set_testVal(const uint32 &nv, const uint32 &ov)
{
	KBE_INFO(TEXT("Account::set_testVal(), new value %d, old value %d"), nv, ov);
}

void Account::set_floatValue(const float &nv, const float &ov)
{
	KBE_INFO(TEXT("Account::set_floatValue(), new value %f, old value %f"), nv, ov);
}

void Account::set_strValue(const FString &nv, const FString &ov)
{
	KBE_INFO(TEXT("Account::set_strValue(), new value %s, old value %s"), *nv, *ov);
}

void Account::set_vector2Value(const FVector2D &nv, const FVector2D &ov)
{
	KBE_INFO(TEXT("Account::set_vector2Value(), new value (%f, %f), old value (%f, %f)"), nv.X, nv.Y, ov.X, ov.Y);
}

void Account::set_vector3Value(const FVector &nv, const FVector &ov)
{
	KBE_INFO(TEXT("Account::set_vector3Value(), new value (%f, %f, %f), old value (%f, %f, %f)"), nv.X, nv.Y, nv.Z, ov.X, ov.Y, ov.Z);
}

void Account::set_arrayof(const KBEngine::FVariantArray& nv, const KBEngine::FVariantArray& ov)
{
	KBE_INFO(TEXT("Account::set_arrayof"));
}

void Account::testFixedDictT1(const FVariant& val)
{
	KBE_INFO(TEXT("Account::testFixedDictT1"));

	auto* inst = ALIAS_ITEM_T1::CreateFromVariant(val);
	KBE_INFO(TEXT("Account::testFixedDictT1: %s"), *inst->ToString());
	delete inst;
}

void Account::testFixedDict(const FVariant& val)
{
	KBE_INFO(TEXT("Account::testFixedDict"));

	auto* inst = ALIAS_ITEM::CreateFromVariant(val);
	KBE_INFO(TEXT("Account::testFixedDict: %s"), *inst->ToString());
	delete inst;

}

void Account::OnRemoteMethodCall(const FString &name, const TArray<FVariant> &args)
{
	Avatar::OnRemoteMethodCall(name, args);

	KBE_DEBUG(TEXT("Account::OnRemoteMethodCall, %s"), *name);
	if (name == TEXT("testFixedDict"))
	{
		KBE_DEBUG(TEXT("Account::RemoteMethodCall, 1 - %s"), *name);
	}
	else if (name == TEXT("testFixedDictT1"))
	{
		KBE_DEBUG(TEXT("Account::RemoteMethodCall, 2 -  %s"), *name);
	}
	else
	{

	}
}

void Account::set_moveSpeed(const float &nv, const float &ov)
{
	mMoveSpeed = nv;

	if (mComponent != nullptr)
	{
		Cast<UAccountActorComponent>(mComponent)->SetMoveSpeed();
	}
}


void Account::testOther1(float val1, FVariant val2, const FString& val3, const FVariant& val4)
{
	float v1 = val1;
	ALIAS_ITEM *v2 = ALIAS_ITEM::CreateFromVariant(val2);
	FString v3 = val3;
	TArray<int32> v4;

	auto vs = val4.GetValue<KBEngine::FVariantArray>();
	for (auto& itor : vs)
	{
		v4.Add(itor.GetValue<int32>());
	}

	int i = 0;
	FString v4Str;
	TArray<FStringFormatArg> arg;
	for (auto f : v4)
	{
		v4Str += FString::Printf(TEXT("{%u}, "), i++);
		arg.Add(f);
	}
	v4Str = FString::Format(*v4Str, arg);

	KBE_INFO(TEXT("Account::testOther1: v1: %f, v2: %s, v3: %s, v4: %s"), v1, *v2->ToString(), *v3, *v4Str);
	delete v2;
}

void Account::testJson(FString val)
{
	KBE_INFO(TEXT("Account::testJson: %s"), *val);

	TSharedRef< TJsonReader<> > Reader = TJsonReaderFactory<>::Create(val);
	TSharedPtr<FJsonObject> object;
	bool bSuccessful = FJsonSerializer::Deserialize(Reader, object);
	//KBE_ASSERT(bSuccessful);
	if (!bSuccessful)
	{
		KBE_ERROR(TEXT("parse json data fault"));
		return;
	}

	FJsonObject* jo = object.Get();
	KBE_INFO(TEXT("json -> 1 : %d"), jo->GetIntegerField("1"));
	KBE_INFO(TEXT("json -> a : %s"), *jo->GetStringField("a"));

	const TArray<TSharedPtr<FJsonValue>> &t = jo->GetArrayField("t");
	KBE_INFO(TEXT("json -> t : [%s, %d, %s]"), *t[0].Get()->AsString(), int(t[1].Get()->AsNumber()), *t[2].Get()->AsString());

	const TArray<TSharedPtr<FJsonValue>> &l = jo->GetArrayField("l");
	KBE_INFO(TEXT("ljson -> l : [%d, %s, %s]"), int(l[0].Get()->AsNumber()), *l[1].Get()->AsString(), *l[2].Get()->AsString());
}

void Account::testForNoParam()
{
	KBE_INFO(TEXT("Account::testForNoParam(), ......"));
}

void Account::Event_OnMonsterEnterWorld(const KBEngine::FVariantArray& args)
{
	auto id = args[0].GetValue<int32>();
	KBE_ERROR(TEXT("Account::Event_OnMonsterEnterWorld: %d"), id);
}

void Account::Event_OnMonsterEnterWorld2(const KBEngine::FVariantArray& args)
{
	auto id = args[0].GetValue<int32>();
	KBE_ERROR(TEXT("Account::Event_OnMonsterEnterWorld: 2 - %d"), id);
}

void Event_OnMonsterEnterWorldFun1(const KBEngine::FVariantArray& args)
{
	auto id = args[0].GetValue<int32>();
	KBE_ERROR(TEXT("normal function ::Event_OnMonsterEnterWorldFun1: %d"), id);
}

void Event_OnMonsterEnterWorldFun2(const KBEngine::FVariantArray& args)
{
	auto id = args[0].GetValue<int32>();
	KBE_ERROR(TEXT("normal function ::Event_OnMonsterEnterWorldFun2: %d"), id);
}
