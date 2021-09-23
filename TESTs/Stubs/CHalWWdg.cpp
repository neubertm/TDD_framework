#include "CHalWWdg.hpp"

#include "CppUTestExt/MockSupport.h"


CWWDGHandle::CWWDGHandle(uint32_t u32_crcRegAddres)
{
  mock().actualCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_crcRegAddres);
}


CHalWWdg::CHalWWdg(CWWDGHandle& ro_handle)
  : ro_mWWDGHandle{ro_handle}
{
  mock().actualCall("CHalWWdg.CHalWWdg");
}


bool CHalWWdg::i_init()
{
  mock().actualCall("CHalWWdg.i_init");
  return mock().boolReturnValue();
}
void CHalWWdg::i_start()
{
  mock().actualCall("CHalWWdg.i_start");
}
void CHalWWdg::i_stop()
{
  mock().actualCall("CHalWWdg.i_stop");
}
void CHalWWdg::i_deinit()
{
  mock().actualCall("CHalWWdg.i_deinit");
}
void CHalWWdg::i_refresh()
{
  mock().actualCall("CHalWWdg.i_refresh");
}
