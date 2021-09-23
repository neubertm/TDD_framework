#include "CHalAdcIt.hpp"
#include "CppUTestExt/MockSupport.h"

CHalAdcIt::CHalAdcIt()
{
}


void CHalAdcIt::i_start(uint32_t* pu32_data, uint32_t u32_len)
{
  mock().actualCall("CHalAdcIt.i_start")
        .withParameter("pu32_data",pu32_data)
        .withParameter("u32_len",u32_len);
}

void CHalAdcIt::i_stop()
{
  mock().actualCall("CHalAdcIt.i_stop");
}

void CHalAdcIt::i_getValue(uint32_t& ru32_value)
{
  mock().actualCall("CHalAdcIt.i_getValue");
  ru32_value =  mock().unsignedIntReturnValue();
}

bool CHalAdcIt::i_init()
{
  mock().actualCall("CHalAdcIt.i_init");
  return mock().boolReturnValue();
}



void CHalAdcIt::i_notify()
{
  mock().actualCall("CHalAdcIt.i_notify");
  po_mHalObserver->i_notify();
}

void CHalAdcIt::i_error()
{
  mock().actualCall("CHalAdcIt.i_error");
  po_mHalObserver->i_error();
}

void CHalAdcIt::i_timeout()
{
  mock().actualCall("CHalAdcIt.i_timeout");
  po_mHalObserver->i_timeout();
}
