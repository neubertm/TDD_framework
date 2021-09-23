#include "CWdgDrv.hpp"

// Mocks
#include "CHalIWdg.hpp"
#include "CHalWWdg.hpp"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

TEST_GROUP(CWdgDrv)
{


  void teardown()
  {
	  mock().checkExpectations();
	  mock().clear();
  }
};


IGNORE_TEST(CWdgDrv, TemplateIgnoredTestWithHelp)
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

TEST(CWdgDrv, CreateInstanceOfCWdgDrv)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);
  CHECK_EQUAL(DRV_STATE_RESET,o_wdg.getState());

}


TEST(CWdgDrv, WdgDrvInitFalse)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);

  mock().expectOneCall("CHalWWdg.i_init").andReturnValue(false);
  CHECK_FALSE(o_wdg.i_init());
  CHECK_EQUAL(DRV_STATE_ERROR,o_wdg.getState());
}

TEST(CWdgDrv, WdgDrvInitOk)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);

  mock().expectOneCall("CHalWWdg.i_init").andReturnValue(true);
  CHECK_TRUE(o_wdg.i_init());

  CHECK_EQUAL(DRV_STATE_READY,o_wdg.getState());
}

TEST(CWdgDrv, WdgDrvInitOkAndDeinit)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);

  mock().expectOneCall("CHalWWdg.i_init").andReturnValue(true);
  CHECK_TRUE(o_wdg.i_init());

  CHECK_EQUAL(DRV_STATE_READY,o_wdg.getState());

  mock().expectOneCall("CHalWWdg.i_deinit");
  o_wdg.deinit();
  CHECK_EQUAL(DRV_STATE_RESET,o_wdg.getState());
}

TEST(CWdgDrv, WdgDrvStart)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);

  mock().expectOneCall("CHalWWdg.i_init").andReturnValue(true);
  CHECK_TRUE(o_wdg.i_init());

  CHECK_EQUAL(DRV_STATE_READY,o_wdg.getState());

  mock().expectOneCall("CHalWWdg.i_start");
  o_wdg.start();

  CHECK_EQUAL(DRV_STATE_BUSY,o_wdg.getState());
}

TEST(CWdgDrv, WdgDrvStop)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);

  mock().expectOneCall("CHalWWdg.i_init").andReturnValue(true);
  CHECK_TRUE(o_wdg.i_init());

  CHECK_EQUAL(DRV_STATE_READY,o_wdg.getState());

  mock().expectOneCall("CHalWWdg.i_start");
  o_wdg.start();

  CHECK_EQUAL(DRV_STATE_BUSY,o_wdg.getState());

  mock().expectOneCall("CHalWWdg.i_stop");
  o_wdg.stop();

  CHECK_EQUAL(DRV_STATE_READY,o_wdg.getState());
}

TEST(CWdgDrv, WdgDrvRefresh)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);

  mock().expectOneCall("CHalWWdg.i_init").andReturnValue(true);
  CHECK_TRUE(o_wdg.i_init());

  CHECK_EQUAL(DRV_STATE_READY,o_wdg.getState());

  mock().expectOneCall("CHalWWdg.i_start");
  o_wdg.start();

  CHECK_EQUAL(DRV_STATE_BUSY,o_wdg.getState());

  mock().expectOneCall("CHalWWdg.i_refresh");
  o_wdg.refresh();
}


TEST(CWdgDrv, WdgDrvCheckIsActive)
{
  uint32_t u32_address = 0x33516800;

  mock().expectOneCall("CWWDGHandle.CWWDGHandle").withParameter("u32_crcRegAddres",u32_address);
  CWWDGHandle o_wwdgHandle(u32_address);

  mock().expectOneCall("CHalWWdg.CHalWWdg");
  CHalWWdg o_halWWDG(o_wwdgHandle);

  CWdgDrv o_wdg(o_halWWDG);

  mock().expectOneCall("CHalWWdg.i_init").andReturnValue(true);
  CHECK_TRUE(o_wdg.i_init());

  CHECK_EQUAL(DRV_STATE_READY,o_wdg.getState());

  mock().expectOneCall("CHalWWdg.i_start");
  o_wdg.start();

  CHECK_EQUAL(DRV_STATE_BUSY,o_wdg.getState());

  mock().expectOneCall("IHal.getState").andReturnValue(static_cast<uint32_t>(HAL_STATE_BUSY));
  CHECK_TRUE(o_wdg.isActive());

  mock().expectOneCall("CHalWWdg.i_refresh");
  o_wdg.refresh();
}
