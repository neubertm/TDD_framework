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
	return a/b;
}
