#include "CAdcDrv.hpp"

CAdcDrv::CAdcDrv(IHalAdc& o_HalAdc)
  : o_mHalAdc{o_HalAdc}
{

}

void CAdcDrv::getValue(uint32_t& pu32_data)
{
  o_mHalAdc.i_getValue(pu32_data);
}

bool CAdcDrv::i_init()
{
  bool b_retval = o_mHalAdc.i_init();
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


void CAdcDrv::i_start(uint32_t* pu32_data, uint32_t u32_len)
{
  e_mState = DRV_STATE_BUSY;
  o_mHalAdc.i_start(pu32_data, u32_len);
}

void CAdcDrv::i_stop()
{
  e_mState = DRV_STATE_READY;
  o_mHalAdc.i_stop();
}

void CAdcDrv::i_notify(uint8_t u8_notifID)
{
  e_mState = DRV_STATE_READY;
}

void CAdcDrv::i_error(uint8_t u8_errorID)
{
  e_mState = DRV_STATE_ERROR;
}

void CAdcDrv::i_timeout(uint8_t u8_timeoutID)
{
  e_mState = DRV_STATE_TIMEOUT;
}
