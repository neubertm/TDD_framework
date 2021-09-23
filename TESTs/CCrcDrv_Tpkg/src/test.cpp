#include "CCrcDrv.hpp"

// Mocks
#include "CHalCrc16.hpp"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

TEST_GROUP(CCrcDrv)
{


  void teardown()
  {
	  mock().checkExpectations();
	  mock().clear();
  }
};


IGNORE_TEST(CCrcDrv, TemplateIgnoredTestWithHelp)
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

TEST(CCrcDrv, CreateInstanceOfCrcDrv)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");

  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);
}


TEST(CCrcDrv, UseZeroPtrObserver)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  mock().expectOneCall("CHalCrc16.i_notify");
  mock().expectOneCall("NullPtrObserver.i_notify");
  o_hC16.i_notify();

  CCrcDrv o_crc(o_hC16);
}


TEST(CCrcDrv, ConnectDriverAsObserverOfItsHal)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);
}


TEST(CCrcDrv, DriverInitalizationCorrect)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);

  mock().expectOneCall("CHalCrc16.i_init").andReturnValue(true);
  CHECK_TRUE(o_crc.i_init());
  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);
}

TEST(CCrcDrv, DriverInitalizationFail)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);

  mock().expectOneCall("CHalCrc16.i_init").andReturnValue(false);
  CHECK_FALSE(o_crc.i_init());
  CHECK_EQUAL(o_crc.getState(),DRV_STATE_ERROR);
}

TEST(CCrcDrv, DriverCalculateCorrect)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);

  mock().expectOneCall("CHalCrc16.i_init").andReturnValue(true);
  CHECK_TRUE(o_crc.i_init());
  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);

  const uint32_t cu32_len = 10;
  const uint8_t array[cu32_len] = {};

  mock().expectOneCall("CHalCrc16.i_setBufferAndLength")
        .withParameter("pBuffer[]",array)
        .withParameter("BufferLength",cu32_len);
  mock().expectOneCall("CHalCrc16.i_calculate").withParameter("u16_startValue",0xffff);
  o_crc.i_calculate(array,cu32_len);

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_BUSY);

  mock().expectOneCall("CHalCrc16.i_notify");
  o_hC16.i_notify();

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);
}


TEST(CCrcDrv, DriverCalculateCorrectWithNonDefaultValue)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);

  mock().expectOneCall("CHalCrc16.i_init").andReturnValue(true);
  CHECK_TRUE(o_crc.i_init());
  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);

  const uint32_t cu32_len = 10;
  const uint8_t array[cu32_len] = {};
  const uint16_t cu16_defaultValue = 0x1234;

  mock().expectOneCall("CHalCrc16.i_setBufferAndLength")
        .withParameter("pBuffer[]",array)
        .withParameter("BufferLength",cu32_len);
  mock().expectOneCall("CHalCrc16.i_calculate").withParameter("u16_startValue",cu16_defaultValue);
  o_crc.i_calculate(array,cu32_len,cu16_defaultValue);

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_BUSY);

  mock().expectOneCall("CHalCrc16.i_notify");
  o_hC16.i_notify();

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);
}

TEST(CCrcDrv, DriverCalculateError)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);

  mock().expectOneCall("CHalCrc16.i_init").andReturnValue(true);
  CHECK_TRUE(o_crc.i_init());
  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);

  const uint32_t cu32_len = 10;
  const uint8_t array[cu32_len] = {};

  mock().expectOneCall("CHalCrc16.i_setBufferAndLength")
        .withParameter("pBuffer[]",array)
        .withParameter("BufferLength",cu32_len);
  mock().expectOneCall("CHalCrc16.i_calculate").withParameter("u16_startValue",0xffff);
  o_crc.i_calculate(array,cu32_len);

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_BUSY);

  mock().expectOneCall("CHalCrc16.i_error");
  o_hC16.i_error();

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_ERROR);
}

TEST(CCrcDrv, DriverCalculateTimeout)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);

  mock().expectOneCall("CHalCrc16.i_init").andReturnValue(true);
  CHECK_TRUE(o_crc.i_init());
  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);

  const uint32_t cu32_len = 10;
  const uint8_t array[cu32_len] = {};

  mock().expectOneCall("CHalCrc16.i_setBufferAndLength")
        .withParameter("pBuffer[]",array)
        .withParameter("BufferLength",cu32_len);
  mock().expectOneCall("CHalCrc16.i_calculate").withParameter("u16_startValue",0xffff);
  o_crc.i_calculate(array,cu32_len);

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_BUSY);

  mock().expectOneCall("CHalCrc16.i_timeout");
  o_hC16.i_timeout();

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_TIMEOUT);
}

TEST(CCrcDrv, DriverCalculateCorrectGetValue)
{
  mock().expectOneCall("CCrcHandle.CCrcHandle").withParameter("u32_crcRegAddres", 0xdeadbeef);

  CCrcHandle o_crcHandle(0xdeadbeef);

  mock().expectOneCall("CHalCrc16.CHalCrc16");
  CHalCrc16 o_hC16(o_crcHandle);

  CCrcDrv o_crc(o_hC16);

  mock().expectOneCall("IHalNonBlocking.i_setObserver").withParameter("IHalObserver*",dynamic_cast<IHalObserver*>(&o_crc) );
  o_hC16.i_setObserver(&o_crc);

  mock().expectOneCall("CHalCrc16.i_init").andReturnValue(true);
  CHECK_TRUE(o_crc.i_init());
  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);

  const uint32_t cu32_len = 10;
  const uint8_t array[cu32_len] = {};

  mock().expectOneCall("CHalCrc16.i_setBufferAndLength")
        .withParameter("pBuffer[]",array)
        .withParameter("BufferLength",cu32_len);
  mock().expectOneCall("CHalCrc16.i_calculate").withParameter("u16_startValue",0xffff);
  o_crc.i_calculate(array,cu32_len);

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_BUSY);

  mock().expectOneCall("CHalCrc16.i_notify");
  o_hC16.i_notify();

  CHECK_EQUAL(o_crc.getState(),DRV_STATE_READY);

  mock().expectOneCall("CHalCrc16.getValue").andReturnValue(0xbeef);
  uint16_t u16_crc = o_crc.getValue();
  CHECK_EQUAL(0xbeef,u16_crc);
}
