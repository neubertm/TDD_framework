#pragma once

#include "IHalUart.hpp"

class CHalUart : public IHalUart
{
public:
  CHalUart();
  // IHal
  bool i_init() override;

  //IHalUart
  void i_sendByte(const uint8_t cu8_byte) override;
  //void i_setObserver(IHalUartObserver* po_observer) override;
};
