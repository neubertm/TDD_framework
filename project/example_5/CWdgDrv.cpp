#include "CWdgDrv.hpp"

CWdgDrv::CWdgDrv(IHalWdg& ro_wdg)
  : ro_mWdg{ro_wdg}
{
}

bool CWdgDrv::i_init()
{
  bool b_retVal = ro_mWdg.i_init();
  if (true == b_retVal)
  {
    e_mState = DRV_STATE_READY;
  }
  else
  {
    e_mState = DRV_STATE_ERROR;
  }
  return b_retVal;
}

void CWdgDrv::deinit()
{
  e_mState = DRV_STATE_RESET;
  ro_mWdg.i_deinit();
}

void CWdgDrv::refresh()
{
  ro_mWdg.i_refresh();
}

void CWdgDrv::start()
{
  e_mState = DRV_STATE_BUSY;
  ro_mWdg.i_start();
}

void CWdgDrv::stop()
{
  e_mState = DRV_STATE_READY;
  ro_mWdg.i_stop();
}

bool CWdgDrv::isActive() const
{
  bool b_retVal = HAL_STATE_BUSY == ro_mWdg.getState();
  b_retVal = b_retVal && (DRV_STATE_BUSY == e_mState);
  return b_retVal;
}
