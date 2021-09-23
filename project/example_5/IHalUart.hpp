#pragma once

#include "IHal.hpp"
#include "IHalNonBlocking.hpp"

typedef enum
{
  HAL_UART_RX = 0x00U,
  HAL_UART_TX = 0x01U
} EHAL_UART_LINE;

class IHalUart : public IHal, public IHalNonBlocking
{
public:
  virtual void transmit(const uint8_t* cu8_pData, const uint32_t cu32_len) = 0;
  virtual void receive(uint8_t* cu8_pData, const uint32_t cu32_len) = 0;

  virtual void abort() = 0;
  virtual void abortTransmit() = 0;
  virtual void abortReceive() = 0;
  virtual bool isTransmitting() = 0;
  virtual bool isReceiving() = 0;
};
