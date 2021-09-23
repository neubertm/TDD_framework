#include "IHalNonBlocking.hpp"
#include "IHalObserver.hpp"

class NullPtrObserver : public IHalObserver
{
public:
  void i_notify()
  {
  }
  void i_error()
  {
  }
  void i_timeout()
  {
  }
};

NullPtrObserver o_nullObserver;



IHalNonBlocking::IHalNonBlocking()
  : po_mHalObserver{&o_nullObserver}
{

}

void IHalNonBlocking::i_setObserver(IHalObserver* po_observer)
{
  po_mHalObserver = po_observer;
}
