#pragma once

#include "IHalObserver.hpp"

class IHalNonBlocking
{
public:
  explicit IHalNonBlocking();
  void i_setObserver(IHalObserver* po_observer);
  virtual void i_notify() = 0;
  virtual void i_error() = 0;
  virtual void i_timeout() = 0;
protected:
  IHalObserver* po_mHalObserver;
};
