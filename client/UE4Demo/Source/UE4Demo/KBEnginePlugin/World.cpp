#include "World.h"
#include "UE4Demo.h"
#include "DemoStartUp.h"

namespace KBEngine
{
	KBEWorld* KBEWorld::instance_ = nullptr;

	void KBEWorld::Register(KBEWorld * inst)
	{
		KBE_ASSERT(instance_ == nullptr);
		instance_ = inst;
	}

	void KBEWorld::Deregister()
	{
		if (instance_)
			instance_ = nullptr;
	}

	void KBEWorld::OnSetSpaceData(uint32 spaceID, const FString& key, const FString& value)
	{
		if (key == "MetaClass")
		{
			LoadSceneAsyc(value);
		}
		else
		{

		}
	}

	void KBEWorld::LoadSceneAsyc(const FString& level)
	{
		IsLoadComplete(false);

		if (level == "1")
		{
			UWorld* w = ADemoStartUp::Instance()->GetWorld();
			FString StartStr = FString::Printf(TEXT("/Game/Maps/L_Map_1"));
			w->SeamlessTravel(StartStr, true);
		}
		if (level == "2")
		{
			UWorld* w = ADemoStartUp::Instance()->GetWorld();
			FString StartStr = FString::Printf(TEXT("/Game/Maps/L_Map_2"));
			w->SeamlessTravel(StartStr, true);
		}
	}

	/// <summary>
	/// 请求进入地图，此接口会把请求者放入队列中，如果地图加载完成，则会回调请求者的OnEnterScenes()接口
	/// </summary>
	/// <param name="obj"></param>
	void KBEWorld::RequestEnterScenes(Avatar* obj)
	{
		if (IsLoadComplete())
		{
				obj->OnEnterScenes();
		}
		else
		{
			mWaitingEnterScenes.push_back(obj);
		}
	}

	void KBEWorld::RequestLeaveScenes(Avatar* obj)
	{
		if (IsLoadComplete())
		{
			return;
		}

		std::vector<Avatar*>::iterator _iter = mWaitingEnterScenes.begin();
		for (; _iter != mWaitingEnterScenes.end(); _iter++)
		{
			if (*_iter == obj)
				mWaitingEnterScenes.erase(_iter);
		}
	}

	void KBEWorld::CheckResourceLoadComplete()
	{
		IsLoadComplete(true);

		std::vector<Avatar*>::iterator _iter = mWaitingEnterScenes.begin();
		for (; _iter != mWaitingEnterScenes.end(); _iter++)
		{
			(*_iter)->OnEnterScenes();
		}

		mWaitingEnterScenes.clear();
	}
}