#pragma once

#include "IHal.hpp"
#include "IHalNonBlocking.hpp"


class IHalUartMini : public IHal, public IHalNonBlocking
{
public:
  virtual void i_sendByte(const uint8_t cu8_byte);
  virtual void i_notifyObsTransmit(); //isr
  virtual void i_notifyObsReaded();   //isr

};
