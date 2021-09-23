#pragma once

#include "IConversionDrv.hpp"
#include "IHalObserver.hpp"
#include "IHalAdc.hpp"

class CAdcDrv : public IConversionDrv, public IHalObserver
{
public:
  explicit CAdcDrv(IHalAdc& o_HalAdc);
  void getValue(uint32_t& pu32_data);
  bool i_init() override;
  void i_start(uint32_t* pu32_data = nullptr, uint32_t u32_len = 0) override;
  void i_stop() override;
  void i_notify(uint8_t u8_notifID = 0) override;
  void i_error(uint8_t u8_errorID = 0) override;
  void i_timeout(uint8_t u8_timeoutID = 0) override;
private:
  IHalAdc& o_mHalAdc;

};
