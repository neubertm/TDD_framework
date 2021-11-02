/*
 ============================================================================
 Name        : BitInverter.h
 Author      : 
 Version     :
 Copyright   : 
 Description :
 ============================================================================
 */
#ifndef BitInverter_h
#define BitInverter_h

	
typedef struct
{
    unsigned short x;
    unsigned short p;
    unsigned short n;
} invertArgument_t;

/*
 *  Function invert(x,p,n) returns x with the n bits inverted (1 changed to 0
 *  and vice versa) that begin at position p. I.e., 
 *  x - input value that is used for calculation of the output value
 *  p - position (starting from lowest) of first bit that shall be inverted
 *  n - total number of bits that shall be inverted
 *  Check test cases located in \TESTs\BitInverter_Tpkg\src\test.cpp
 * */
unsigned short invert(invertArgument_t argument);

#endif