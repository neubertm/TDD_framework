#pragma once

#include "Idriver.hpp"

enum EReceiverStatus_t
{
    RECEIVER_STATUS_OK       = 0,
    RECEIVER_STATUS_OVERFLOW = 1
};

class IDriverUart : public IDriver
{
public:
  virtual uint8_t i_readUartByte() = 0;
  virtual bool i_isUartByteAvailable() const = 0;
  virtual bool i_writeUartBuf(const uint8_t *const pui8_pSendBuf, const uint8_t ui8_pBufLen) = 0;
  virtual EReceiverStatus_t i_getUartReceiverStatus() = 0;
};
