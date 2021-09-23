# TDD_framework
TDD_framework is tool mainly for C++ development but it can be use even for C.

Hello this document describe how set up and enabled this unit test framework.
For initialization of framework you have to be connected to internet. Because
we need additional packages and tools.

## Current situation
What works now is full functionality of framework, but we are limited only for Windows platform and gcc compiler.


Complete list of steps:
1. Manual install of Python3 and pip
2. Manual update of file start.bat and makeItWork.bat. This step is important only when the python3 in not in system path.
3. Run makeItWork.bat
  1. First is install or find tools in the system.
  2. Download and compile library(automated)
  3. Configure init file for test(automated)
4. Run start.bat


## Python installation
Framework is written in Python3. So you have to install Python3 and during
the installation allow to install package install(pip). It will be use for
automatical installation of other packages.
https://www.python.org/downloads/

## CMake installation
Framework should be(in future) multiplatform and compiler independent. That is
why we decide to use CMake for generating makefiles. During setup script user is
asked if CMake is already installed. When you allow that. It tries to download
and install it.
https://github.com/Kitware/CMake/releases/download/v3.20.3/cmake-3.20.3-windows-x86_64.msi

## Compiler installation
### MinGW compiler
Currently framework support only gcc compiler(mingw64). If script doesnt
recognize g++. It ask you if you want to install it or try to find on disk.
Please install posix thread support.
### CLang compiler
Currently use only for formatting, but it contain advance code inspection tool,
static analysis.
https://github.com/llvm/llvm-project/releases/download/llvmorg-12.0.0/LLVM-12.0.0-win64.exe
### MSVC compiler
Under construction

## Static analysis tools
### Cppcheck
Currently we support only cppcheck.
### CLang static check
Under construction
### Other non free and non opensource tools
Under construction

## C++ test framework
### CppUTest
Currently we use only this Framework
### GoogleTest
Is intended to allow this.

## C# testing
C# is impossible to use now.
Ideas about how to allow use this framework as C# TDD framework.
### C# compilator
For platform independency is smart to use mono Compiler, but with MSVC compatible configuration.
https://www.mono-project.com/
### C# test Library
It important to choose which test lib/framework to use. xUnit and NUnit is possible to run under even under *nix system.
Question is about support and automatization of mocking(moq https://softchris.github.io/pages/dotnet-moq.html).
1. xUnit
2. MSTest
3. NUnit

https://www.mono-project.com/community/contributing/test-suite/

### C# & CMake
https://stackoverflow.com/questions/2074144/generate-c-sharp-project-using-cmake/46247927

### C# Sourcetrail
How to use index C#.
https://github.com/CoatiSoftware/Sourcetrail/issues/398
