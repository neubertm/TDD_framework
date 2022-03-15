//Here you can include some file from stdlib and this will be excluded from memory leak detection
//But when you do not it becomes uncompilable. Reason is obvios stdlib is in many files templated and full of macros.
// And CppUTest/MemoryLeakDetectorMallocMacros.h try to override macro and not operator.

// What is included here will be excluded from memory leak detection

//example is here
//#include <vector>


//This include is the last one.
#include "CppUTest/MemoryLeakDetectorMallocMacros.h"
