#include "Pencil.hpp"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

using ::CPencil;
using ::CPaperInterface;

class CPaperStub : public CPaperInterface
{
	public :	
	  CPaperStub(){};
	  ~CPaperStub(){};

	  void replacePaper(void)
	  {
		   mock().actualCall("CPaperStub.replacePaper").onObject(this);
	  };
				
	  void writeCharacter(char c_pCharacter)
	  {
		  mock().actualCall("CPaperStub.writeCharacter").withParameter("c_pCharacter", c_pCharacter).onObject(this);
	  };
		
	  int getLastIndexOfCharacter(char c_pCharacter)
	  {
		  mock().actualCall("CPaperStub.getLastIndexOfCharacter").withParameter("c_pCharacter", c_pCharacter).onObject(this); 
		  
		  return mock().intReturnValue();
	  };
		
	  void eraseCharacterOnIndex(int i_pIndex)
	  {
		  mock().actualCall("CPaperStub.eraseCharacterOnIndex").withParameter("i_pIndex", i_pIndex).onObject(this);
	  };
		
	  void getCountOfCharacter(char &rc_pCharacter, int &ri_pCount)
	  {
		  mock().actualCall("CPaperStub.getCountOfCharacter").withParameter("rc_pCharacter", rc_pCharacter).withOutputParameter("ri_pCount", &ri_pCount).onObject(this);
	  };
};



TEST_GROUP(CPencil)
{
  void setup()
  {
  }
  void teardown()
  {
	mock().clear();
  }
};


IGNORE_TEST(CPencil, TemplateIgnoredTestWithHelp)
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


TEST(CPencil, TestEraseAll)
{
	CPaperStub o_lPaper1;
	CPaperStub o_lPaper2;
	
	// SUT
	CPencil o_lPencil(o_lPaper1, o_lPaper2);
		
	// EXPECTATIONS
	mock().expectOneCall("CPaperStub.replacePaper").onObject(&o_lPaper1);
	
	// Call interface
	o_lPencil.eraseAll();
	
	// CHECK
	mock().checkExpectations();
}


TEST(CPencil, TestSetPaper)
{
	CPaperStub o_lPaper1;
	CPaperStub o_lPaper2;
	
	// SUT
	CPencil o_lPencil(o_lPaper1, o_lPaper2);
		
	// EXPECTATIONS
	mock().expectOneCall("CPaperStub.replacePaper").onObject(&o_lPaper1);
	
	// Call interface
	o_lPencil.eraseAll();
	
	// CHECK
	mock().checkExpectations();
	
	// EXPECTATIONS
	mock().expectOneCall("CPaperStub.replacePaper").onObject(&o_lPaper2);
	
	// Call interface
	o_lPencil.setPaper(2);
	o_lPencil.eraseAll();
	
	// CHECK
	mock().checkExpectations();
	
	// EXPECTATIONS
	mock().expectOneCall("CPaperStub.replacePaper").onObject(&o_lPaper1);
	
	// Call interface
	o_lPencil.setPaper(1);
	o_lPencil.eraseAll();
	
	// CHECK
	mock().checkExpectations();
}


TEST(CPencil, TestWriteString)
{
	CPaperStub o_lPaper1;
	CPaperStub o_lPaper2;
	
	// SUT
	CPencil o_lPencil(o_lPaper1, o_lPaper2);
	
	// EXPECTATIONS
	mock().expectOneCall("CPaperStub.writeCharacter").onObject(&o_lPaper1).withParameter("c_pCharacter", 'A');
	mock().expectOneCall("CPaperStub.writeCharacter").onObject(&o_lPaper1).withParameter("c_pCharacter", 'B');
	
	// Call interface
	char c_lString[] = "AB";
	o_lPencil.writeString(c_lString, 2);
	
	// CHECK
	mock().checkExpectations();
}


TEST(CPencil, TestEraseLastSpecificCharacter)
{
	CPaperStub o_lPaper1;
	CPaperStub o_lPaper2;
	
	bool b_lSuccess = false;
	
	// SUT
	CPencil o_lPencil(o_lPaper1, o_lPaper2);
	
	// EXPECTATIONS
	mock().expectOneCall("CPaperStub.getLastIndexOfCharacter").onObject(&o_lPaper1)
	      .withParameter("c_pCharacter", 'A').andReturnValue(1);
	mock().expectOneCall("CPaperStub.eraseCharacterOnIndex").onObject(&o_lPaper1).withParameter("i_pIndex", 1);
	
	// Call interface
	b_lSuccess = o_lPencil.eraseLastSpecificCharacter('A');
	
	CHECK_EQUAL(true, b_lSuccess);
	
	// CHECK
	mock().checkExpectations();
}


TEST(CPencil, TestEraseLastSpecificCharacterError)
{
	CPaperStub o_lPaper1;
	CPaperStub o_lPaper2;
	
	bool b_lSuccess = false;
	
	// SUT
	CPencil o_lPencil(o_lPaper1, o_lPaper2);
	
	// EXPECTATIONS
	mock().expectOneCall("CPaperStub.getLastIndexOfCharacter").onObject(&o_lPaper1)
	      .withParameter("c_pCharacter", 'A').andReturnValue(-1);
	
	// Call interface
	b_lSuccess = o_lPencil.eraseLastSpecificCharacter('A');
	
	CHECK_EQUAL(false, b_lSuccess);
	
	// CHECK
	mock().checkExpectations();
}



TEST(CPencil, TestEraseAllSameCharacters)
{
	CPaperStub o_lPaper1;
	CPaperStub o_lPaper2;
		
	// SUT
	CPencil o_lPencil(o_lPaper1, o_lPaper2);
			
	// EXPECTATIONS
	int i_lCount = 2;
	mock().expectOneCall("CPaperStub.getCountOfCharacter").onObject(&o_lPaper1)
	      .withParameter("rc_pCharacter", 'A').withOutputParameterReturning("ri_pCount", &i_lCount, sizeof(int));
		  
	mock().expectOneCall("CPaperStub.getLastIndexOfCharacter").onObject(&o_lPaper1).withParameter("c_pCharacter", 'A').andReturnValue(1);
	mock().expectOneCall("CPaperStub.eraseCharacterOnIndex").onObject(&o_lPaper1).withParameter("i_pIndex", 1);

    mock().expectOneCall("CPaperStub.getLastIndexOfCharacter").onObject(&o_lPaper1).withParameter("c_pCharacter", 'A').andReturnValue(2);
	mock().expectOneCall("CPaperStub.eraseCharacterOnIndex").onObject(&o_lPaper1).withParameter("i_pIndex", 2);	
	
	// Call interface
	o_lPencil.eraseAllSameCharacters('A');
	
	// CHECK
	mock().checkExpectations();
}


