extern "C" {
#include "BitInverter.h"
}

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

// helper function to init argument
invertArgument_t argInit(unsigned short x, unsigned short p, unsigned short n)
{
	invertArgument_t arg = {x, p, n};
	
	return arg;
}

TEST_GROUP(BitInverter)
{
  void setup()
  {
  }
  void teardown()
  {
	mock().clear();
  }
};

TEST(BitInverter, inverter_works_in_bounds)
{
	invertArgument_t arg;
	
	arg = argInit(0x00, 3, 2);
	LONGS_EQUAL(0x0C, invert(arg));
	
	arg = argInit(0x00, 1, 2);
	LONGS_EQUAL(0x03, invert(arg));
	
	arg = argInit(0x03, 1, 2);
	LONGS_EQUAL(0x00, invert(arg));
	
	arg = argInit(0xAA, 3, 2);
	LONGS_EQUAL(0xA6, invert(arg));

	// MSB inversion
	arg = argInit(0xF000, 15, 1);
	LONGS_EQUAL(0x7000, invert(arg));
	
	// LSB inversion
	arg = argInit(0xF000, 0, 1);
	LONGS_EQUAL(0xF001, invert(arg));

	// whole range inversion
	arg = argInit(0xAAAA, 15, 16);
	LONGS_EQUAL(0x5555, invert(arg));
}

TEST(BitInverter, inverter_returns_x_value_unchanged_if_parameters_out_of_bounds)
{
	invertArgument_t arg;

	// inversion would modify bit out of range (below LSB)
	arg = argInit(0xAAAA, 3, 5);
	LONGS_EQUAL(0xAAAA, invert(arg));

	// inversion would modify bit out of range (above MSB)
	arg = argInit(0xAAAA, 16, 3);
	LONGS_EQUAL(0xAAAA, invert(arg));
}
