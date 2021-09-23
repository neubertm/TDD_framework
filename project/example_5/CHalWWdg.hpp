#pragma once

#include "IHalWdg.hpp"

typedef struct WWDG
{
  volatile uint32_t CR;   /*!< WWDG Control register,       Address offset: 0x00 */
  volatile uint32_t CFR;  /*!< WWDG Configuration register, Address offset: 0x04 */
  volatile uint32_t SR;   /*!< WWDG Status register,        Address offset: 0x08 */
} SWWDG;

class CWWDGHandle
{
  public :
    explicit CWWDGHandle(uint32_t u32_crcRegAddres);
    SWWDG *ptr_mInstance;
    EHAL_Lock e_mLock;
    HalStateEnum e_mState;
  private :
    CWWDGHandle();
};


class CHalWWdg : public IHalWdg
{
public:
  explicit CHalWWdg(CWWDGHandle& ro_handle);
  bool i_init() override;
  void i_start() override;
  void i_stop() override;
  void i_deinit() override;
  void i_refresh() override;
private:
  CWWDGHandle& ro_mWWDGHandle;
};
