#pragma once

#include <cstdint>

template <class T, int N>
class CircBuff
{
public:
  CircBuff();

  virtual ~CircBuff();

  bool push(const T[], int32_t i32_len);
  T pull();
  bool isNonEmpty() const;

  static const int32_t ci32_mMaxBufferContent  = N;
private:
  static const int32_t ci32_mRealBufferSize = ci32_mMaxBufferContent + 1;

  T a_mBuffer[ci32_mRealBufferSize];
  int32_t i32_mTail;
  int32_t i32_mHead;

  void push(const T);
};
