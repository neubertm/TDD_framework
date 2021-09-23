#pragma once

#include "IDriver.hpp"


class ICalcDrv : public IDriver
{
public:
  virtual void i_calculate(const uint8_t pui8_pBuf[],const uint32_t ui32_pBufLength, const uint32_t cu32_startValue) = 0;
};
