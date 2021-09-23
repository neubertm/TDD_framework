#include "CAdcDrv.hpp"

// Mocks
#include "CHalAdcIt.hpp"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

TEST_GROUP(CAdcDrv)
{


  void teardown()
  {
	  mock().checkExpectations();
	  mock().clear();
  }
};


IGNORE_TEST(CAdcDrv, TemplateIgnoredTestWithHelp)
{
	/*
	CHECK(boolean condition) - checks any boolean result.
	CHECK_TEXT(boolean condition, text) - checks any boolean result and prints text on failure.
	CHECK_FALSE(condition) - checks any boolean result
	CHECK_EQUAL(expected, actual) - checks for equality between entities using ==. So if you have a class that supports operator==() you can use this macro to compare two instances. You will also need to add a StringFrom() function like those found in SimpleString. This is for printing the objects when the check failed.
	CHECK_COMPARE(first, relop, second) - checks thats a relational operator holds between two entities. On failure, prints what both operands evaluate to.
	CHECK_THROWS(expected_exception, expression) - checks if expression throws expected_exception (e.g. std::exception). CHECK_THROWS is only available if CppUTest is built with the Standard C++ Library (default).
	STRCMP_EQUAL(expected, actual) - checks const char* strings for equality using strcmp().
	STRNCMP_EQUAL(expected, actual, length) - checks const char* strings for equality using strncmp().
	STRCMP_NOCASE_EQUAL(expected, actual) - checks const char* strings for equality, not considering case.
	STRCMP_CONTAINS(expected, actual) - checks whether const char* actual contains const char* expected.
	LONGS_EQUAL(expected, actual) - compares two numbers.
	UNSIGNED_LONGS_EQUAL(expected, actual) - compares two positive numbers.
	BYTES_EQUAL(expected, actual) - compares two numbers, eight bits wide.
	POINTERS_EQUAL(expected, actual) - compares two pointers.
	DOUBLES_EQUAL(expected, actual, tolerance) - compares two floating point numbers within some tolerance
	FUNCTIONPOINTERS_EQUAL(expected, actual) - compares two void (*)() function pointers
	MEMCMP_EQUAL(expected, actual, size) - compares two areas of memory
	BITS_EQUAL(expected, actual, mask) - compares expected to actual bit by bit, applying mask
	FAIL(text) - always fails
	*/
}

TEST(CAdcDrv, CreateInstanceOfAdcDrv)
{
  CHalAdcIt o_halAdcIt;
  CAdcDrv o_adc(o_halAdcIt);
}

TEST(CAdcDrv, CallInitDriverOk)
{
  CHalAdcIt o_halAdcIt;
  CAdcDrv o_adc(o_halAdcIt);
  mock().expectOneCall("CHalAdcIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_adc.i_init());
  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());
}

TEST(CAdcDrv, CallInitDriverFalse)
{
  CHalAdcIt o_halAdcIt;
  CAdcDrv o_adc(o_halAdcIt);
  mock().expectOneCall("CHalAdcIt.i_init").andReturnValue(false);
  CHECK_FALSE(o_adc.i_init());
  CHECK_EQUAL(DRV_STATE_ERROR, o_adc.getState());
}

TEST(CAdcDrv, getValue)
{
  CHalAdcIt o_halAdcIt;
  CAdcDrv o_adc(o_halAdcIt);
  mock().expectOneCall("CHalAdcIt.i_getValue").andReturnValue(0xaabbccdd);
  uint32_t u32_val = 0;
  o_adc.getValue(u32_val);

  CHECK_EQUAL(0xaabbccdd,u32_val);
}


TEST(CAdcDrv, CallStartAdc)
{
  CHalAdcIt o_halAdcIt;

  CAdcDrv o_adc(o_halAdcIt);

  mock().expectOneCall("CHalAdcIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_adc.i_init());

  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());

  const uint32_t cu32_len = 10;
  uint32_t u32a_data[cu32_len] = {0};

  mock().expectOneCall("CHalAdcIt.i_start")
        .withParameter("pu32_data", u32a_data)
        .withParameter("u32_len", cu32_len);
  o_adc.i_start(u32a_data,cu32_len);

  CHECK_EQUAL(DRV_STATE_BUSY, o_adc.getState());
}

TEST(CAdcDrv, ConnectObserver)
{
  CHalAdcIt o_halAdcIt;

  CAdcDrv o_adc(o_halAdcIt);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_adc) );
  o_halAdcIt.i_setObserver(&o_adc);

}


TEST(CAdcDrv, CallStartAndNotifyFinishOk)
{
  CHalAdcIt o_halAdcIt;

  CAdcDrv o_adc(o_halAdcIt);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_adc) );
  o_halAdcIt.i_setObserver(&o_adc);

  mock().expectOneCall("CHalAdcIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_adc.i_init());

  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());

  const uint32_t cu32_len = 10;
  uint32_t u32a_data[cu32_len] = {0};

  mock().expectOneCall("CHalAdcIt.i_start")
        .withParameter("pu32_data", u32a_data)
        .withParameter("u32_len", cu32_len);
  o_adc.i_start(u32a_data,cu32_len);

  CHECK_EQUAL(DRV_STATE_BUSY, o_adc.getState());

  mock().expectOneCall("CHalAdcIt.i_notify");
  o_halAdcIt.i_notify();

  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());

}

TEST(CAdcDrv, CallStartAndNotifyFinishError)
{
  CHalAdcIt o_halAdcIt;

  CAdcDrv o_adc(o_halAdcIt);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_adc) );
  o_halAdcIt.i_setObserver(&o_adc);

  mock().expectOneCall("CHalAdcIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_adc.i_init());

  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());

  const uint32_t cu32_len = 10;
  uint32_t u32a_data[cu32_len] = {0};

  mock().expectOneCall("CHalAdcIt.i_start")
        .withParameter("pu32_data", u32a_data)
        .withParameter("u32_len", cu32_len);
  o_adc.i_start(u32a_data,cu32_len);

  CHECK_EQUAL(DRV_STATE_BUSY, o_adc.getState());

  mock().expectOneCall("CHalAdcIt.i_error");
  o_halAdcIt.i_error();

  CHECK_EQUAL(DRV_STATE_ERROR, o_adc.getState());
}

TEST(CAdcDrv, CallStartAndNotifyFinishTimeout)
{
  CHalAdcIt o_halAdcIt;

  CAdcDrv o_adc(o_halAdcIt);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_adc) );
  o_halAdcIt.i_setObserver(&o_adc);

  mock().expectOneCall("CHalAdcIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_adc.i_init());

  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());

  const uint32_t cu32_len = 10;
  uint32_t u32a_data[cu32_len] = {0};

  mock().expectOneCall("CHalAdcIt.i_start")
        .withParameter("pu32_data", u32a_data)
        .withParameter("u32_len", cu32_len);
  o_adc.i_start(u32a_data,cu32_len);

  CHECK_EQUAL(DRV_STATE_BUSY, o_adc.getState());

  mock().expectOneCall("CHalAdcIt.i_timeout");
  o_halAdcIt.i_timeout();

  CHECK_EQUAL(DRV_STATE_TIMEOUT, o_adc.getState());
}

TEST(CAdcDrv, CallStartAndStopHalByDriver)
{
  CHalAdcIt o_halAdcIt;

  CAdcDrv o_adc(o_halAdcIt);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_adc) );
  o_halAdcIt.i_setObserver(&o_adc);

  mock().expectOneCall("CHalAdcIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_adc.i_init());

  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());

  const uint32_t cu32_len = 10;
  uint32_t u32a_data[cu32_len] = {0};

  mock().expectOneCall("CHalAdcIt.i_start")
        .withParameter("pu32_data", u32a_data)
        .withParameter("u32_len", cu32_len);
  o_adc.i_start(u32a_data,cu32_len);

  CHECK_EQUAL(DRV_STATE_BUSY, o_adc.getState());

  mock().expectOneCall("CHalAdcIt.i_stop");
  o_adc.i_stop();

  CHECK_EQUAL(DRV_STATE_READY, o_adc.getState());
}
