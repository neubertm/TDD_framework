#pragma once

#include "IDriver.hpp"
#include "IHalWdg.hpp"

class CWdgDrv : public IDriver
{
public:
  explicit CWdgDrv(IHalWdg& ro_wdg);
  bool i_init() override;
  void deinit();
  void refresh();
  void start();
  void stop();
  bool isActive() const;
private:
  IHalWdg& ro_mWdg;
};
