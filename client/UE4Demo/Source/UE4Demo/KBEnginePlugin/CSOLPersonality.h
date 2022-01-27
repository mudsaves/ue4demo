#pragma once

#include "KBEngine.h"

class CSOLPersonality : public KBEngine::KBEPersonality
{
public:
	virtual void OnSetSpaceData(uint32 spaceID, const FString &key, const FString &value) override;
	virtual void OnDelSpaceData(uint32 spaceID, const FString &key) override;
	virtual void OnAddSpaceGeometryMapping(uint32 spaceID, const FString &respath) override;
	
	virtual void OnLoginFailed(int32 errCode, const FString& errName, const FString& errDesc) override;

	virtual void OnDisconnect() override;

};