# eTDD

Framework for Test-driven development (TDD) to support to isolate the unit code in C/C++.

# Installing

## Windows

Before to execute the test, you need to execute the option "Install CppUTest on ./tmp" in the tdd.menu(). It will download and compile the cpputest code.

You need to install also:
 - cmake : https://cmake.org/download/
 - cppcheck : http://cppcheck.net/
 - git : https://github.com/git-for-windows/git/releases/tag/v2.41.0.windows.1
 - mingw-gcc : https://github.com/niXman/mingw-builds-binaries/releases
 - doxygen : https://www.doxygen.nl/download.html


## Linux

```
sudo apt install cmake libcpputest-dev cppcheck
sudo apt install doxygen graphviz
```


# Example 1 - simplest example

```
from etdd import TDD

tdd = TDD()
tdd.download_from_git("https://github.com/neubertm/TDD_framework.git")

test = tdd.test("TDD_framework/TESTs/BitInverter_Tpkg/src/test.cpp", "BitInverter")
test.sut = ["TDD_framework/project/BitInverter/BitInverter.c", "TDD_framework/project/BitInverter/BitInverter.h"]
test.compile = ["BitInverter.c"]

tdd.menu()
```


# Example 2 - with environment file

You can create the file tdd.py and execute it with the follow code:

```
from etdd import TDD, full_main

tdd = TDD(main=full_main, envpath="envpath.ini")
tdd.download_from_git("https://github.com/neubertm/TDD_framework.git")

tdd.cmake["CMAKE_C_FLAGS"] = "-g -O0 -coverage -lgcov "
tdd.cmake["CMAKE_CXX_FLAGS"] = "-g -O0 -coverage -lgcov "

# Test 1 - BitInverter
test = tdd.test("TDD_framework/TESTs/BitInverter_Tpkg/src/test.cpp", "BitInverter")
test.sut = ["TDD_framework/project/BitInverter/BitInverter.c", "TDD_framework/project/BitInverter/BitInverter.h"]
test.files = ["TDD_framework/TESTs/BitInverter_Tpkg/src/MemLeakDetection*.h"]
test.compile = ["BitInverter.c"]

# Open the menu in the console
tdd.menu()
```

## envpath.ini
```
[CMAKE]
check=true
ENV_CONFIG_SCRIPT = /usr/bin/

[MINGW]
check=False
ENV_CONFIG_SCRIPT = /usr/bin/

[MSVC]
check=False
ENV_CONFIG_SCRIPT = /usr/bin/

[CLANG]
check=False
ENV_CONFIG_SCRIPT = /usr/bin/

[CPPCHECK]
check=False
ENV_CONFIG_SCRIPT = /usr/bin/

[CPPUMOCKGEN]
ENV_CONFIG_SCRIPT = /usr/bin/
```



# Example 3 - Test Code

## tdd.py

```
from etdd import TDD

tdd = TDD()
tdd.download_from_git("https://github.com/neubertm/TDD_framework.git")

# CHuaMaker Test
test = tdd.test("./test.cpp", "cHuamaker")
test.sut = ["TDD_framework/project/example_4/CHuamaker.cpp", "TDD_framework/project/example_4/CHuamaker.h"]
test.files = ["TDD_framework/project/example_4/CPrinter.h"]
test.compile = ["CHuamaker.cpp"]

tdd.menu()
```


## ./test.cpp

```
#include "CHuamaker.h"
#include "CPrinter.h"

/** @code CPrinter.cpp

#include "CPrinter.h"

void CPrinter::out(const char *cs_pText) {

}

*/

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
  Printer->out("opa");
}
```




