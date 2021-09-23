#pragma once

#include <cstdint>

class IHalObserver
{
public:
  virtual void i_notify(uint8_t u8_notifID = 0) = 0;
  virtual void i_error(uint8_t u8_errorID = 0) = 0;
  virtual void i_timeout(uint8_t u8_timeoutID = 0) = 0;
};
