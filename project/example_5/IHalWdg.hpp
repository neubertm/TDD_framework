#pragma once

#include "IHal.hpp"

class IHalWdg : public IHal
{
public:
  /**
    * @brief function start counter -> its necessary to call i_refresh
    */
  virtual void i_start() = 0;

  /**
    * @brief function stop counter -> its necessary to call i_refresh
    */
  virtual void i_stop() = 0;

  /**
    * @brief function stop and deinitialize wdg counter, for next run is necessary to call init
    */
  virtual void i_deinit() = 0;
  /**
    * @brief function reset wdg internal counter
    */
  virtual void i_refresh() = 0;
};
