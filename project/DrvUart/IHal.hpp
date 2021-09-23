#pragma once

#include <cstdint>


/**
  * @brief  HAL Lock structures definition, not sure if this is realy necessary
  */
typedef enum
{
  HAL_UNLOCKED = 0x00U,
  HAL_LOCKED   = 0x01U
} EHAL_Lock;

/**
  * @brief HalState enum definition
  */
typedef enum HalState
{
  HAL_STATE_RESET     = 0x00U,  /*!< CALC not yet initialized or disabled */
  HAL_STATE_READY     = 0x01U,  /*!< CALC initialized and ready for use   */
  HAL_STATE_BUSY      = 0x02U,  /*!< CALC internal process is ongoing     */
  HAL_STATE_TIMEOUT   = 0x03U,  /*!< CALC timeout state                   */
  HAL_STATE_ERROR     = 0x04U   /*!< CALC error state                     */
} HalStateEnum;

class IHal
{
public:
    IHal() : e_mState{HAL_STATE_RESET} {};
    /**
      * @brief function returning current HAL status
      */
    HalStateEnum getState() const;
    /**
      * @brief function function initialize HAL&HW to the logiacal deafault situation and return status
      */
    virtual bool i_init() = 0;
protected :
    HalStateEnum e_mState;
private:
};
