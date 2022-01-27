#pragma once

#include <vector>
#include "KBEngine.h"

/*
d = {"uid":123456789012345678, "id":1234567890, "amount":123,"flag":[11,22,33,44,55],"misc":"test - string"}
d1 = {"parent":113, "items":[d,]}


p.client.testFixedDict(d)
p.client.testFixedDictT1(d1)
p.client.testOther1(123.456, d, "string for test", [111, 112, 113, 114, 115])
*/

class ALIAS_ITEM
{
public:
	uint64 uid;
	uint64 id;
	int32 amount;
	TArray<int8> flag;
	FString misc;

	FString ToString()
	{
		FString flagS;
		TArray<FStringFormatArg> arg;
		int i = 0;
		for (auto f : flag)
		{
			flagS += FString::Printf(TEXT("{%u}, "), i++);
			arg.Add(f);
		}
		flagS = FString::Format(*flagS, arg);

		return FString::Printf(TEXT("uid: %llu, id: %llu, amount: %d, misc: %s, flag: [%s]"), uid, id, amount, *misc, *flagS);
	}

	void ToFVariantMap(KBEngine::FVariantMap &out)
	{
		out.Add(TEXT("uid"), FVariant(uid));
		out.Add(TEXT("id"), FVariant(id));
		out.Add(TEXT("amount"), FVariant(amount));
		out.Add(TEXT("misc"), FVariant(misc));

		KBEngine::FVariantArray arr;
		for (auto v : flag)
			arr.Add(FVariant(v));

		out.Add(TEXT("flag"), FVariant(arr));
	}

	static ALIAS_ITEM* CreateFromVariant(const FVariant& val)
	{
		auto* inst = new ALIAS_ITEM();

		auto m = val.GetValue<KBEngine::FVariantMap>();
		inst->uid = m[TEXT("uid")].GetValue<uint64>();
		inst->id = m[TEXT("id")].GetValue<uint64>();
		inst->amount = m[TEXT("amount")].GetValue<int32>();
		inst->misc = m[TEXT("misc")].GetValue<FString>();

		auto fs = m[TEXT("flag")].GetValue<KBEngine::FVariantArray>();
		for (auto& itor : fs)
		{
			inst->flag.Add(itor.GetValue<int8>());
		}
		return inst;
	}
};

class ALIAS_ITEM_T1
{
public:
	uint64 parent;
	TArray<ALIAS_ITEM*> items;

	~ALIAS_ITEM_T1()
	{
		for (auto item : items)
			delete item;
		items.Empty();
	}

	FString ToString()
	{
		FString itemStr;
		TArray<FStringFormatArg> arg;
		uint32 i = 0;
		for (auto item : items)
		{
			itemStr += FString::Printf(TEXT("{%u}, "), i++);
			arg.Add(item->ToString());
		}

		itemStr = FString::Format(*itemStr, arg);
		return FString::Printf(TEXT("parent: %u, items:[%s]"), parent, *itemStr);
	}

	static ALIAS_ITEM_T1* CreateFromVariant(const FVariant& val)
	{
		auto* inst = new ALIAS_ITEM_T1();

		auto m = val.GetValue<KBEngine::FVariantMap>();
		inst->parent = m[TEXT("parent")].GetValue<uint64>();

		auto fs = m[TEXT("items")].GetValue<KBEngine::FVariantArray>();
		for (auto& itor : fs)
		{
			ALIAS_ITEM* item = ALIAS_ITEM::CreateFromVariant(itor.GetValue<KBEngine::FVariantMap>());
			inst->items.Add(item);
		}
		return inst;
	}
};
