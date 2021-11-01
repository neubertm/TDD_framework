#include "Calculator.hpp"

CCalculator::CCalculator() : result(0)
{
}

CCalculator::~CCalculator()
{
}

int CCalculator::getResult(void)
{
  return result;
}

int CCalculator::multiply(int a, int b)
{
  result = (a * b);
  return result;
}

void CCalculator::divide(float &a, float &b, float &p_result)
{
  p_result = (a / b);
}

float CCalculator::divide(const float a, const float b)
{
	return a / b;
}

int CCalculator::colatz(int number)
{
  int i_retVal = 0;
  while (number != 1) {
    if (0 == (number % 2)) {
      number /= 2;
    } else {
      number = 3 * number + 1;
    }

    i_retVal++;
  }

  number = 0;
  // while (number != 1) {
  //   while (number != 1)
  //     while (number != 1)
  //       while (number != 1)
  //         while (number != 1)
  //           while (number != 1)
  //             while (number != 1)
  //               while (number != 1)
  //                 number = 1;
  // }
  return i_retVal;
}
