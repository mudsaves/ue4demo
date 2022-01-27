#pragma once

#include "KBEngine.h"
#include "Vector.h"
#include "Avatar.h"

namespace KBEngine
{
	class KBEWorld
	{
	public:
		void LoadSceneAsyc(const FString& level);
		void OnSetSpaceData(uint32 spaceID, const FString& key, const FString& value);

		FORCEINLINE bool IsLoadComplete()
		{
			return mIsLoadComplete;
		}

		FORCEINLINE void IsLoadComplete(bool isLoad)
		{
			mIsLoadComplete = isLoad;
		}

		void RequestEnterScenes(Avatar* obj);
		void RequestLeaveScenes(Avatar* obj);
		void CheckResourceLoadComplete();

	public:
		static void Register(KBEWorld * inst);
		static void Deregister();
		FORCEINLINE static KBEWorld* Instance() { return instance_; }

	private:
		std::vector<Avatar*> mWaitingEnterScenes;
		bool mIsLoadComplete = false;		

	private:
		static KBEWorld* instance_;
	};
}