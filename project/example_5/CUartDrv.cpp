#include "CUartDrv.hpp"

CUartDrv::CUartDrv(IHalUart& ro_halUart)
  : ro_mHalUart{ro_halUart}
  , b_mRxIsActive{false}
  , b_mTxIsActive{false}
{

}

bool CUartDrv::isReadyToWrite()
{
  bool b_retVal = (e_mState == DRV_STATE_READY);
  b_retVal = b_retVal || ((e_mState == DRV_STATE_BUSY) && !b_mTxIsActive);
  return b_retVal;
}

uint32_t CUartDrv::rxDataLength()
{
  return 0;
}

void CUartDrv::read(uint8_t* pu8_data, uint32_t& ru32_length)
{
}

void CUartDrv::write(const uint8_t* cpu8_data, const uint32_t cu32_length)
{
  e_mState = DRV_STATE_BUSY;
  b_mTxIsActive = true;
  ro_mHalUart.transmit(cpu8_data,cu32_length);
}

bool CUartDrv::i_init()
{
  bool b_retVal = ro_mHalUart.i_init();
  e_mState = b_retVal ? DRV_STATE_READY : DRV_STATE_ERROR;
  return b_retVal;
}


void CUartDrv::i_notify(uint8_t u8_notifID)
{
  //e_mState = DRV_STATE_READY;
  EHAL_UART_LINE e_uartLineID = static_cast<EHAL_UART_LINE>(u8_notifID);
  if(HAL_UART_RX == e_uartLineID)
  {
    b_mRxIsActive = false;
  }

  if(HAL_UART_TX == e_uartLineID)
  {
    b_mTxIsActive = false;
  }

  if (!(b_mRxIsActive || b_mTxIsActive))
  {
    e_mState = DRV_STATE_READY;
  }
}

void CUartDrv::i_error(uint8_t u8_errorID)
{
  e_mState = DRV_STATE_ERROR;
}

void CUartDrv::i_timeout(uint8_t u8_timeoutID)
{
  e_mState = DRV_STATE_TIMEOUT;
}
