#pragma once

#include "IHalAdc.hpp"
#include "IHalNonBlocking.hpp"

class CHalAdcIt : public IHalAdc, public IHalNonBlocking
{
  public :
    explicit CHalAdcIt();
    void i_start(uint32_t* pu32_data = nullptr, uint32_t u32_len = 0) override;
    void i_stop() override;
    //void i_getValue(uint32_t& ru32_value, const uint32_t cu32_chanID = 0) override;
    void i_getValue(uint32_t& ru32_value) override;
    bool i_init() override;
    void i_notify() override;
    void i_error() override;
    void i_timeout() override;
};
