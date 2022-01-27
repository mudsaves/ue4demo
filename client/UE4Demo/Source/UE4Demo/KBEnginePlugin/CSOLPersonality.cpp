#include "CSOLPersonality.h"
#include "UE4Demo.h"
#include "World.h"
#include "LoginServerMgr.h"

using namespace KBEngine;

void CSOLPersonality::OnSetSpaceData(uint32 spaceID, const FString &key, const FString &value)
{
	KBE_ERROR(TEXT("CSOLPersonality::OnSetSpaceData: spaceID: %u, key: %s, value: %s"), spaceID, *key, *value);

	if(KBEWorld::Instance())
		KBEWorld::Instance()->OnSetSpaceData(spaceID, key, value);
}

void CSOLPersonality::OnDelSpaceData(uint32 spaceID, const FString &key)
{
	KBE_ERROR(TEXT("CSOLPersonality::OnDelSpaceData: spaceID: %u, key: %s"), spaceID, *key);
}

void CSOLPersonality::OnAddSpaceGeometryMapping(uint32 spaceID, const FString &respath)
{
	KBE_ERROR(TEXT("CSOLPersonality::OnAddSpaceGeometryMapping: spaceID: %u, key: %s"), spaceID, *respath);
}

void CSOLPersonality::OnDisconnect()
{
	KBE_ERROR(TEXT("CSOLPersonality::OnDisconnect: "));
	if (LoginServerMgr::Instance())
		LoginServerMgr::Instance()->OnDisconnect();
}

void CSOLPersonality::OnLoginFailed(int32 errCode, const FString& errName, const FString& errDesc)
{
	KBE_ERROR(TEXT("CSOLPersonality::OnLoginFailed: code: %d, name: %s, desc: %s"), errCode, *errName, *errDesc);
}
