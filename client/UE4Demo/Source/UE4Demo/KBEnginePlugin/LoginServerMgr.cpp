#include "LoginServerMgr.h"


LoginServerMgr* LoginServerMgr::instance_ = nullptr;

void LoginServerMgr::Register(LoginServerMgr * inst)
{
	KBE_ASSERT(instance_ == nullptr);
	instance_ = inst;
}

void LoginServerMgr::Deregister()
{
	if (instance_)
		instance_ = nullptr;
}

void LoginServerMgr::Process()
{
	//¼ì²â¿ç·þµÇÂ½
	if (isWaitAcrossLogin_)
	{
		auto span = FDateTime::UtcNow() - waitAcrossLoginTime_;
		if (span.GetTotalSeconds() >= 2)
		{
			isWaitAcrossLogin_ = false;
			KBEngine::KBEngineApp::app->AcrossLoginBaseapp();
		}
	}

	//¼ì²â·µ»Ø±¾·þ
	if (isWaitAcrossLoginBack_)
	{
		auto span = FDateTime::UtcNow() - waitAcrossLoginBackTime_;
		if (span.GetTotalSeconds() >= 2)
		{
			isWaitAcrossLoginBack_ = false;
			KBEngine::KBEngineApp::app->AcrossLoginBack();
		}
	}
}

void LoginServerMgr::OnLoginOffForAcrossLogin()
{
	isLoginoffForAcrossLogin_ = true;
}

void LoginServerMgr::OnLoginOffForAcrossLoginBack()
{
	isLoginoffForAcrossBack_ = true;
}

void LoginServerMgr::OnDisconnect()
{
	if (isLoginoffForAcrossLogin_)
	{
		isLoginoffForAcrossLogin_ = false;
		isWaitAcrossLogin_ = true;
		waitAcrossLoginTime_ = FDateTime::UtcNow();
	}

	if (isLoginoffForAcrossBack_)
	{
		isLoginoffForAcrossBack_ = false;
		isWaitAcrossLoginBack_ = true;
		waitAcrossLoginBackTime_ = FDateTime::UtcNow();
	}
}

void LoginServerMgr::LoginServer(const FString& username, const FString& password, const TArray<uint8>& datas)
{
	if (isWaitAcrossLogin_)
	{
		KBE_ERROR(TEXT("LoginServerMgr::LoginServer, is wait across login!"));
		return;
	}

	if (isWaitAcrossLoginBack_)
	{
		KBE_ERROR(TEXT("LoginServerMgr::LoginServer, is wait across login back!"));
		return;
	}

	KBEngine::KBEngineApp::app->Login(username, password, datas);
}

