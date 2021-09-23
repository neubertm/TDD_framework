#pragma once

#include "IHal.hpp"
#include "IHalObserver.hpp"



class IHalCalc : public IHal
{
  public :
    IHalCalc() : IHal() {}
    virtual void i_setBufferAndLength(const uint8_t pBuffer[],const uint32_t BufferLength) = 0;
    virtual void i_calculate(uint16_t u16_startValue) = 0;
};
