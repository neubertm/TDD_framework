#include "CHalCrc16.hpp"
#include "CppUTestExt/MockSupport.h"


CCrcHandle::CCrcHandle(uint32_t u32_crcRegAddres)
  : ptr_mInstance{reinterpret_cast<SCRC *>(u32_crcRegAddres)}
  , e_mLock{HAL_UNLOCKED}
  , e_mState{HAL_STATE_RESET}
{
  mock().actualCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", u32_crcRegAddres);
}

CCrcHandle::CCrcHandle()
{
  mock().actualCall("CCrcHandle.CCrcHandle");
}

CHalCrc16::CHalCrc16(CCrcHandle& o_handle )
  :  IHalCalc()
  ,  s_mHandle{o_handle}
  ,  ptru8_mBuffer{nullptr}
  ,  u32_mBufferLength{0x00}

{
  mock().actualCall("CHalCrc16.CHalCrc16");
}


uint16_t CHalCrc16::getValue() const
{
  mock().actualCall("CHalCrc16.getValue");
  return static_cast<uint16_t>(mock().intReturnValue());
}

bool CHalCrc16::i_init()
{
  mock().actualCall("CHalCrc16.i_init");
  return mock().boolReturnValue();
}

void CHalCrc16::i_setBufferAndLength(const uint8_t pBuffer[],const uint32_t BufferLength)
{
  mock().actualCall("CHalCrc16.i_setBufferAndLength")
        .withParameter("pBuffer[]",pBuffer)
        .withParameter("BufferLength",BufferLength);
}


void CHalCrc16::i_calculate(uint16_t u16_startValue)
{
  mock().actualCall("CHalCrc16.i_calculate").withParameter("u16_startValue",u16_startValue);
}


void CHalCrc16::i_notify()
{
  mock().actualCall("CHalCrc16.i_notify");
  po_mHalObserver->i_notify();
}

void CHalCrc16::i_error()
{
  mock().actualCall("CHalCrc16.i_error");
  po_mHalObserver->i_error();
}

void CHalCrc16::i_timeout()
{
  mock().actualCall("CHalCrc16.i_timeout");
  po_mHalObserver->i_timeout();
}
