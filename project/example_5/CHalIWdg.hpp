#pragma once

#include "IHalWdg.hpp"

typedef struct IWDG
{
  volatile uint32_t KR;   /*!< IWDG Key register,       Address offset: 0x00 */
  volatile uint32_t PR;   /*!< IWDG Prescaler register, Address offset: 0x04 */
  volatile uint32_t RLR;  /*!< IWDG Reload register,    Address offset: 0x08 */
  volatile uint32_t SR;   /*!< IWDG Status register,    Address offset: 0x0C */
} SIWDG;

class CIWDGHandle
{
  public :
    explicit CIWDGHandle(uint32_t u32_crcRegAddres);
    SIWDG *ptr_mInstance;
    EHAL_Lock e_mLock;
    HalStateEnum e_mState;
  private :
    CIWDGHandle();
};


class CHalIWdg : public IHalWdg
{
public:
  explicit CHalIWdg(CIWDGHandle& ro_handle);
  bool i_init() override;
  void i_start() override;
  void i_stop() override;
  void i_deinit() override;
  void i_refresh() override;
private:
  CIWDGHandle& ro_mIWDGHandle;
};
