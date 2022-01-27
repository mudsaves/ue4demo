// Copyright 1998-2016 Epic Games, Inc. All Rights Reserved.

#pragma once

#include "SlateBasics.h"
#include "ExportDataStyle.h"

class FExportDataCommands : public TCommands<FExportDataCommands>
{
public:

	FExportDataCommands()
		: TCommands<FExportDataCommands>(TEXT("ExportData"), NSLOCTEXT("Contexts", "ExportData", "ExportData Plugin"), NAME_None, FExportDataStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
