#include "IHal.hpp"

IHal::IHal()
  : e_mState{HAL_STATE_RESET}
{
}

HalStateEnum IHal::getState() const
{
  return e_mState;
}
