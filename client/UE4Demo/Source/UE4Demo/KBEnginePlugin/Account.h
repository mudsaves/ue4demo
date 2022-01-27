#pragma once

#include "KBEngine.h"
#include "Avatar.h"

class Account : public Avatar
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Avatar Supper;

public:
	Account();
	~Account();

	void onDBID(uint64 dbid);
	void onClientEvent(int32 val);
	void testFixedDict(const FVariant& val);
	void testFixedDictT1(const FVariant& val);
	void testOther1(float val1, FVariant val2, const FString& val3, const FVariant& val4);
	void testJson(FString val);
	void testForNoParam();
	void notifyAcrossServer();
	void notifyAcrossServerBack();

	float MoveSpeed() { return mMoveSpeed * 100; }
	void set_moveSpeed(const float &nv, const float &ov);

	void set_testVal(const uint32 &nv, const uint32 &ov);
	void set_floatValue(const float &nv, const float &ov);
	void set_strValue(const FString &nv, const FString &ov);
	void set_vector2Value(const FVector2D &nv, const FVector2D &ov);
	void set_vector3Value(const FVector &nv, const FVector &ov);
	// 用于测试 ARRAY OF 参数传输
	void set_arrayof(const KBEngine::FVariantArray& nv, const KBEngine::FVariantArray& ov);

	virtual void OnRemoteMethodCall(const FString &name, const TArray<FVariant> &args) override;
	virtual void OnEnterScenes() override;

	void Event_OnMonsterEnterWorld(const KBEngine::FVariantArray& args);
	void Event_OnMonsterEnterWorld2(const KBEngine::FVariantArray& args);

	virtual eEntityType EntityType() override { return Avatar::eEntityType::Player; }

protected:
	virtual void Set_Position(const FVector &oldVal) override;
	virtual void Set_Direction(const FVector &oldVal) override;
	virtual void OnUpdateVolatileData() override;

	virtual void OnEnterWorld() override;            // 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;            // 当Entity离开世界（被销毁时）时，此方法被调用
	virtual void OnEnterSpace() override;            // 当Entity进入地图时，此方法被调用
	virtual void OnLeaveSpace() override;            // 当Entity离开地图时，此方法被调用

private:
	float mMoveSpeed = 0.0f;
};


