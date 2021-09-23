#include "lib/Bathroom.hpp"
#include "CppUTestExt/MockSupport.h"

CBathroom::CBathroom()
{	
	mock().actualCall("CBathroom.CBathroom");
}

CBathroom::~CBathroom()
{	
	
}

void CBathroom::useShower(void)
{
	mock().actualCall("CBathroom.useShower");
}
			
void CBathroom::useWashBasin(void)
{
	mock().actualCall("CBathroom.useWashBasin");
}