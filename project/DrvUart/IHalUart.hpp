#pragma once


#include "IHal.hpp"
#include "IHalUartObserver.hpp"

class IHalUart : public IHal
{
public:
  virtual void i_sendByte(const uint8_t cu8_byte) = 0;
  void i_setObserver(IHalUartObserver* po_observer);
protected:
  IHalUartObserver* po_mObserver;
};
