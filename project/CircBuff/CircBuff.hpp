#pragma once

#include <cstdint>

template <class T, int N>
class CircBuff
{
public:
  CircBuff();

  virtual ~CircBuff();

  bool push(const T[], int32_t i32_len);
  bool push(const T);
  T pull();
  bool isNonEmpty() const;

private:
  
};
