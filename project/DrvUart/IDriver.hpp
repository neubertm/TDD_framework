#pragma once
#include <cstdint>

typedef enum DrvState
{
  DRV_STATE_RESET     = 0x00U,  /*!< not yet initialized or disabled */
  DRV_STATE_READY     = 0x01U,  /*!< initialized and ready for use   */
  DRV_STATE_BUSY      = 0x02U,  /*!< internal process is ongoing     */
  DRV_STATE_TIMEOUT   = 0x03U,  /*!< timeout state                   */
  DRV_STATE_ERROR     = 0x04U   /*!< error state                     */
} DrvStateEnum;


class IDriver
{
public:
  IDriver() : e_mState{DRV_STATE_RESET} {};

  virtual bool i_init() = 0;

  DrvStateEnum getState() const {return e_mState;}

protected:
  DrvStateEnum e_mState;

};
