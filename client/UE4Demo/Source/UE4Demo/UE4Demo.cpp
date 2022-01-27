// Fill out your copyright notice in the Description page of Project Settings.

#include "UE4Demo.h"

#include "KBEngine.h"
#include "KBEnginePlugin/EntityDeclare.h"
#include "KBEnginePlugin/CSOLPersonality.h"
#include "KBEnginePlugin/World.h"
#include "KBEnginePlugin/LoginServerMgr.h"

using namespace KBEngine;

KBEPersonality *g_KBEPersonality;
KBEWorld *g_KBEWorld;
LoginServerMgr *g_LoginServerMgr;

class FCSOLGameModule : public FDefaultGameModuleImpl
{
	virtual void StartupModule() override
	{
		g_KBEPersonality = new CSOLPersonality();
		KBEPersonality::Register(g_KBEPersonality);

		g_KBEWorld = new KBEWorld();
		KBEWorld::Register(g_KBEWorld);

		g_LoginServerMgr = new LoginServerMgr();
		LoginServerMgr::Register(g_LoginServerMgr);

		EntityDeclare();

	}

	virtual void ShutdownModule()
	{
		if (g_KBEPersonality)
		{
			KBEPersonality::Deregister();
			delete g_KBEPersonality;
		}

		if (g_KBEWorld)
		{
			KBEWorld::Deregister();
			delete g_KBEWorld;
		}

		if (g_LoginServerMgr)
		{
			LoginServerMgr::Deregister();
			delete g_LoginServerMgr;
		}
	}
};

//IMPLEMENT_PRIMARY_GAME_MODULE( FDefaultGameModuleImpl, Love4, "Love4" );
//IMPLEMENT_PRIMARY_GAME_MODULE( FDefaultGameModuleImpl, UE4Demo, "UE4Demo" );
IMPLEMENT_PRIMARY_GAME_MODULE( FCSOLGameModule, UE4Demo, "UE4Demo" );
