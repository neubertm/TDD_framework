#include "CHalUartIt.hpp"

#include "CppUTestExt/MockSupport.h"


CHalUartIt::CHalUartIt()
{

}
CHalUartIt::~CHalUartIt()
{

}
//IHal
bool CHalUartIt::i_init()
{
  mock().actualCall("CHalUartIt.i_init");
  return mock().boolReturnValue();
}

//IHalUart
void CHalUartIt::transmit(const uint8_t* cu8_pData, const uint32_t cu32_len)
{
  mock().actualCall("CHalUartIt.transmit").withParameter("cu8_pData",cu8_pData).withParameter("cu32_len",cu32_len);
}

void CHalUartIt::receive(uint8_t* u8_pData, const uint32_t cu32_len)
{
  mock().actualCall("CHalUartIt.receive").withParameter("u8_pData",u8_pData).withParameter("cu32_len",cu32_len);
}

void CHalUartIt::abort()
{
  mock().actualCall("CHalUartIt.abort");
}

void CHalUartIt::abortTransmit()
{
  mock().actualCall("CHalUartIt.abortTransmit");
}

void CHalUartIt::abortReceive()
{
  mock().actualCall("CHalUartIt.abortReceive");
}

bool CHalUartIt::isTransmitting()
{
  mock().actualCall("CHalUartIt.isTransmitting");
  return mock().boolReturnValue();
}

bool CHalUartIt::isReceiving()
{
  mock().actualCall("CHalUartIt.isReceiving");
  return mock().boolReturnValue();
}


//IHalNonBlocking
void CHalUartIt::i_notify()
{
  mock().actualCall("CHalUartIt.i_notify");
  uint32_t u32_val = mock().unsignedIntReturnValue();
  po_mHalObserver->i_notify( static_cast<uint8_t>(0x000000ff & u32_val));
}

void CHalUartIt::i_error()
{
  mock().actualCall("CHalUartIt.i_error");
  po_mHalObserver->i_notify();
}

void CHalUartIt::i_timeout()
{
  mock().actualCall("CHalUartIt.i_timeout");
  po_mHalObserver->i_notify();
}
