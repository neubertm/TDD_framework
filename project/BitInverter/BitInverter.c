/*
 ============================================================================
 Name        : BitInverter.c
 Author      :
 Version     :
 Copyright   :
 Description :
 ============================================================================
 */

#include "BitInverter.h"


unsigned short invert(invertArgument_t argument)
{
	unsigned short mask; 
	unsigned short result;

	// out of bounds (right side)
	if (argument.n > argument.p + 1)
	{
		// no change will be made
		argument.n = 0;
	}

	// move mask to start position
	mask = (0x0001 << argument.p) & 0xffff;

	// set result to default value
	result = argument.x;

	// XOR and shift bits n-times
	for (int i = 0; i < argument.n; i++)
	{
		result ^= mask;
		mask >>= 1;
	}

    return result;
}
