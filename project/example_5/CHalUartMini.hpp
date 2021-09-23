#pragma once

#include "IHalUartMini.hpp"

class CHalUartMini : public IHalUartMini
{
  explicit CHalUartMini();
  //IHal
  bool i_init();
  //IHalUartMini
  void i_sendByte(const uint8_t cu8_byte);
  void i_notifyObsTransmit(); //isr
  void i_notifyObsReaded();   //isr
}
