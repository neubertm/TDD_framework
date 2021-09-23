#include "IHal.hpp"

#include "CppUTestExt/MockSupport.h"

IHal::IHal()
{
}

HalStateEnum IHal::getState() const
{
  mock().actualCall("IHal.getState");
  return static_cast<HalStateEnum> (mock().unsignedIntReturnValue());
}
