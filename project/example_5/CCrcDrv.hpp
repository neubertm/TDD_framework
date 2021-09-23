#pragma once

#include "ICalcDrv.hpp"
#include "CHalCrc16.hpp"
#include "IHalObserver.hpp"


class CCrcDrv : public ICalcDrv, public IHalObserver
{

public:
  explicit CCrcDrv(CHalCrc16& hal);
  ~CCrcDrv();
  uint16_t getValue() const;
  bool i_init() override;
  void i_calculate(const uint8_t pui8_pBuf[],const uint32_t ui32_pBufLength, const uint32_t cu32_startValue = cu32_defaultStartVal) override;

  void i_notify(uint8_t u8_notifID = 0) override;
  void i_error(uint8_t u8_errorID = 0) override;
  void i_timeout(uint8_t u8_timeoutID = 0) override;

private:
  static const uint32_t cu32_defaultStartVal = 0x0000ffff;
  CHalCrc16& o_mHalCrc16;
};
