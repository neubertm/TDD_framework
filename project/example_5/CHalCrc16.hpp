#pragma once

#include "IHalCalc.hpp"
#include "IHalNonBlocking.hpp"



typedef struct CRC
{
  volatile uint32_t DR;
  volatile uint8_t IDR;
  volatile uint8_t RESERVED0;
  volatile uint16_t RESERVED1;
  volatile uint32_t CR;
} SCRC;

class CCrcHandle
{
  public :
    explicit CCrcHandle(uint32_t u32_crcRegAddres);
    SCRC *ptr_mInstance;
    EHAL_Lock e_mLock;
    HalStateEnum e_mState;
  private :
    CCrcHandle();
};


class CHalCrc16 : public IHalCalc, public IHalNonBlocking
{
public :
  explicit CHalCrc16(CCrcHandle& o_handle );
  uint16_t getValue() const;
  bool i_init() override;
  void i_setBufferAndLength(const uint8_t pBuffer[],const uint32_t BufferLength) override;
  void i_notify() override;
  void i_error() override;
  void i_timeout() override;
  void i_calculate(uint16_t u16_startValue = cu16_defaultValue) override;

private:
  static const uint16_t cu16_defaultValue = 0xffff;
  CCrcHandle & s_mHandle;
  const uint8_t *ptru8_mBuffer;
  const uint32_t  u32_mBufferLength;
  CHalCrc16();
};


//class NullObserver : public IHalOBserver
//{
//public :
//  void i_notify();
//  void i_error();
//  void i_timeout();
//};
