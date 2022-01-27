// Copyright 1998-2016 Epic Games, Inc. All Rights Reserved.

#include "ExportData.h"
#include "ExportDataPrivatePCH.h"
#include "SlateBasics.h"
#include "SlateExtras.h"

#include "ExportDataStyle.h"
#include "ExportDataCommands.h"

#include "LevelEditor.h"

#if WITH_RECAST

#include "NavMesh/RecastNavMesh.h"
#include "NavMesh/RecastNavMeshGenerator.h"
#include "NavMesh/PImplRecastNavMesh.h"
#include "NavMesh/NavMeshBoundsVolume.h"
#include "NavigationSystem.h"
#include "Detour/DetourNavMesh.h"
#include "Recast/Recast.h"
#include "EngineUtils.h"
#endif

static const int NAVMESHSET_MAGIC = 'M' << 24 | 'S' << 16 | 'E' << 8 | 'T'; //'MSET';
static const int NAVMESHSET_VERSION = 1;

struct NavMeshSetHeader
{
	int magic;
	int version;
	int numTiles;
	dtNavMeshParams params;
};

struct NavMeshTileHeader
{
	dtTileRef tileRef;
	int dataSize;
};

static const FName ExportDataTabName("ExportData");

#define LOCTEXT_NAMESPACE "FExportDataModule"

void FExportDataModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FExportDataStyle::Initialize();
	FExportDataStyle::ReloadTextures();

	FExportDataCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FExportDataCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FExportDataModule::PluginButtonClicked),
		FCanExecuteAction());
		
	FLevelEditorModule& LevelEditorModule = FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor");
	
	{
		TSharedPtr<FExtender> MenuExtender = MakeShareable(new FExtender());
		MenuExtender->AddMenuExtension("WindowLayout", EExtensionHook::After, PluginCommands, FMenuExtensionDelegate::CreateRaw(this, &FExportDataModule::AddMenuExtension));

		LevelEditorModule.GetMenuExtensibilityManager()->AddExtender(MenuExtender);
	}
	
	{
		TSharedPtr<FExtender> ToolbarExtender = MakeShareable(new FExtender);
		ToolbarExtender->AddToolBarExtension("Settings", EExtensionHook::After, PluginCommands, FToolBarExtensionDelegate::CreateRaw(this, &FExportDataModule::AddToolbarExtension));
		
		LevelEditorModule.GetToolBarExtensibilityManager()->AddExtender(ToolbarExtender);
	}
}

void FExportDataModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
	FExportDataStyle::Shutdown();

	FExportDataCommands::Unregister();
}

class ARecastNavMeshTrick : public ARecastNavMesh { public: const FPImplRecastNavMesh* GetRecastNavMeshImplTrick() const { return GetRecastNavMeshImpl(); } };

void FExportDataModule::PluginButtonClicked()
{
	// Put your "OnButtonClicked" stuff here
	/*FText DialogText = FText::Format(
							LOCTEXT("PluginButtonDialogText", "Add code to {0} in {1} to override this button's actions"),
							FText::FromString(TEXT("FExportDataModule::PluginButtonClicked()")),
							FText::FromString(TEXT("ExportData.cpp"))
					   );
	FMessageDialog::Open(EAppMsgType::Ok, DialogText);*/

	//FWorldContext &EditorContext = GEditor->GetEditorWorldContext();
	//for (int32 NavDataIndex = 0; NavDataIndex < EditorContext.World()->GetNavigationSystem()->NavDataSet.Num(); ++NavDataIndex)
	//{
	//	ANavigationData* NavData = EditorContext.World()->GetNavigationSystem()->NavDataSet[NavDataIndex];
	//	if (NavData && !NavData->IsPendingKill())
	//	{
	//		ARecastNavMesh * RecastNavData = Cast<ARecastNavMesh>(NavData);
	//		dtNavMesh* NavMesh = RecastNavData->GetRecastNavMeshImpl()->GetRecastMesh();
	//		char text[32];
	//		snprintf(text, 32, "%d.navmesh", NavDataIndex);
	//		if (NavMesh != NULL)
	//		{
	//			UE_LOG(LogNavigation, Error, TEXT("Succeed to get navigation data!!!"));
	//			SaveData(text, NavMesh);
	//		}
	//		else
	//		{
	//			UE_LOG(LogNavigation, Error, TEXT("Failed to export navigation data due to navigation data"));
	//		}			
	//	}
	//}


	FWorldContext &EditorContext = GEditor->GetEditorWorldContext();
	UWorld * InWorld = EditorContext.World();
	UNavigationSystemV1* navigationSystem = FNavigationSystem::GetCurrent<UNavigationSystemV1>(InWorld);
	TArray<FNavDataConfig> supportedAgents = navigationSystem->GetSupportedAgents();
	for (int32 agents = 0; agents < supportedAgents.Num(); agents++)
	{
		FNavDataConfig dataConfig = supportedAgents[agents];
		ANavigationData* NavData = navigationSystem->GetNavDataForProps(dataConfig);
		if (NavData && !NavData->IsPendingKill())
		{
			ARecastNavMeshTrick * RecastNavData = Cast<ARecastNavMeshTrick>(NavData);
			const FPImplRecastNavMesh* tempRN = RecastNavData->GetRecastNavMeshImplTrick();
			const dtNavMesh* NavMesh = tempRN->GetRecastMesh();
			char text[32];
			snprintf(text, 32, "%d.navmesh", agents);
			if (NavMesh != NULL)
			{
				UE_LOG(LogNavigation, Error, TEXT("Succeed to get navigation data!!!"));
				SaveData(text, NavMesh);
			}
			else
			{
				UE_LOG(LogNavigation, Error, TEXT("Failed to export navigation data due to navigation data"));
			}
		}
	}
}

void FExportDataModule::AddMenuExtension(FMenuBuilder& Builder)
{
	Builder.AddMenuEntry(FExportDataCommands::Get().PluginAction);
}

void FExportDataModule::AddToolbarExtension(FToolBarBuilder& Builder)
{
	Builder.AddToolBarButton(FExportDataCommands::Get().PluginAction);
}

void FExportDataModule::SaveData(const char* path, const dtNavMesh* mesh)
{
	if (!mesh) return;

	// Store header.
	NavMeshSetHeader header;
	header.magic = NAVMESHSET_MAGIC;
	header.version = NAVMESHSET_VERSION;
	header.numTiles = 0;
	for (int i = 0; i < mesh->getMaxTiles(); ++i)
	{
		const dtMeshTile* tile = mesh->getTile(i);
		if (!tile || !tile->header || !tile->dataSize) continue;
		header.numTiles++;
	}
	
	//判断是否有数据，没有数据，直接返回
	if (header.numTiles == 0)
		return;

	FILE* fp = fopen(path, "wb");
	if (!fp)
		return;

	memcpy(&header.params, mesh->getParams(), sizeof(dtNavMeshParams));
	fwrite(&header, sizeof(NavMeshSetHeader), 1, fp);

	// Store tiles.
	for (int i = 0; i < mesh->getMaxTiles(); ++i)
	{
		const dtMeshTile* tile = mesh->getTile(i);
		if (!tile || !tile->header || !tile->dataSize) continue;

		NavMeshTileHeader tileHeader;
		tileHeader.tileRef = mesh->getTileRef(tile);
		tileHeader.dataSize = tile->dataSize;
		fwrite(&tileHeader, sizeof(tileHeader), 1, fp);

		fwrite(tile->data, tile->dataSize, 1, fp);
	}

	fclose(fp);
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FExportDataModule, ExportData)