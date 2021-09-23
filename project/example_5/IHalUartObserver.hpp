#pragma once

#include <cstdint>

class IHalUartObserver
{
public:
  virtual void i_notifyTx() = 0;
  virtual void i_notifyRx(const uint8_t cu8_byte) = 0;
  virtual void i_error() = 0;
};
