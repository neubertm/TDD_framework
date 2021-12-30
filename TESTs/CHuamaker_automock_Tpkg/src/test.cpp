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
    mock().checkExpectations();
    cHuamaker = new CHuamaker();
    Printer =  new CPrinter();

  }
  void teardown()
  {
    delete cHuamaker;
    delete Printer;

    mock().checkExpectations();
    mock().clear();
  }
};

/*
TEST(CHuamaker, Create)
{
  FAIL("Nemohu testovat hodnotu je private.");
}
*/

//TEST(CHuamaker, PrinterNotSet)
//{
//  cHuamaker->makeHua(4);
//}

TEST(CHuamaker, Write0Time)
{

  cHuamaker->setPrinter( Printer );

  mock().expectOneCall("CPrinter::out").onObject(Printer).withStringParameter("cs_pText", "!!!");
  cHuamaker->makeHua(0);

  //mock().expectNCalls(4,"CPrinter::out").onObject(Printer).withStringParameter("cs_pText", "hua ");

  mock().checkExpectations();
}

TEST(CHuamaker, WriteNTime)
{
  int N = 4;
  cHuamaker->setPrinter( Printer );

  mock().expectNCalls(N,"CPrinter::out").onObject(Printer).withStringParameter("cs_pText", "hua ");
  mock().expectOneCall("CPrinter::out").onObject(Printer).withStringParameter("cs_pText", "!!!");
  cHuamaker->makeHua(N);



  mock().checkExpectations();
}

//TEST(CHuamaker, Write0Time)
//{
//  cHuamaker->setPrinter( Printer );
//
//  cHuamaker->makeHua(0);
//
//  STRCMP_EQUAL("!!!",Printer->getOutput());
//}
