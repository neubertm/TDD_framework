#include "CHuamaker.h"

// Mocks
#include "CPrinter.h"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"
#include "CppUTest/MemoryLeakDetectorNewMacros.h"

TEST_GROUP(CHuamaker)
{
  CHuamaker *cHuamaker;
  CPrinter *Printer;

  void setup()
  {
    cHuamaker = new CHuamaker();
	Printer =  new CPrinter();
	
  }
  void teardown()
  {
    delete cHuamaker;
	delete Printer;
	
	mock().clear();
  }
};

/*
TEST(CHuamaker, Create)
{
  FAIL("Nemohu testovat hodnotu je private.");
}
*/
TEST(CHuamaker, PrinterNotSet)
{
  cHuamaker->makeHua(4);

  STRCMP_EQUAL("\0",Printer->getOutput());
}

TEST(CHuamaker, Write4Time)
{

  cHuamaker->setPrinter( Printer );
  
  cHuamaker->makeHua(4);
  
  STRCMP_EQUAL("hua hua hua hua !!!",Printer->getOutput());
}

TEST(CHuamaker, Write0Time)
{
  cHuamaker->setPrinter( Printer );
  
  cHuamaker->makeHua(0);
  
  STRCMP_EQUAL("!!!",Printer->getOutput());
}

