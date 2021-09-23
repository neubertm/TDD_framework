#include "CCrcDrv.hpp"


CCrcDrv::CCrcDrv(CHalCrc16& hal)
  : o_mHalCrc16{hal}
{
}

CCrcDrv::~CCrcDrv()
{

}

bool CCrcDrv::i_init()
{
  bool b_retval = o_mHalCrc16.i_init();
  if(true == b_retval)
  {
      e_mState = DRV_STATE_READY;
  }
  else
  {
      e_mState = DRV_STATE_ERROR;
  }
  return b_retval;
}

void CCrcDrv::i_calculate(const uint8_t pui8_pBuf[],const uint32_t ui32_pBufLength, const uint32_t cu32_startValue)
{
  e_mState = DRV_STATE_BUSY;
  o_mHalCrc16.i_setBufferAndLength(pui8_pBuf,ui32_pBufLength);
  o_mHalCrc16.i_calculate(static_cast<uint16_t>(0x0000FFFF & cu32_startValue));
}

uint16_t CCrcDrv::getValue() const
{
  return o_mHalCrc16.getValue();
}


void CCrcDrv::i_notify(uint8_t u8_notifID)
{
  e_mState = DRV_STATE_READY;
}

void CCrcDrv::i_error(uint8_t u8_errorID)
{
  e_mState = DRV_STATE_ERROR;
}

void CCrcDrv::i_timeout(uint8_t u8_timeoutID)
{
  e_mState = DRV_STATE_TIMEOUT;
}
