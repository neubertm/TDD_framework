###############################################################################
# Copyright (c) 2021, Milan Neubert (milan.neuber@gmail.com)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

from TDDConfig import CTestConfig
from TDDConfig import CMainConfig


import os
from pathlib import Path

def assertUnexpectedBehavior(text):
    assertWithText(False, text)

def assertWithText(condition, text):
    assert condition, text

def getGeneratorName(tcfg: CTestConfig):
    dict = {'gcc': "Unix Makefiles",
            'mingw': "MinGW Makefiles",
            'msvc_9': "Visual Studio 9 2008",
            'msvc_10': "Visual Studio 10 2010",
            'msvc_11': "Visual Studio 11 2012",
            'msvc_12': "Visual Studio 12 2013",
            'msvc_14': "Visual Studio 14 2015",
            'msvc_15': "Visual Studio 15 2017",
            'msvc_16': "Visual Studio 16 2019"}
    return(dict[tcfg.co_testToolchain.str_compiler])


def getMaketoolName(tcfg: CTestConfig):
    dict = {'gcc': "make",
            'mingw': "mingw32-make",
            'msvc_9':  "nmake",
            'msvc_10': "nmake",
            'msvc_11': "nmake",
            'msvc_12': "nmake",
            'msvc_14': "nmake",
            'msvc_15': "nmake",
            'msvc_16': "nmake"}
    return(dict[tcfg.co_testToolchain.str_compiler])


def getTestBinaryName():
    # for windows
    if os.name == "nt":
        return("TestApp.exe")

    # for other normal system
    return("TestApp")


def createCMakeListsFromConfiguration(fileName: str, mainCfg: CMainConfig(), testCfg: CTestConfig, str_tType: str):
    """This function generate CMakelists file."""
    with open(fileName, "w") as cmFile:
        # start of CMakeLists is version of CMakeLists. We have to confirm but
        # i expect we can use very old version
        writeToCMakefileMinimalRequiredVersion(cmFile, 3.00)

        # Add switches to generate gcov files
        writeToCMakefileCoverageSection(cmFile,testCfg)


        # next include macro header is code injection in to production code. Overriding malloc and operator new.
        writeToCMakefileUsageOfMemLeakDetectionMacros(cmFile, testCfg)
        # memLeakDetectionInclude = getPathToMemoryLeakDetectionMacros(testCfg)
        # cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorNewMacros.h")))
        # cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h")))
        # cmFile.write("SET(CMAKE_C_FLAGS  \"${CMAKE_C_FLAGS} -include %s\")\n\n" % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h")))

        # this generate root folder of test compilation, all files for
        # compilation have to placed here.
        tmpTestSrcFldr = getSrcTestTempFolderName(
            testCfg, mainCfg, str_tType)
        # add executable
        writeToCMakefileAddExecutableSection(cmFile, testCfg, mainCfg, tmpTestSrcFldr)

        # add include directories
        writeToCMakefileAddIncludeDirs(cmFile, testCfg, tmpTestSrcFldr)


        ##
        writeToCMakefileAddFindLinkTestLibrary(cmFile, testCfg)




def writeToCMakefileMinimalRequiredVersion(openedFileW, fNumber):
    openedFileW.write("cmake_minimum_required(VERSION %.2f)\n\n" % (fNumber))

def writeToCMakefileCoverageSection(cmFile, testCfg: CTestConfig):
    if testCfg.co_coverage.isTurnedOn:
        cmFile.write(
            'SET(GCC_COVERAGE_COMPILE_FLAGS "-g -O0 -coverage'
            ' -fprofile-arcs -ftest-coverage")\n'
        )
        cmFile.write(
            'SET(GCC_COVERAGE_LINK_FLAGS    "-coverage -lgcov")' "\n")
        cmFile.write(
            'SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS}'
            " ${GCC_COVERAGE_COMPILE_FLAGS} -std=c++11 -Wall -Werror"
            ' -pedantic")\n'
        )
        cmFile.write(
            'SET( CMAKE_C_FLAGS  "${CMAKE_C_FLAGS}'
            ' ${GCC_COVERAGE_COMPILE_FLAGS} -Wall -Werror -pedantic")\n'
        )
        cmFile.write('SET(CMAKE_CXX_OUTPUT_EXTENSION_REPLACE ON)\n')
        cmFile.write('SET(CMAKE_C_OUTPUT_EXTENSION_REPLACE ON)\n')

        cmFile.write(
            "SET( CMAKE_EXE_LINKER_FLAGS  "
            '"${CMAKE_EXE_LINKER_FLAGS} '
            '${GCC_COVERAGE_LINK_FLAGS}" )\n'
        )

def getSrcTestTempFolderName(testCfg: CTestConfig, mainCfg: CMainConfig, str_tType: str):
    """Function create string for temporary test folder."""
    toolchain_str = testCfg.co_testToolchain.str_compiler
    suff = mainCfg.co_pkg.str_srctmp_suffix
    return toolchain_str + suff + "_" + str_tType

def getPathToRootOfIncludeForTestLib(testCfg: CTestConfig):

    #TODO this is incorrect can cause crash, because test folder could be in different position
    #TODO should looks like relative from ${CMAKE_SOURCE_DIR} to root of TDD_framework and to include folder
    return  Path('${TDD_FRAMEWORK_ROOT_DIR}')/ "Tools" / "testlibs" / \
        testCfg.co_testToolchain.str_testlib / "include"

def getPathToMemoryLeakDetectionMacros(testCfg: CTestConfig):
    pIncludeDir = getPathToRootOfIncludeForTestLib(testCfg)
    return pIncludeDir / 'CppUTest'

def writeToCMakefileUsageOfMemLeakDetectionMacros(cmFile, testCfg):
    memLeakDetectionInclude = getPathToMemoryLeakDetectionMacros(testCfg)
    if 'cpputest' == testCfg.co_testToolchain.str_testlib:
        cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%s' % str((memLeakDetectionInclude / "MemoryLeakDetectorNewMacros.h").as_posix())))
        cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%s' % str((memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h").as_posix())))
        cmFile.write("SET(CMAKE_C_FLAGS  \"${CMAKE_C_FLAGS} -include %s\")\n\n" % ('%s' % str((memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h").as_posix())))
    else:
        assertUnexpectedBehavior('Wrong testlib %s' % (testCfg.co_testToolchain.str_testlib))

def writeToCMakefileAddExecutableStart(cmFile):
    cmFile.write("add_executable(TestApp\n")

def writeToCMakefileAddExecutableSutFiles(cmFile, testCfg, mainCfg, tmpTestSrcFldr):
    sut = testCfg.SUT_dict
    sep = mainCfg.separ
    # for all SUT file
    for key in sut:
        # exclude header files
        if not (key.split(sep)[-1].split(".")[-1] in mainCfg.hsuffix):
            if sut[key].split(sep)[-1]:
                # this is work if we define path only
                pathFile = Path("${CMAKE_SOURCE_DIR}") / sut[key].replace("SRC_TEMP", tmpTestSrcFldr) / key.split(sep)[-1]
                strPathFile = '%s' % str(pathFile.as_posix())
                cmFile.write(
                    "\t"
                    + strPathFile
                    + "\n"
                    )
            else:
                # this is used when is used path with name
                pathFile = Path("${CMAKE_SOURCE_DIR}") / sut[key].replace("SRC_TEMP", tmpTestSrcFldr)
                strPathFile = '%s' % str(pathFile.as_posix())
                cmFile.write(
                    "\t"
                    + strPathFile
                    + "\n"
                    )


def writeToCMakefileAddExecutableOtherFiles(cmFile, testCfg, mainCfg, tmpTestSrcFldr):
    other = testCfg.OTHER_dict
    sep = mainCfg.separ
    # print(other)
    for key in other:
        # check if it is header file
        if not (key.split(sep)[-1].split(".")[-1] in mainCfg.hsuffix):
            # check if use specify position of file in test environment
            if "SRC_TEMP" in other[key]:
                pathFile = Path("${CMAKE_SOURCE_DIR}") / other[key].replace("SRC_TEMP", tmpTestSrcFldr) / key.split(sep)[-1]
                strPathFile = '%s' % str(pathFile.as_posix())
                cmFile.write(
                    "\t"
                    + strPathFile
                    + "\n"
                    )
            else:
                # non default -> store in default src folder
                if other[key].split(sep)[-1]:
                    pathFile = Path("${CMAKE_SOURCE_DIR}") / other[key].replace("SRC_TEMP", tmpTestSrcFldr)
                    strPathFile = '%s' % str(pathFile.as_posix())
                    cmFile.write(
                        "\t"
                        + strPathFile
                        + "\n"
                        )


def writeToCMakefileAddExecutableEnd(cmFile):
    cmFile.write("\t)\n\n")


def writeToCMakefileAddExecutableCoreTestFiles(cmFile, testCfg, mainCfg, tmpTestSrcFldr):
    # add file with test description
    sep = mainCfg.separ
    # this files are dependent of test library/framework
    if 'cpputest' == testCfg.co_testToolchain.str_testlib:
        pathFile = Path("${CMAKE_SOURCE_DIR}") / tmpTestSrcFldr / 'test.cpp'
        strPathFile = '%s' % str(pathFile.as_posix())
        cmFile.write(
            "\t"
            + strPathFile
            + "\n"
            )

        pathFile = Path("${CMAKE_SOURCE_DIR}") / tmpTestSrcFldr / 'AllTests.cpp'
        strPathFile = '%s' % str(pathFile.as_posix())
        cmFile.write(
            "\t"
            + strPathFile
            + "\n"
            )
    else:
        assertUnexpectedBehavior('Wrong testlib %s' % (testCfg.co_testToolchain.str_testlib))

def writeToCMakefileAddExecutableSection(cmFile, testCfg, mainCfg, tmpTestSrcFldr):
    # # open add_executable
    writeToCMakefileAddExecutableStart(cmFile)

    # # add all files from SUT except headers
    writeToCMakefileAddExecutableSutFiles(cmFile, testCfg, mainCfg, tmpTestSrcFldr)

    # # add all source files in OTHER sections
    writeToCMakefileAddExecutableOtherFiles(cmFile, testCfg, mainCfg, tmpTestSrcFldr)

    # add file with test description
    writeToCMakefileAddExecutableCoreTestFiles(cmFile, testCfg, mainCfg, tmpTestSrcFldr)

    #close section for adding executables
    writeToCMakefileAddExecutableEnd(cmFile)

def writeToCMakefileAddIncludeDirsStart(cmFile):
    cmFile.write("include_directories(" + "\n")

def writeToCMakefileAddIncludeDirsEnd(cmFile):
    cmFile.write("\t)\n\n")


def writeToCMakefileAddIncludeDirsImportantFolders(cmFile, testCfg: CTestConfig, tmpTestSrcFldr):
    pathFile = Path("${CMAKE_SOURCE_DIR}") / tmpTestSrcFldr
    strPathFile = '%s' % str(pathFile.as_posix())
    cmFile.write(
        "\t"
        + strPathFile
        + "\n"
        )

    pIncludeDir = getPathToRootOfIncludeForTestLib(testCfg)
    strVl = '%s' % str(pIncludeDir.as_posix())
    cmFile.write("\t" + strVl + "\n")



def writeToCMakefileAddIncludeDirs(cmFile, testCfg, tmpTestSrcFldr):
    writeToCMakefileAddIncludeDirsStart(cmFile)

    # # add source folder
    writeToCMakefileAddIncludeDirsImportantFolders(cmFile, testCfg, tmpTestSrcFldr)


    writeToCMakefileAddIncludeDirsEnd(cmFile)


def writeToCMakefileAddFindLinkTestLibrary(cmFile, testCfg: CTestConfig):
    str_compilerName = testCfg.co_testToolchain.str_compiler
    pathToTestLibs = Path('${TDD_FRAMEWORK_ROOT_DIR}') / "Tools" / "testlibs" / \
        testCfg.co_testToolchain.str_testlib / str_compilerName

    strPathToTestLibs = '%s' % str(pathToTestLibs.as_posix())
    cmFile.write( 'find_library(TestLib    libCppUTest %s)\n' % (strPathToTestLibs)
    )
    cmFile.write(
        'find_library(TestLibExt libCppUTestExt %s)\n\n' % (strPathToTestLibs)
    )

    # add target link library
    cmFile.write("target_link_libraries(TestApp ${TestLib} ${TestLibExt})\n")
