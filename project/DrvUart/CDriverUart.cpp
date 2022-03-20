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

}

/**
 * @brief Checks whether there is at least one byte available in receiver buffer
 * @return True = byte is ready to be read, False = nothing to read
 */
bool CDriverUart::i_isUartByteAvailable() const
{

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

}



/**
 * @brief If something wrong happend during receiving, corresponding status is set and can be read with this function
 * @note Call of this function causes status reset
 * @return EReceiverStatus
 */
EReceiverStatus_t CDriverUart::i_getUartReceiverStatus()
{

}


void CDriverUart::i_notifyTx()
{
}

/**
 * @brief Saves byte to internal receive buffer
 * @param ui8_byte - byte from receiver
 */
void CDriverUart::i_notifyRx(const uint8_t cu8_byte)
{

}

void CDriverUart::i_error(const uint8_t cu8_errID)
{

}
