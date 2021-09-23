#pragma once

#include "IDriverUart.hpp"
#include "IHalUartObserver.hpp"

#include "IHalUart.hpp"
#include "CircBuff.hpp"


class CDriverUart : public IDriverUart, public IHalUartObserver
{
public:
  explicit CDriverUart(IHalUart& ro_halUart);

  //IDriver
  bool i_init() override;

  //IDriverUart
  uint8_t i_readUartByte() override;
  bool i_isUartByteAvailable() const override;
  bool i_writeUartBuf(const uint8_t pui8_pSendBuf[], const uint8_t ui8_pBufLen) override;
  EReceiverStatus_t i_getUartReceiverStatus() override;

  //IHalUartObserver
  void i_notifyTx() override;
  void i_notifyRx(const uint8_t cu8_byte) override;
  void i_error(const uint8_t cu8_errID) override;

  static const uint8_t cui8_mMaxBufferContent  = 10;
private:

  IHalUart& ro_mHalUart;

  static const uint16_t cui16_mErrorRange   = 0x8000;

  // Transmit
  CircBuff<uint8_t,cui8_mMaxBufferContent> o_mTXbuff;


  // Receive
  CircBuff<uint8_t,cui8_mMaxBufferContent> o_mRXbuff;


  EReceiverStatus_t e_mRecvState;
};
