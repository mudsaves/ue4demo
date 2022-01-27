#pragma once

#include "KBEngine.h"
#include "Avatar.h"


class MovePlatform : public Avatar
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Avatar Supper;

public:
	MovePlatform();
	~MovePlatform();

	float MoveSpeed() { return mMoveSpeed * 100; }
	void set_moveSpeed(const float &nv, const float &ov);

	virtual void OnEnterScenes() override;

	virtual eEntityType EntityType() override { return Avatar::eEntityType::MovePlatform; }

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

