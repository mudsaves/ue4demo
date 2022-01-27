#pragma once

#include "KBEngine.h"

class LoginServerMgr
{
public:
	static void Register(LoginServerMgr * inst);
	static void Deregister();
	FORCEINLINE static LoginServerMgr* Instance() { return instance_; }

	virtual void Process();

	void OnLoginOffForAcrossLogin();

	void OnLoginOffForAcrossLoginBack();

	void OnDisconnect();

	void LoginServer(const FString& username, const FString& password, const TArray<uint8>& datas);

private:
	static LoginServerMgr* instance_;

	bool isLoginoffForAcrossLogin_ = false;
	bool isWaitAcrossLogin_ = false;
	FDateTime waitAcrossLoginTime_;

	bool isLoginoffForAcrossBack_ = false;
	bool isWaitAcrossLoginBack_ = false;
	FDateTime waitAcrossLoginBackTime_;
};

