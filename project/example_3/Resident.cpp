#include "Resident.hpp"

using ::CBathroom;

CResident::CResident() : ro_mBathroom(CBathroom::instance())
{

}

CResident::~CResident()
{
	
}


void CResident::washHands()
{
	ro_mBathroom.useWashBasin();
}

void CResident::takeAShower()
{
	ro_mBathroom.useShower();
}

