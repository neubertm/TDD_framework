#include "CDriverUart.hpp"

#include <iostream>

CDriverUart::CDriverUart(IHalUart& ro_halUart)
    : ro_mHalUart { ro_halUart }
    , o_mTXbuff {}
    , o_mRXbuff {}
    , e_mRecvState { RECEIVER_STATUS_OK }
{
}

bool CDriverUart::i_init()
{
    // Initialise HAL
    bool b_lRetVal = ro_mHalUart.i_init();
    if (true == b_lRetVal)
    {
      ro_mHalUart.i_setObserver(this);
    }
    return b_lRetVal;
}

/**
 * @brief Takes one byte from receiver buffer
 * @note Should be used when receiver buffer is not empty, otherwise return value is not valid. To check receiver buffer use i_isUartByteAvailable()
 * @return Received byte
 */
uint8_t CDriverUart::i_readUartByte()
{
    // Save the value to be returned
    return  o_mRXbuff.pull();
}

/**
 * @brief Checks whether there is at least one byte available in receiver buffer
 * @return True = byte is ready to be read, False = nothing to read
 */
bool CDriverUart::i_isUartByteAvailable() const
{
    return o_mRXbuff.isNonEmpty();
}

/**
 * @brief Hand over the buffer to be sent
 * @note In case of insufficient free space in the buffer, nothing is handed over
 * @param pui8_pSendBuf Input buffer
 * @param ui8_pBufLen Size of input buffer
 * @return True on success, false in case of full output buffer
 */
bool CDriverUart::i_writeUartBuf(const uint8_t pui8_pSendBuf[], const uint8_t ui8_pBufLen)
{
    bool b_lRetVal = o_mTXbuff.push(pui8_pSendBuf,ui8_pBufLen);
    if( true == b_lRetVal )
    {
      ro_mHalUart.i_sendByte(o_mTXbuff.pull());
    }


    return b_lRetVal;

}



/**
 * @brief If something wrong happend during receiving, corresponding status is set and can be read with this function
 * @note Call of this function causes status reset
 * @return EReceiverStatus
 */
EReceiverStatus_t CDriverUart::i_getUartReceiverStatus()
{
    // Save receiver status in temp variable
    EReceiverStatus_t e_lRetVal = e_mRecvState;
    // Reset receiver status
    e_mRecvState = RECEIVER_STATUS_OK;
    //Return receiver status before reset
    return e_lRetVal;
}


void CDriverUart::i_notifyTx()
{
    if(o_mTXbuff.isNonEmpty())
    {
      ro_mHalUart.i_sendByte(o_mTXbuff.pull());
    }
}

/**
 * @brief Saves byte to internal receive buffer
 * @param ui8_byte - byte from receiver
 */
void CDriverUart::i_notifyRx(const uint8_t cu8_byte)
{
    // Save byte
    if (false == o_mRXbuff.push(static_cast<const uint8_t*>(&cu8_byte),1))
    {
      e_mRecvState = RECEIVER_STATUS_OVERFLOW;
    }
}

void CDriverUart::i_error(const uint8_t cu8_errID)
{
  (void) cu8_errID;
    // Print error to stderr to avoid
    // unused variable warning
    //std::cerr << ui8_errID;
}
