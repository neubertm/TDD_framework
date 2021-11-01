#include "CircBuff.hpp"
#include <cstdint>

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

class CBuff10: public CircBuff<uint8_t, 10>
{
public:
  CBuff10(){}
  ~CBuff10(){}
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

TEST(CircBuff, CircBuffer_can_be_derived)
{
  CBuff10 o_cb;
}

TEST(CircBuff, CircBuffer_can_be_created_statically)
{
	CircBuff<uint8_t, 10> o_lCB;

	mock().checkExpectations();
}

TEST(CircBuff, CircBuffer_can_be_created_dynamically)
{
	CircBuff<uint8_t, 10>* po_lCB = new CircBuff<uint8_t, 10>();
	delete po_lCB;

	mock().checkExpectations();
}


TEST(CircBuff, CircBuffer_is_empty_after_initialization)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, Successfully_pushed_byte_returns_true)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_TRUE(o_lCB.push(44));

	mock().checkExpectations();
}

TEST(CircBuff, CircBuffer_is_not_empty_after_first_push)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_TRUE(o_lCB.push(44));

	CHECK_TRUE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, Pushed_one_byte_can_be_pulled_again)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_TRUE(o_lCB.push(44));

	uint8_t u8 = o_lCB.pull();
	
	CHECK_EQUAL(44, u8);

	mock().checkExpectations();
}

TEST(CircBuff, after_pulling_the_last_byte_CircBuffer_is_empty_again)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_TRUE(o_lCB.push(44));

	o_lCB.pull();

	CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, CircBuffer_accepts_array)
{
	CircBuff<uint8_t, 10> o_lCB;

	uint8_t array[10] = {1,2,3,4,5,6,7,8,9,10};
	o_lCB.push(array, 1);

	CHECK_TRUE(o_lCB.isNonEmpty());

	uint8_t u8 = o_lCB.pull();
	CHECK_EQUAL(u8,array[0]);

	CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, CircBuffer_rejects_bytes_when_full_without_spoiling_stored_data)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

	uint8_t array[10] = {1,2,3,4,5,6,7,8,9,10};
	CHECK_TRUE(o_lCB.push(array, 10));
	
	CHECK_FALSE(o_lCB.push(5));
	CHECK_FALSE(o_lCB.push(array, 1));

	CHECK_TRUE(o_lCB.isNonEmpty());
	
	for(int i = 0; i<10; ++i)
	{
		CHECK_EQUAL(array[i],o_lCB.pull());
	}

	CHECK_FALSE(o_lCB.isNonEmpty());
	
	mock().checkExpectations();
}

TEST(CircBuff, CircBuffer_rejects_arrays_which_dont_fit_to_free_size)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

	uint8_t array[11] = {1,2,3,4,5,6,7,8,9,10,11};
	
	// buffer size is only 10
	CHECK_FALSE(o_lCB.push(array, 11));

	// fill buffer partly
	CHECK_TRUE(o_lCB.push(array, 3));
	
	// free buffer size is only 7
	CHECK_FALSE(o_lCB.push(array, 8));

	// fill the rest of buffer
	CHECK_TRUE(o_lCB.push(array, 7));

	// no space anymore
	CHECK_FALSE(o_lCB.push(array, 1));

	mock().checkExpectations();
}

TEST(CircBuff, buffer_space_can_be_reused)
{
	CircBuff<uint8_t, 10> o_lCB;

	CHECK_FALSE(o_lCB.isNonEmpty());

	uint8_t array[10] = {1,2,3,4,5,6,7,8,9,10};
	
	// fill buffer completely
	CHECK_TRUE(o_lCB.push(array,10));

	// pull 3 bytes
	o_lCB.pull();
	o_lCB.pull();
	o_lCB.pull();
	
	// fill the free space
	CHECK_TRUE(o_lCB.push(array, 3));

	// buffer is full again
	CHECK_FALSE(o_lCB.push(array, 1));
	
	// expected buffer content
	uint8_t expected[10] = {4,5,6,7,8,9,10,1,2,3};
	
	for(int i=0; i<10;++i)
	{
		CHECK_TRUE(o_lCB.isNonEmpty());
		CHECK_EQUAL(expected[i], o_lCB.pull());
	}

	CHECK_FALSE(o_lCB.isNonEmpty());

	mock().checkExpectations();
}

TEST(CircBuff, buffer_space_can_be_reused_multiple_times)
{
	CircBuff<uint8_t, 10> o_lCB;
	
	uint8_t array[10] = {1,2,3,4,5,6,7,8,9,10};
	
	for (int c = 0; c < 100; c++)
	{
		CHECK_FALSE(o_lCB.isNonEmpty());

		CHECK_TRUE(o_lCB.push(array, 3));

		CHECK_TRUE(o_lCB.isNonEmpty());
		
		for(int i = 0; i<3; ++i)
		{
			CHECK_EQUAL(array[i],o_lCB.pull());
		}

		CHECK_FALSE(o_lCB.isNonEmpty());

		CHECK_TRUE(o_lCB.push(array,10));
		CHECK_TRUE(o_lCB.isNonEmpty());

		for(int i = 0; i<10; ++i)
		{
			CHECK_EQUAL(array[i],o_lCB.pull());
		}
	}

	mock().checkExpectations();
}
