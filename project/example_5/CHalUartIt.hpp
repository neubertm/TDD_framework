#pragma once

#include "IHalUart.hpp"


//typedef struct
//{
//  volatile uint32_t SR;         /*!< Status register,                   Address offset: 0x00 */
//  volatile uint32_t DR;         /*!< Data register,                     Address offset: 0x04 */
//  volatile uint32_t BRR;        /*!< Baud rate register,                Address offset: 0x08 */
//  volatile uint32_t CR1;        /*!< Control register 1,                Address offset: 0x0C */
//  volatile uint32_t CR2;        /*!< Control register 2,                Address offset: 0x10 */
//  volatile uint32_t CR3;        /*!< Control register 3,                Address offset: 0x14 */
//  volatile uint32_t GTPR;       /*!< Guard time and prescaler register, Address offset: 0x18 */
//} SUSART;
//
//class CUsartHandle
//{
//  public :
//    explicit CUsartHandle(uint32_t u32_crcRegAddres);
//    SUSART *ptr_mInstance;
//    EHAL_Lock e_mLock;
//    HalStateEnum e_mState;
//  private :
//    CUsartHandle();
//};

class CHalUartIt : public IHalUart
{
public:
  //explicit CHalUartIt(CUsartHandle& ro_handle);
  explicit CHalUartIt();
  ~CHalUartIt();
  //IHal
  bool i_init() override;

  //IHalUart
  void transmit(const uint8_t* cu8_pData, const uint32_t cu32_len) override;
  void receive(uint8_t* u8_pData, const uint32_t cu32_len) override;
  void abort() override;
  void abortTransmit() override;
  void abortReceive() override;
  bool isTransmitting() override;
  bool isReceiving() override;

  //IHalNonBlocking
  void i_notify() override;
  void i_error() override;
  void i_timeout() override;

private:
  //CUsartHandle& ro_mUsartHandle;
};
