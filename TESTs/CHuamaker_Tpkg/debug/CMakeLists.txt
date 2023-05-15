cmake_minimum_required(VERSION 3.00)

project(UnitTest)

SET(CMAKE_SOURCE_DIR  "../../../project")
SET(TDD_FRAMEWORK_ROOT_DIR  "../../..")
SET(TPKG_DIR  "..")

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_USE_RESPONSE_FILE_FOR_INCLUDES Off)
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -g -include ../src/MemLeakDetectionNewMacros.h")
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -include ${TPKG_DIR}/Stubs/CPrinter.h")
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -include ${CMAKE_SOURCE_DIR}/HuaMaker/CHuamaker.h")
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -include ../src/MemLeakDetectionMallocMacros.h")
SET(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -g -include ../src/MemLeakDetectionMallocMacros.h")

add_executable(TestApp
	${TPKG_DIR}/Stubs/CPrinter.cpp
	${CMAKE_SOURCE_DIR}/HuaMaker/CHuamaker.cpp
	#${CMAKE_SOURCE_DIR}/HuaMaker/CHuamaker.h
	#${TPKG_DIR}/Stubs/CPrinter.h
	${TPKG_DIR}/src/test.cpp
	${TPKG_DIR}/src/AllTests.cpp
	)

include_directories(
	#${TPKG_DIR}/Stubs
	#${CMAKE_SOURCE_DIR}/HuaMaker
	${TDD_FRAMEWORK_ROOT_DIR}/Tools/testlibs/cpputest/include
	)

find_library(TestLib    libCppUTest ${TDD_FRAMEWORK_ROOT_DIR}/Tools/testlibs/cpputest/mingw)
find_library(TestLibExt libCppUTestExt ${TDD_FRAMEWORK_ROOT_DIR}/Tools/testlibs/cpputest/mingw)

target_link_libraries(TestApp ${TestLib} ${TestLibExt})
