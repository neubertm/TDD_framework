#include "CUartDrv.hpp"

// Mocks
#include "CHalUartIt.hpp"


//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

TEST_GROUP(CUartDrv)
{


  void teardown()
  {
	  mock().checkExpectations();
	  mock().clear();
  }
};


IGNORE_TEST(CUartDrv, TemplateIgnoredTestWithHelp)
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

TEST(CUartDrv, CreateInstanceOfCUartDrv)
{
  CHalUartIt o_halUart;
  CUartDrv o_uartDrv(o_halUart);

}

TEST(CUartDrv, CreateInstanceOfCUartDrvConnectObserver)
{
  CHalUartIt o_halUart;
  CUartDrv o_uartDrv(o_halUart);


  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_uartDrv));
  o_halUart.i_setObserver(&o_uartDrv);
}

TEST(CUartDrv, InitializationOk)
{
  CHalUartIt o_halUart;
  CUartDrv o_uartDrv(o_halUart);


  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_uartDrv));
  o_halUart.i_setObserver(&o_uartDrv);

  mock().expectOneCall("CHalUartIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_uartDrv.i_init());
  CHECK_EQUAL(DRV_STATE_READY, o_uartDrv.getState());
}

TEST(CUartDrv, InitializationFalse)
{
  CHalUartIt o_halUart;
  CUartDrv o_uartDrv(o_halUart);


  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_uartDrv));
  o_halUart.i_setObserver(&o_uartDrv);

  mock().expectOneCall("CHalUartIt.i_init").andReturnValue(false);
  CHECK_FALSE(o_uartDrv.i_init());
  CHECK_EQUAL(DRV_STATE_ERROR, o_uartDrv.getState());
}

TEST(CUartDrv, ReadyToWrite_WeAreInReadyState)
{
  CHalUartIt o_halUart;
  CUartDrv o_uartDrv(o_halUart);


  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_uartDrv));
  o_halUart.i_setObserver(&o_uartDrv);

  mock().expectOneCall("CHalUartIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_uartDrv.i_init());


  CHECK_TRUE(o_uartDrv.isReadyToWrite());
}


TEST(CUartDrv, ReadyToWrite_WriteData)
{
  CHalUartIt o_halUart;
  CUartDrv o_uartDrv(o_halUart);


  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_uartDrv));
  o_halUart.i_setObserver(&o_uartDrv);

  mock().expectOneCall("CHalUartIt.i_init").andReturnValue(true);
  CHECK_TRUE(o_uartDrv.i_init());


  CHECK_TRUE(o_uartDrv.isReadyToWrite());

  const uint32_t cu32_length = 10;
  uint8_t au8_data[cu32_length] = {1,2,3,4,5,6,7,8,9};
  mock().expectOneCall("CHalUartIt.transmit").withParameter("cu8_pData",const_cast<const uint8_t*>(au8_data)).withParameter("cu32_len",cu32_length);
  o_uartDrv.write(au8_data,cu32_length);

  CHECK_FALSE(o_uartDrv.isReadyToWrite())

  //interrupt call HAL -> write to observer inform that we can write again
  mock().expectOneCall("CHalUartIt.i_notify").andReturnValue(static_cast<uint32_t>(HAL_UART_TX));
  o_halUart.i_notify();

  CHECK_TRUE(o_uartDrv.isReadyToWrite())
}
