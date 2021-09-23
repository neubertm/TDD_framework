#include "Resident.hpp"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

using ::CResident;


TEST_GROUP(CResident)
{
  void setup()
  {
  }
  void teardown()
  {
	mock().clear();
  }
};

IGNORE_TEST(CResident, TemplateIgnoredTestWithHelp)
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

TEST(CResident, TestWashHands)
{
	// SUT
	CResident o_lResident;
	
	// EXPECTATIONS
	mock().expectOneCall("CBathroom.useWashBasin");
	
	//call interface	
	o_lResident.washHands();
	
	mock().checkExpectations();
}

TEST(CResident, TestTakeAShower)
{
	// SUT
	CResident o_lResident;
	
	// EXPECTATIONS
	mock().expectOneCall("CBathroom.useShower");
	
	//call interface	
	o_lResident.takeAShower();
	
	mock().checkExpectations();
}

TEST(CResident, TestBathroomConstructor)
{
	// EXPECTATIONS
	// only one constructor called - singletone
	mock().expectOneCall("CBathroom.CBathroom");
	
	// SUTs
	CResident o_lResident1;
	CResident o_lResident2;
	
	mock().checkExpectations();	
}
