#include "CircBuff.hpp"

template class CircBuff<uint8_t,10>;

template <class T, int N>
CircBuff< T, N>::CircBuff()
  : a_mBuffer{}
  , i32_mTail{0}
  , i32_mHead{0}
{
}

template <class T, int N>
CircBuff< T, N>::~CircBuff()
{
}

template <class T, int N>
void CircBuff< T, N>::push(const T value)
{
  // Write byte into buffer
  a_mBuffer[i32_mHead] = value;

  // If head is going out of range
  if (i32_mHead  >= ci32_mMaxBufferContent)
  {
      // Wrap around
      i32_mHead = 0;
  }
  else
  {
      i32_mHead++;
  }
}


template <class T, int N>
bool CircBuff< T, N>::push(const T T_array[], int32_t i32_len)
{
  bool b_lRetVal = false;
  if( (i32_len > 0) && (((i32_mTail - i32_mHead + ci32_mMaxBufferContent) % ci32_mRealBufferSize) >= i32_len ) )
  {
      // Copy buffer over with this loop
      for (int i = 0; i < i32_len; i++)
      {
          push(T_array[i]);
      }
      b_lRetVal = true;
  }
  return b_lRetVal;
}

template <class T, int N>
T CircBuff< T, N>::pull()
{
  T T_retVal = a_mBuffer[i32_mTail];
  // If tail is going out of range
  if(i32_mTail != i32_mHead)
  {
    if (i32_mTail >= ci32_mMaxBufferContent)
    {
        // Wrap around
        i32_mTail = 0;
    }
    else
    {
        i32_mTail++;
    }
  }

  return T_retVal;
}

template <class T, int N>
bool CircBuff< T, N>::isNonEmpty() const
{
  return i32_mTail != i32_mHead;
}
