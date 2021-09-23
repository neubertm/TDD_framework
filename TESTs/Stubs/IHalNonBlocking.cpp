#include "IHalNonBlocking.hpp"
#include "IHalObserver.hpp"

#include "CppUTestExt/MockSupport.h"

class NullPtrObserver : public IHalObserver
{
public:
  void i_notify(uint8_t u8_notifID)
  {
    (void) u8_notifID;
    mock().actualCall("NullPtrObserver.i_notify");
  }
  void i_error(uint8_t u8_errorID)
  {
    (void) u8_errorID;
    mock().actualCall("NullPtrObserver.i_error");
  }
  void i_timeout(uint8_t u8_timeoutID)
  {
    (void) u8_timeoutID;
    mock().actualCall("NullPtrObserver.i_timeout");
  }
};

NullPtrObserver o_nullObserver;


IHalNonBlocking::IHalNonBlocking()
  : po_mHalObserver{&o_nullObserver}
{

}

void IHalNonBlocking::i_setObserver(IHalObserver* po_observer)
{
  mock().actualCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",po_observer );
  po_mHalObserver = po_observer;
}
