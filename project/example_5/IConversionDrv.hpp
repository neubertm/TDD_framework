#pragma once

#include "IDriver.hpp"


class IConversionDrv : public IDriver
{
public:
  virtual void i_start(uint32_t* pu32_data = nullptr, uint32_t u32_len = 0) = 0;
  virtual void i_stop() = 0;

};
