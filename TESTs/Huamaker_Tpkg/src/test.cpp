extern "C"
{
#include "Huamaker.h"
}
// Mocks
#include "Printer.h"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness.h"
#include "CppUTestExt/MockSupport.h"

TEST_GROUP(Huamaker)
{
  void setup()
  {
    mock().checkExpectations();
  }
  void teardown()
  {
    mock().checkExpectations();
    mock().clear();
  }
};

TEST(Huamaker, Write0Time)
{
  mock().expectOneCall("print_out").withStringParameter("cs_pText", "!!!");
  makeHua(0);

  mock().checkExpectations();
}

TEST(Huamaker, WriteNTime)
{
  int N = 4;
  mock().expectNCalls(N,"print_out").withStringParameter("cs_pText", "hua ");
  mock().expectOneCall("print_out").withStringParameter("cs_pText", "!!!");
  makeHua(N);

  mock().checkExpectations();
}
