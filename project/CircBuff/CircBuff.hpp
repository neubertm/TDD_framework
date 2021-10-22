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
  static const int32_t ci32_mMaxBufferContent  = N;
  static const int32_t ci32_mRealBufferSize = ci32_mMaxBufferContent + 1;
  
  void add(const T);

  T a_mBuffer[ci32_mRealBufferSize];
  int32_t i32_mTail;
  int32_t i32_mHead;

};
