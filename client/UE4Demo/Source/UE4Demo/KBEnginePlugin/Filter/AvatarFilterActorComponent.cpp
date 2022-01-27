// Fill out your copyright notice in the Description page of Project Settings.
#include "AvatarFilterActorComponent.h"
#include "UE4Demo.h"
#include "Component/AvatarActorComponent.h"
#include "KBEnginePlugin/Avatar.h"


namespace FilterUtilityFunctions
{
	/**
	*	This function decodes the 'on ground' condition by sampling
	*	the terrain height.
	*/
	bool resolveOnGroundPosition(FVector& position, bool& onGround)
	{
		//onGround = false;

		//if (position.y < -12000.0f)
		//{
		//	float terrainHeight = Terrain::BaseTerrainBlock::getHeight(position[0],
		//		position[2]);
		//	if (terrainHeight == Terrain::BaseTerrainBlock::NO_TERRAIN)
		//		return false;


		//	position.y = terrainHeight;
		//	onGround = true;
		//}

		return true;
	}

	/**
	*	This function transforms the given position and direction into
	*	common/world space.
	*
	*	@param	spaceID	The server space in which the give position and direction
	*				are defined.
	*	@param	vehicleID	The vehicle who's coordinate system the given position and
	*				direction are defined.
	*	@param	pos	The local space position to be translated into common space.
	*	@param	dir	The local space direction to be translated into common space.
	*/
	void transformIntoCommon(int32 spaceID, int32 vehicleID, FVector& pos, FVector& dir)
	{
		if (vehicleID <= 0)
			return;

		KBEngine::Entity* parentEnt = KBEngine::KBEngineApp::app->FindEntity(vehicleID);
		if (!parentEnt)
			return;

		pos = parentEnt->PositionLocalToWorld(pos);
		dir = parentEnt->DirectionLocalToWorld(dir);
	}

	/**
	*	This function transforms the given position to its local representation.
	*
	*	@param	spaceID	The server space into which the give position and direction
	*				will be placed.
	*	@param	vehicleID	The vehicle in who's coordinate system the given position
	*				and direction will now exist.
	*	@param	pos	The common space position to be translated into local space.
	*	@param	dir	The common space direction to be translated into local space.
	*/
	void transformFromCommon(int32 spaceID, int32 vehicleID, FVector& pos, FVector& dir)
	{
		if (vehicleID <= 0)
			return;

		KBEngine::Entity* parentEnt = KBEngine::KBEngineApp::app->FindEntity(vehicleID);
		if (!parentEnt)
			return;

		pos = parentEnt->PositionWorldToLocal(pos);
		dir = parentEnt->DirectionWorldToLocal(dir);
	}

	FVector clamp(const FVector& alpha, const FVector& lower, const FVector& upper)
	{
		return FVector(
			FMath::Clamp<float>(alpha.X, lower.X, upper.X),
			FMath::Clamp<float>(alpha.Y, lower.Y, upper.Y),
			FMath::Clamp<float>(alpha.Z, lower.Z, upper.Z) );
	}

	bool almostEqual(const FVector& v1, const FVector& v2, const float epsilon = 0.0004f)
	{
		return	FMath::IsNearlyEqual(v1.X, v2.X, epsilon) &&
				FMath::IsNearlyEqual(v1.Y, v2.Y, epsilon) &&
				FMath::IsNearlyEqual(v1.Z, v2.Z, epsilon);
	}

	/**
	*	This method tests if the bounding box contains the given point
	*/
	bool intersects(const FBox& b, const FVector& v)
	{
		return (v[0] >= b.Min[0]) && (v[1] >= b.Min[1]) && (v[2] >= b.Min[2]) &&
			(v[0] < b.Max[0]) && (v[1] < b.Max[1]) && (v[2] < b.Max[2]);
	}

	/**
	* 把两个不同符号的角度換成相同符号的角度
	*/
	float sameSignDegree(float degree, float closer)
	{
		if (closer > degree + 180.0)
			return closer - 2.0 * 180.0;
		else if (closer < degree - 180.0)
			return closer + 2.0 * 180.0;
		else
			return closer;
	}

	FVector sameSignDegree(const FVector& degree, const FVector& closer)
	{
		FVector v;
		v.X = sameSignDegree(degree.X, closer.X);
		v.Y = sameSignDegree(degree.Y, closer.Y);
		v.Z = sameSignDegree(degree.Z, closer.Z);
		return v;
	}
}









float SmoothFilter::s_latencyVelocity_ = 1.00f;
float SmoothFilter::s_latencyMinimum_ = 0.10f;
float SmoothFilter::s_latencyFrames_ = 2.0f;
float SmoothFilter::s_latencyCurvePower_ = 2.0f;


SmoothFilter::SmoothFilter() :
	latency_(0),
	idealLatency_(0),
	timeOfLastOutput_(0),
	gotNewInput_(false),
	reset_(true),
	timeOfLastInput_(0),
	owner_(nullptr)
{
	this->resetStoredInputs(-2000, 0, 0, FVector::ZeroVector, FVector::ZeroVector, FVector::ZeroVector);
	this->reset(0);
}

SmoothFilter::SmoothFilter(const SmoothFilter& filter) :
	currentInputIndex_(filter.currentInputIndex_),
	nextWaypoint_(filter.nextWaypoint_),
	previousWaypoint_(filter.previousWaypoint_),
	latency_(filter.latency_),
	idealLatency_(filter.idealLatency_),
	timeOfLastOutput_(filter.timeOfLastOutput_),
	gotNewInput_(filter.gotNewInput_),
	reset_(filter.reset_),
	timeOfLastInput_(filter.timeOfLastInput_)
{
	for (uint32 i = 0; i<NUM_STORED_INPUTS; i++)
	{
		storedInputs_[i] = filter.storedInputs_[i];
	}
}

SmoothFilter::~SmoothFilter()
{
}

void SmoothFilter::input(double time, int32 spaceID, int32 vehicleID, const FVector & position, const FVector& positionError, const FVector& direction)
{
	// 长时间没有新数据输入就认为是重新开始，需要重置时间
	if (!reset_ && time - timeOfLastInput_ > 1.0f)
	{
		const StoredInput& topInput = getStoredInput(0);
		for (uint32 i = 0; i < NUM_STORED_INPUTS; i++)
		{
			StoredInput& storedInput = getStoredInput(i);
			storedInput.time_ = time - (i * NONZERO_TIME_DIFFERENCE);
			storedInput.position_ = topInput.position_;
			storedInput.direction_ = topInput.direction_;
			storedInput.vehicleID_ = topInput.vehicleID_;
			storedInput.spaceID_ = topInput.spaceID_;
			storedInput.onGround_ = topInput.onGround_;
		}
	}

	if (reset_)
	{
		this->resetStoredInputs(time, spaceID, vehicleID, position, positionError, direction);
		reset_ = false;
	}
	else
	{
		if (time > this->getStoredInput(0).time_)
		{
			currentInputIndex_ = (currentInputIndex_ + NUM_STORED_INPUTS - 1) % NUM_STORED_INPUTS;
		}

		StoredInput & storedInput = this->getStoredInput(0);

		storedInput.time_ = time;
		storedInput.spaceID_ = spaceID;
		storedInput.vehicleID_ = vehicleID;
		storedInput.position_ = position;
		storedInput.positionError_ = positionError;
		storedInput.direction_ = direction;

		FilterUtilityFunctions::resolveOnGroundPosition(storedInput.position_, storedInput.onGround_);

		gotNewInput_ = true;
	}

	timeOfLastInput_ = time;
}

void SmoothFilter::output(double time)
{
	// adjust ideal latency if we got something new
	if (gotNewInput_)
	{
		gotNewInput_ = false;

		const double newestTime = this->getStoredInput(0).time_;
		const double olderTime = this->getStoredInput(NUM_STORED_INPUTS - 1).time_;
		
		SmoothFilter::s_latencyFrames_ = FMath::Clamp<float>(SmoothFilter::s_latencyFrames_, 0.0f, NUM_STORED_INPUTS - 1);

		double ratio = ((NUM_STORED_INPUTS - 1) - SmoothFilter::s_latencyFrames_) / (NUM_STORED_INPUTS - 1);
		
		idealLatency_ = float(time - FMath::Lerp(olderTime, newestTime, ratio));

		idealLatency_ = std::max(idealLatency_, s_latencyMinimum_);
	}

	// move latency towards the ideal...
	float dTime = float(time - timeOfLastOutput_);
	if (idealLatency_ > latency_)
	{
		latency_ += (s_latencyVelocity_ * dTime) * std::min(1.0f, powf(fabsf(idealLatency_ - latency_), SmoothFilter::s_latencyCurvePower_));
		latency_ = std::min(latency_, idealLatency_);
	}
	else
	{
		latency_ -= (s_latencyVelocity_ * dTime) * std::min(1.0f, powf(fabsf(idealLatency_ - latency_), SmoothFilter::s_latencyCurvePower_));
		latency_ = std::max(latency_, idealLatency_);
	}


	// record this so we can move latency at a velocity independent
	//  of the number of times we're called.
	timeOfLastOutput_ = time;

	// find the position at 'time - latency'
	double outputTime = time - latency_;

	int32		resultSpaceID;
	int32		resultVehicleID;
	FVector		resultPosition;
	FVector		resultVelocity;
	FVector		resultDirection;

	this->extract(outputTime, resultSpaceID, resultVehicleID, resultPosition, resultVelocity, resultDirection);

	// make sure it's in the right coordinate system
	//FilterUtilityFunctions::coordinateSystemCheck(owner_, resultSpaceID, resultVehicleID);

	owner_->Pos(resultVehicleID, resultPosition, resultDirection, resultVelocity);
}

/**
*	This method changes the coordinate system of the waypoint by first
*	transforming into common coordinates and then into the new coordinates.
*	spaceID_ and vehicleID_ are also set to that of the new coordinate system.
*/
void SmoothFilter::Waypoint::changeCoordinateSystem(int32 spaceID, int32 vehicleID)
{
	if (spaceID_ == spaceID && vehicleID_ == vehicleID)
		return;

	FilterUtilityFunctions::transformIntoCommon(spaceID_,
		vehicleID_,
		position_,
		direction_);

	spaceID_ = spaceID;
	vehicleID_ = vehicleID;

	FilterUtilityFunctions::transformFromCommon(spaceID_,
		vehicleID_,
		position_,
		direction_);
}

void SmoothFilter::resetStoredInputs(double time, int32 spaceID, int32 vehicleID, const FVector& position, const FVector& positionError, const FVector& direction)
{
	currentInputIndex_ = 0;
	gotNewInput_ = true;

	for (uint32 i = 0; i< NUM_STORED_INPUTS; i++)
	{
		StoredInput & storedInput = this->getStoredInput(i);

		// set times of older inputs as to avoid zero time differences
		storedInput.time_ = time - (i * NONZERO_TIME_DIFFERENCE);

		storedInput.spaceID_ = spaceID;
		storedInput.vehicleID_ = vehicleID;
		storedInput.position_ = position;
		storedInput.positionError_ = positionError;
		storedInput.direction_ = direction;

		FilterUtilityFunctions::resolveOnGroundPosition(storedInput.position_, storedInput.onGround_);
	}

	this->latency_ = s_latencyFrames_ * NONZERO_TIME_DIFFERENCE;

	nextWaypoint_.time_ = time - NONZERO_TIME_DIFFERENCE;
	nextWaypoint_.spaceID_ = spaceID;
	nextWaypoint_.vehicleID_ = vehicleID;
	nextWaypoint_.position_ = position;
	nextWaypoint_.direction_ = direction;

	previousWaypoint_ = nextWaypoint_;
	previousWaypoint_.time_ -= NONZERO_TIME_DIFFERENCE;
}

/**
*	This method 'extracts' a set of filtered values from the input history,
*	clamping at the extremes of the time period stored. In the case that
*	requested time falls between two inputs a weighed blend is performed
*	taking into account vehicle transitions.
*	A small amount of speculative movement supported when the most recent
*	value in the history is older than the time requested.
*
*	@param	time		The client time stamp of the values required.
*	@param	iSID		The resultant space ID
*	@param	iVID		The resultant vehicle ID
*	@param	iPos		The estimated position in the space of iVID
*	@param	iVelocity	The estimated velocity of the entity at the time
*						specified.
*	@param	iDir		The estimated yaw and pitch of the entity.
*/
void SmoothFilter::extract(double time, int32& outputSpaceID, int32& outputVehicleID, FVector& outputPosition, FVector& outputVelocity, FVector& outputDirection)
{
	if (!isActive())
	{
		const StoredInput & mostRecentInput = this->getStoredInput(0);

		outputSpaceID = mostRecentInput.spaceID_;
		outputVehicleID = mostRecentInput.vehicleID_;
		outputPosition = mostRecentInput.position_;
		outputDirection = mostRecentInput.direction_;
		outputVelocity = FVector::ZeroVector;
		
		return;
	}
	else
	{
		if (time > nextWaypoint_.time_)
		{
			this->chooseNextWaypoint(time);
		}

		float proportionateDifferenceInTime = float((time - previousWaypoint_.time_) /
			(nextWaypoint_.time_ - previousWaypoint_.time_));

		outputSpaceID = nextWaypoint_.spaceID_;
		outputVehicleID = nextWaypoint_.vehicleID_;
		
		outputPosition = FMath::Lerp(previousWaypoint_.position_, nextWaypoint_.position_, proportionateDifferenceInTime);

		outputVelocity = (nextWaypoint_.position_ - previousWaypoint_.position_) /
			float(nextWaypoint_.time_ - previousWaypoint_.time_);

		outputDirection = FMath::Lerp(FilterUtilityFunctions::sameSignDegree(nextWaypoint_.direction_, previousWaypoint_.direction_), nextWaypoint_.direction_, proportionateDifferenceInTime);
	}


}

/**
*	This internal method choses a new set of waypoints to traverse based on the
*	history of stored input and the requested time. A few approaches are used
*	depending on the number of received inputs ahead of the requested time.
*
*	Two inputs ahead of time
*	A vector is made from head of the previous waypoints to the centre of the
*	input two ahead. The point on this vector that exists one input ahead in
*	time is then found and its position clamped to the box of error tolerance
*	of that same input. This point forms the new head waypoint and the previous
*	becomes the new tail.
*
*	Only one input ahead of time
*	The current pair of waypoints are projected into the future to the time of
*	the next input ahead. The resultant position is then clamped to the box of
*	error tolerance of that input.
*
*	No inputs ahead of time
*	In the event no inputs exist ahead of the time both waypoints are set to
*	the same position. The entity will stand still until an input is received
*	that is ahead of game time minus latency.
*
*	Note: Both waypoints are always in the same coordinate system; that of the
*	next input ahead.
*
*	@param time	The time which the new waypoints should enclose
*/
void SmoothFilter::chooseNextWaypoint(double time)
{
	Waypoint & previousWaypoint = previousWaypoint_;
	Waypoint & currentWaypoint = nextWaypoint_;

	Waypoint newWaypoint;

	if (this->getStoredInput(0).time_ > time)
	{
		for (int i = NUM_STORED_INPUTS - 1; i >= 0; i--)
		{
			if (this->getStoredInput(i).time_ > time)
			{
				const StoredInput & lookAheadInput = this->getStoredInput(0);
				const StoredInput & nextInput = this->getStoredInput(i);

				newWaypoint.time_ = nextInput.time_;
				newWaypoint.spaceID_ = nextInput.spaceID_;
				newWaypoint.vehicleID_ = nextInput.vehicleID_;
				newWaypoint.direction_ = nextInput.direction_;

				newWaypoint.storedInput_ = nextInput;

				previousWaypoint.changeCoordinateSystem(newWaypoint.spaceID_,
					newWaypoint.vehicleID_);

				currentWaypoint.changeCoordinateSystem(newWaypoint.spaceID_,
					newWaypoint.vehicleID_);

				float lookAheadRelativeDifferenceInTime = float((lookAheadInput.time_ - previousWaypoint.time_) /
					(currentWaypoint.time_ - previousWaypoint.time_));

				FVector lookAheadPosition = FMath::Lerp(previousWaypoint.position_, currentWaypoint.position_, lookAheadRelativeDifferenceInTime);

				FVector direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformIntoCommon(newWaypoint.spaceID_,    newWaypoint.vehicleID_,    lookAheadPosition, direction);
				direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformFromCommon(lookAheadInput.spaceID_, lookAheadInput.vehicleID_, lookAheadPosition, direction);

				lookAheadPosition = FilterUtilityFunctions::clamp(lookAheadPosition, 
							lookAheadInput.position_ - lookAheadInput.positionError_,
							lookAheadInput.position_ + lookAheadInput.positionError_);

				direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformIntoCommon(lookAheadInput.spaceID_, lookAheadInput.vehicleID_, lookAheadPosition, direction);
				direction = FVector::ZeroVector;
				FilterUtilityFunctions::transformFromCommon(newWaypoint.spaceID_,    newWaypoint.vehicleID_,    lookAheadPosition, direction);

				// Handel overlapping error rectangles
				{
					FBox newWaypointBB(newWaypoint.storedInput_.position_ - newWaypoint.storedInput_.positionError_,
						newWaypoint.storedInput_.position_ + newWaypoint.storedInput_.positionError_);
					FBox currentWaypointBB(currentWaypoint.storedInput_.position_ - currentWaypoint.storedInput_.positionError_,
						currentWaypoint.storedInput_.position_ + currentWaypoint.storedInput_.positionError_);

					if (newWaypoint.spaceID_ == currentWaypoint.storedInput_.spaceID_ &&
						newWaypoint.vehicleID_ == currentWaypoint.storedInput_.vehicleID_ &&
						!FilterUtilityFunctions::almostEqual(newWaypoint.storedInput_.positionError_, currentWaypoint.storedInput_.positionError_) &&
						newWaypointBB.Intersect(currentWaypointBB))
					{
						// Remain still if the previous move was only to adjust
						// for changes in position error (ie overlapping error regions).
						newWaypoint.position_ = currentWaypoint.position_;
					}
					else
					{
						float proportionateDifferenceInTime = float((nextInput.time_ - currentWaypoint.time_) /
							(lookAheadInput.time_ - currentWaypoint.time_));

						newWaypoint.position_ = FMath::Lerp(currentWaypoint.position_, lookAheadPosition, proportionateDifferenceInTime);
					}
				}

				// Constrain waypoint position to its input error rectangle
				{
					FBox nextInputBB(nextInput.position_ - nextInput.positionError_,
						nextInput.position_ + nextInput.positionError_);

					if (!FilterUtilityFunctions::intersects(nextInputBB, newWaypoint.position_))
					{
						FVector clampedPosition = FilterUtilityFunctions::clamp(newWaypoint.position_,
							nextInput.position_ - nextInput.positionError_,
							nextInput.position_ + nextInput.positionError_);

						FVector lookAheadVector = newWaypoint.position_ - currentWaypoint.position_;
						FVector clampedVector = clampedPosition - currentWaypoint.position_;

						if (lookAheadVector.SizeSquared() > 0.0f)
							newWaypoint.position_ = currentWaypoint.position_ + clampedVector.ProjectOnTo(lookAheadVector);
						else
							newWaypoint.position_ = currentWaypoint.position_;

						newWaypoint.position_ = FilterUtilityFunctions::clamp(newWaypoint.position_,
							nextInput.position_ - nextInput.positionError_,
							nextInput.position_ + nextInput.positionError_);
					}
				}

				break;
			}
		}
	}
	else
	{
		// In the event there is no more input data, stand still for one frame.
		//newWaypoint = nextWaypoint_;
		//newWaypoint.time_ = time;

		// 总是使用当前帧的数据，以避免在同一个tick下收到多个相同数据包时导致坐标与服务器的不一致的问题
		// 因为KBE在移动结束后不会继续发送数据包过来
		const StoredInput & topInput = this->getStoredInput(0);
		newWaypoint.spaceID_ = topInput.spaceID_;
		newWaypoint.vehicleID_ = topInput.vehicleID_;
		newWaypoint.position_ = topInput.position_;
		newWaypoint.direction_ = topInput.direction_;
		newWaypoint.storedInput_ = topInput;
		newWaypoint.time_ = time;

	}

	previousWaypoint_ = currentWaypoint;
	nextWaypoint_ = newWaypoint;
}

SmoothFilter::StoredInput & SmoothFilter::getStoredInput(uint32 index)
{
	KBE_ASSERT(index < NUM_STORED_INPUTS);

	return storedInputs_[(currentInputIndex_ + index) % NUM_STORED_INPUTS];
}

const SmoothFilter::StoredInput & SmoothFilter::getStoredInput(uint32 index) const
{
	return const_cast<SmoothFilter*>(this)->getStoredInput(index);
}

bool SmoothFilter::getLastInput(double & time, int32& spaceID, int32& vehicleID, FVector& pos, FVector& posError, FVector& direction)
{
	if (!reset_)
	{
		const StoredInput & storedInput = this->getStoredInput(0);
		time = storedInput.time_;
		spaceID = storedInput.spaceID_;
		vehicleID = storedInput.vehicleID_;
		pos = storedInput.position_;
		direction = storedInput.direction_;
		return true;
	}
	return false;
}








UAvatarFilterActorComponent::UAvatarFilterActorComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;
}

void UAvatarFilterActorComponent::ResetComponent()
{
	vLastPos = GetOwner()->GetActorLocation();
	FVector dir = GetOwner()->GetActorRotation().Euler();
	FVector pos = GetOwner()->GetActorLocation();
	KBEngine::Entity* parentEntity = nullptr;
	KBEngine::Entity* entity = nullptr;

	if (GameObjComponent() && GameObjComponent()->entity())
	{
		entity = GameObjComponent()->entity();
		parentEntity = entity->Parent();
	}

	if (parentEntity)
	{
		//pos = parentEntity->PositionWorldToLocal(pos);
		//dir = parentEntity->DirectionWorldToLocal(dir);
		pos = entity->LocalPosition();
		dir = entity->LocalDirection();
	}

	mFilter.reset(GetWorld()->GetTimeSeconds());
	int32 vehicleID = entity ? entity->ParentID() : 0;
	mFilter.input(GetWorld()->GetTimeSeconds() - 0.1, 0, vehicleID, pos, FVector::ZeroVector, dir);
}

void UAvatarFilterActorComponent::InitFilter(UAvatarActorComponent* _comp)
{
	GameObjComponent(_comp);
	mFilter.owner(this);
}

// Called when the game starts
void UAvatarFilterActorComponent::BeginPlay()
{
	Super::BeginPlay();

	ResetComponent();
}


// Called every frame
void UAvatarFilterActorComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	float time = GetWorld()->GetTimeSeconds();
	mFilter.output(time);
	
	//FVector vVelocity = FVector::ZeroVector;
	//FVector entityVelocity = mVelocity;
	//if (entityVelocity.Size() > 0.0f)
	//{
	//	vVelocity = mVelocity;
	//	vVelocity.Normalize();
	//	FVector delta = GetOwner()->GetActorLocation() - vLastPos;
	//	float speed = delta.Size();
	//	vVelocity *= speed * (1.0f / DeltaTime);
	//}
	//else
	//{
	//	vVelocity = (GetOwner()->GetActorLocation() - vLastPos) * (1.0f / DeltaTime);
	//}

	//FVector vHorizontalVelocity = vVelocity;
	//vHorizontalVelocity.Z = 0.0f;

	//float newSpeed = vHorizontalVelocity.Size();
	//if (newSpeed > 10 && runFlag)
	//{
	//	SpeedChangedNotify(newSpeed);
	//}
	//else
	//{
	//	SpeedChangedNotify(0);
	//}

	//vLastPos = GetOwner()->GetActorLocation();
}

void UAvatarFilterActorComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);

	SpeedChangedNotify(0);
}

void UAvatarFilterActorComponent::OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID)
{
	//KBE_DEBUG(TEXT("UAvatarFilterActorComponent::OnUpdateVolatileData(), %d - %d, position (%f, %f, %f), direction (%f, %f, %f)"),
	//	GameObjComponent()->entity()->ID(), parentID,
	//	position.X, position.Y, position.Z,
	//	direction.X, direction.Y, direction.Z);
	FVector dir(0, 0, direction.Z);  // 我们只想同步Z轴（朝向）
	int sceneID = 0;
	int vehicleID = parentID;
	float time = GetWorld()->GetTimeSeconds();
	mFilter.input(time, sceneID, vehicleID, position, FVector::ZeroVector, dir);
}

void UAvatarFilterActorComponent::SetPosition(const FVector& position, int32 parentID)
{
	//KBE_DEBUG(TEXT("UAvatarFilterActorComponent::SetPosition(), %d - %d, position (%f, %f, %f)"),
	//	GameObjComponent()->entity()->ID(), parentID,
	//	position.X, position.Y, position.Z);
	double time = GetWorld()->GetTimeSeconds();
	int32 topSID;
	int32 topVID;
	FVector topPos = position;
	FVector topDir = GetOwner()->GetActorRotation().Euler();
	FVector topErr = FVector::ZeroVector;
	mFilter.getLastInput(time, topSID, topVID, topPos, topErr, topDir);
	mFilter.reset(GetWorld()->GetTimeSeconds());
	mFilter.input(GetWorld()->GetTimeSeconds() + 0.00001, topSID, topVID, position, topErr, topDir);
}

void UAvatarFilterActorComponent::SetDirection(const FVector& direction, int32 parentID)
{
	//KBE_DEBUG(TEXT("UAvatarFilterActorComponent::SetDirection(), %d - %d, direction (%f, %f, %f)"),
	//	GameObjComponent()->entity()->ID(), parentID,
	//	direction.X, direction.Y, direction.Z);

	double time = GetWorld()->GetTimeSeconds();
	int32 topSID;
	int32 topVID;
	FVector topPos = GetOwner()->GetActorLocation();
	FVector topDir = direction;
	FVector topErr = FVector::ZeroVector;
	mFilter.getLastInput(time, topSID, topVID, topPos, topErr, topDir);
	mFilter.reset(GetWorld()->GetTimeSeconds());
	mFilter.input(GetWorld()->GetTimeSeconds() + 0.00001, topSID, topVID, topPos, topErr, direction);
}

void UAvatarFilterActorComponent::SpeedChangedNotify(float speed)
{
	Super::SpeedChangedNotify(speed);

	if (GameObjComponent() != nullptr)
	{
		GameObjComponent()->OnFilterSpeedChanged(speed);
	}
}

void UAvatarFilterActorComponent::Pos(int32 vehicleID, const FVector& position, const FVector& direction, const FVector& velocity)
{
	mVelocity = velocity;

	auto *entity = GameObjComponent()->entity();
	FVector newPos = position;
	FVector newDir = direction;

	if (!entity)
		return;

	if (vehicleID > 0)
	{
		auto *parent = KBEngine::KBEngineApp::app->FindEntity(vehicleID);

		if (parent)
		{
			newPos = parent->PositionLocalToWorld(newPos);
			newDir = parent->DirectionLocalToWorld(newDir);
		}
		else
			return;  // 有父对象，但找不到了，则啥都不做，保持原位置不变
	}

	//auto rotation = FQuat::MakeFromEuler(newDir) * FVector::ForwardVector;
	//GetOwner()->SetActorLocationAndRotation(newPos, rotation.Rotation());
	if (((Avatar*)entity)->EntityType() == Avatar::eEntityType::MovePlatform)
		GameObjComponent()->FixOnGroundPosition(newPos, true);
	else
		GameObjComponent()->FixOnGroundPosition(newPos, false);

	GetOwner()->SetActorLocationAndRotation(newPos, FQuat::MakeFromEuler(newDir));

	FVector vHorizontalVelocity = mVelocity;

	float newSpeed = vHorizontalVelocity.Size();
	if (newSpeed > 0 && runFlag)
	{
		SpeedChangedNotify(newSpeed);
	}
	else
	{
		SpeedChangedNotify(0);
	}

	if (FVector::Dist(vLastPos, newPos) > 0.1)
	{
		entity->SyncAndNotifyVolatileDataToChildren(false);
		vLastPos = newPos;
	}
}

void UAvatarFilterActorComponent::setRunFlag(bool flag)
{
	runFlag = flag;
}

void UAvatarFilterActorComponent::OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID)
{
	float time = GetWorld()->GetTimeSeconds();
	mFilter.output(time);
}

void UAvatarFilterActorComponent::OnGotParentEntity(KBEngine::Entity* parentEnt)
{
	ResetComponent();
}

void UAvatarFilterActorComponent::OnLoseParentEntity()
{
	ResetComponent();
}


