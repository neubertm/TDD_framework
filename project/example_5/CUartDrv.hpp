#pragma once

#include "IDriver.hpp"
#include "IHalUart.hpp"

class CUartDrv : public IDriver, public IHalObserver
{
public:
  CUartDrv(IHalUart& ro_halUart);

  bool isReadyToWrite();
  uint32_t rxDataLength();
  void read(uint8_t* pu8_data, uint32_t& ru32_length);
  void write(const uint8_t* cpu8_data, const uint32_t cu32_length);

  //IDriver
  bool i_init() override;

  //IHalObserver
  void i_notify(uint8_t u8_notifID) override;
  void i_error(uint8_t u8_errorID = 0) override;
  void i_timeout(uint8_t u8_timeoutID = 0) override;
private:
  IHalUart& ro_mHalUart;
  bool b_mRxIsActive;
  bool b_mTxIsActive;
};
