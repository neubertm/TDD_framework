#include "CHalCrc16.hpp"


CCrcHandle::CCrcHandle(uint32_t u32_crcRegAddres)
  : ptr_mInstance{reinterpret_cast<SCRC *>(u32_crcRegAddres)}
  , e_mLock{HAL_UNLOCKED}
  , e_mState{HAL_STATE_RESET}
{

}

CCrcHandle::CCrcHandle()
{

}

CHalCrc16::CHalCrc16(CCrcHandle& o_handle )
    : s_mHandle{o_handle}
    , ptru8_mBuffer{nullptr}
    , u32_mBufferLength{0u}
{
}

void CHalCrc16::i_setObserver(IHalObserver* po_observer)
{
  //TODO continue here
  po_mHalObserver = po_observer;//not finished conversion
}

uint16_t CHalCrc16::getValue() const
{
  return 0x1234;
}

bool CHalCrc16::i_init()
{
  return true;
}

void CHalCrc16::i_setBufferAndLength(const uint8_t pBuffer[],const uint32_t BufferLength)
{
  ptru8_mBuffer = pBuffer;
  u32_mBufferLength = BufferLength;
}


void CHalCrc16::i_calculate(uint16_t u16_startValue)
{

}



void CHalCrc16::i_notify()
{
}

void CHalCrc16::i_error()
{
}

void CHalCrc16::i_timeout()
{
}


void NullObserver::i_notify()
{

}

void NullObserver::i_error()
{

}

void NullObserver::i_timeout()
{

}
