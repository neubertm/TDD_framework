#pragma once

#include "IHal.hpp"

class IHalAdc : public IHal
{
  public :
    virtual void i_start(uint32_t* pu32_data = nullptr, uint32_t u32_len = 0) = 0;
    virtual void i_stop() = 0;
    virtual void i_getValue(uint32_t& ru32_value) = 0;
};
