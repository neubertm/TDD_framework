#pragma once


template <class T, int N>
class CircBuff
{
public:
  CircBuff();

  virtual ~CircBuff();

  bool push(const T[], unsigned int i32_len);
  bool push(const T);
  T pull();
  bool isNonEmpty() const;
};
