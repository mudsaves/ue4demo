// Copyright 1998-2016 Epic Games, Inc. All Rights Reserved.

#include "ExportDataCommands.h"
#include "ExportDataPrivatePCH.h"

#define LOCTEXT_NAMESPACE "FExportDataModule"

void FExportDataCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "ExportData", "Execute ExportData action", EUserInterfaceActionType::Button, FInputGesture());
}

#undef LOCTEXT_NAMESPACE
