#include "Huamaker.h"

// Mocks
#include "Printer.h"

//CppUTest includes should be after your and system includes
#include "CppUTest/TestHarness_c.h"
#include "CppUTestExt/MockSupport_c.h"

TEST_GROUP(CHuamaker)
{
  void setup()
  {
    mock_c().checkExpectations();
  }
  void teardown()
  {
    mock_c().checkExpectations();
    mock_c().clear();
  }
};

TEST(CHuamaker, Write0Time)
{
  mock_c().expectOneCall("print_out").withStringParameter("cs_pText", "!!!");
  makeHua(0);

  mock_c().checkExpectations();
}

TEST(CHuamaker, WriteNTime)
{
  int N = 4;
  mock_c().expectNCalls(N,"print_out").withStringParameter("cs_pText", "hua ");
  mock_c().expectOneCall("print_out").withStringParameter("cs_pText", "!!!");
  makeHua(N);

  mock_c().checkExpectations();
}
