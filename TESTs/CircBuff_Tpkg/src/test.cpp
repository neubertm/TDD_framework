#include "CircBuff.hpp"
#include <cstdint>

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

class CBuff: public CircBuff<uint8_t, 10>
{
public:
  CBuff(){}
  ~CBuff(){}
};


TEST_GROUP(CircBuff)
{
  void setup()
  {
  }
  void teardown()
  {
	mock().clear();
  }
};


IGNORE_TEST(CircBuff, TemplateIgnoredTestWithHelp)
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

TEST(CircBuff, DerivedCircBuffer)
{
  CBuff o_cb;
}

TEST(CircBuff, CreateCircBuffer)
{
	CircBuff<uint8_t, 10> o_lCB;

	mock().checkExpectations();
}

TEST(CircBuff, CreateCircBufferDynamic)
{
	CircBuff<uint8_t, 10>* po_lCB = new CircBuff<uint8_t, 10>();
	delete po_lCB;

	mock().checkExpectations();
}


TEST(CircBuff, CircBufferIsEmptyAfterInitialization)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, CircBufferPushOneBytePullOneByte)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

	uint8_t array[10] = {1,2,3,4,5,6,7,8,9,10};
	o_lCB.push(array,1);

	CHECK_TRUE(o_lCB.isNonEmpty());

	uint8_t u8 = o_lCB.pull();
	CHECK_EQUAL(u8,array[0]);

	CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, CircBufferPushMaxArray)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

  uint8_t array[10] = {1,2,3,4,5,6,7,8,9,10};
	CHECK_TRUE(o_lCB.push(array,10));
	//o_lCB.push(5);

	CHECK_TRUE(o_lCB.isNonEmpty());
	for(int i = 0;i<10;++i)
	{
		CHECK_EQUAL(array[i],o_lCB.pull());
	}

	mock().checkExpectations();
}

TEST(CircBuff, CircBufferPushOversizedArray)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

  uint8_t array[11] = {1,2,3,4,5,6,7,8,9,10,11};
	CHECK_FALSE(o_lCB.push(array,11));
	//o_lCB.push(5);

	CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, CircBufferFullBuffer)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

  uint8_t array[11] = {1,2,3,4,5,6,7,8,9,10,11};
	CHECK_TRUE(o_lCB.push(array,10));


	CHECK_FALSE(o_lCB.push(array,1));

	for(int i=0; i<10;++i)
	{
		CHECK_TRUE(o_lCB.isNonEmpty());
		CHECK_EQUAL(array[i], o_lCB.pull());
	}

	//o_lCB.push(5);
  CHECK_FALSE(o_lCB.isNonEmpty());


	mock().checkExpectations();
}

TEST(CircBuff, CircBufferFullBufferShiftOne)
{
	CircBuff<uint8_t, 10> o_lCB;
	int32_t i32Tail = 0;
	int32_t i32Head = 0;

	CHECK_FALSE(o_lCB.isNonEmpty());

  uint8_t array[11] = {1,2,3,4,5,6,7,8,9,10,11};

	CHECK_TRUE(o_lCB.push(array,1));
	i32Head++;
	CHECK_EQUAL(array[0], o_lCB.pull());
	i32Tail++;

	CHECK_TRUE(o_lCB.push(array,10));


	CHECK_FALSE(o_lCB.push(array,1));

	for(int i=0; i<10;++i)
	{
		CHECK_TRUE(o_lCB.isNonEmpty());
		CHECK_EQUAL(array[i], o_lCB.pull());
	}

	//o_lCB.push(5);
  CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, CircBufferPushHalfMaxArrayReadAllAndPushMaxArrayAgain)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

  uint8_t array[10] = {1,2,3,4,5,6,7,8,9,10};
	//uint8_t array2[10] = {0};
	CHECK_TRUE(o_lCB.push(array,5));
	//o_lCB.push(5);

	CHECK_TRUE(o_lCB.isNonEmpty());
	for(int i = 0;i<5;++i)
	{
		CHECK_EQUAL(array[i],o_lCB.pull());
	}

	CHECK_FALSE(o_lCB.isNonEmpty());

	CHECK_TRUE(o_lCB.push(array,10));
	CHECK_TRUE(o_lCB.isNonEmpty());

  BYTES_EQUAL(array[0], o_lCB.pull());
	BYTES_EQUAL(array[1], o_lCB.pull());
	BYTES_EQUAL(array[2], o_lCB.pull());
	BYTES_EQUAL(array[3], o_lCB.pull());
	BYTES_EQUAL(array[4], o_lCB.pull());
	BYTES_EQUAL(array[5], o_lCB.pull());
	BYTES_EQUAL(array[6], o_lCB.pull());
	BYTES_EQUAL(array[7], o_lCB.pull());
	BYTES_EQUAL(array[8], o_lCB.pull());
	BYTES_EQUAL(array[9], o_lCB.pull());



	mock().checkExpectations();
}
