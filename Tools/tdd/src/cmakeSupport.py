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


def getSuffixNameAlwaysCpp(str_header):
    return 'cpp'

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

class CCMakeGenerator():
    def __init__(self, fName, str_tType, mCfg = CMainConfig(), tCfg = CTestConfig()):
        '''
        Constructor fill variables with default value or user defined.
        '''
        self.cmFile = None
        self.fileName = fName
        self.str_tType = str_tType
        self.mainCfg = mCfg
        self.testCfg = tCfg

    def generate(self):
        """This function generate CMakelists file."""

        self.openFile()
            # start of CMakeLists is version of CMakeLists. We have to confirm but
            # i expect we can use very old version
        self.writeToCMakefileMinimalRequiredVersion(3.00)

            # Add switches to generate gcov files
        self.writeToCMakefileCoverageSection()


            # next include macro header is code injection in to production code. Overriding malloc and operator new.
        self.writeToCMakefileUsageOfMemLeakDetectionMacros()
            # memLeakDetectionInclude = getPathToMemoryLeakDetectionMacros(testCfg)
            # cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorNewMacros.h")))
            # cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h")))
            # cmFile.write("SET(CMAKE_C_FLAGS  \"${CMAKE_C_FLAGS} -include %s\")\n\n" % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h")))

            # this generate root folder of test compilation, all files for
            # compilation have to placed here.
        tmpTestSrcFldr = self.getSrcTestTempFolderName()
            # add executable
        self.writeToCMakefileAddExecutableSection(tmpTestSrcFldr)

            # add include directories
        self.writeToCMakefileAddIncludeDirs(tmpTestSrcFldr)


            ##
        self.writeToCMakefileAddFindLinkTestLibrary()

        self.closeFile()

    def openFile(self):
        self.cmFile = open(self.fileName, 'w')

    def closeFile(self):
        self.cmFile.close()

    def writeToFile(self,strText):
        self.cmFile.write(strText)


    def writeToCMakefileMinimalRequiredVersion(self,fNumber):
        self.writeToFile("cmake_minimum_required(VERSION %.2f)\n\n" % (fNumber))

    def writeToCMakefileCoverageSection(self):
        if self.testCfg.co_coverage.isTurnedOn:
            self.writeToFile(
                'SET(GCC_COVERAGE_COMPILE_FLAGS "-g -O0 -coverage'
                ' -fprofile-arcs -ftest-coverage")\n'
            )
            self.writeToFile(
                'SET(GCC_COVERAGE_LINK_FLAGS    "-coverage -lgcov")' "\n")
            self.writeToFile(
                'SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS}'
                " ${GCC_COVERAGE_COMPILE_FLAGS} -std=c++11 -Wall -Werror"
                ' -pedantic")\n'
            )
            self.writeToFile(
                'SET( CMAKE_C_FLAGS  "${CMAKE_C_FLAGS}'
                ' ${GCC_COVERAGE_COMPILE_FLAGS} -Wall -Werror -pedantic")\n'
            )
            self.writeToFile('SET(CMAKE_CXX_OUTPUT_EXTENSION_REPLACE ON)\n')
            self.writeToFile('SET(CMAKE_C_OUTPUT_EXTENSION_REPLACE ON)\n')

            self.writeToFile(
                "SET( CMAKE_EXE_LINKER_FLAGS  "
                '"${CMAKE_EXE_LINKER_FLAGS} '
                '${GCC_COVERAGE_LINK_FLAGS}" )\n'
            )

    def writeToCMakefileUsageOfMemLeakDetectionMacros(self):
        memLeakDetectionInclude = self.getPathToMemoryLeakDetectionMacros()
        if 'cpputest' == self.testCfg.co_testToolchain.str_testlib:
            self.writeToFile('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%s' % str((memLeakDetectionInclude / "MemoryLeakDetectorNewMacros.h").as_posix())))
            self.writeToFile('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%s' % str((memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h").as_posix())))
            self.writeToFile("SET(CMAKE_C_FLAGS  \"${CMAKE_C_FLAGS} -include %s\")\n\n" % ('%s' % str((memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h").as_posix())))
        else:
            assertUnexpectedBehavior('Wrong testlib %s' % (testCfg.co_testToolchain.str_testlib))

    def writeToCMakefileAddExecutableSection(self,tmpTestSrcFldr):
        # # open add_executable
        self.writeToCMakefileAddExecutableStart()

        # # add all files from SUT except headers
        self.writeToCMakefileAddExecutableSutFiles(tmpTestSrcFldr)

        # # add all source files in OTHER sections
        self.writeToCMakefileAddExecutableOtherFiles(tmpTestSrcFldr)

        # # add all source files in Automock sections
        self.writeToCMakefileAddExecutableAutomockFiles(tmpTestSrcFldr)

        # # add all source files in Automock forced cpp sections
        self.writeToCMakefileAddExecutableAutomockCppFiles(tmpTestSrcFldr)


        # add file with test description
        self.writeToCMakefileAddExecutableCoreTestFiles(tmpTestSrcFldr)

        #close section for adding executables
        self.writeToCMakefileAddExecutableEnd()


    def getSrcTestTempFolderName(self):
        """Function create string for temporary test folder."""
        toolchain_str = self.testCfg.co_testToolchain.str_compiler
        suff = self.mainCfg.co_pkg.str_srctmp_suffix
        return toolchain_str + suff + "_" + self.str_tType

    def writeToCMakefileAddIncludeDirs(self, tmpTestSrcFldr):
        self.writeToCMakefileAddIncludeDirsStart()

        # # add source folder
        self.writeToCMakefileAddIncludeDirsImportantFolders(tmpTestSrcFldr)


        self.writeToCMakefileAddIncludeDirsEnd()

    def writeToCMakefileAddFindLinkTestLibrary(self):
        str_compilerName = self.testCfg.co_testToolchain.str_compiler
        pathToTestLibs = Path('${TDD_FRAMEWORK_ROOT_DIR}') / "Tools" / "testlibs" / \
            self.testCfg.co_testToolchain.str_testlib / str_compilerName

        strPathToTestLibs = '%s' % str(pathToTestLibs.as_posix())
        self.writeToFile( 'find_library(TestLib    libCppUTest %s)\n' % (strPathToTestLibs)
        )
        self.writeToFile(
            'find_library(TestLibExt libCppUTestExt %s)\n\n' % (strPathToTestLibs)
        )

        # add target link library
        self.writeToFile("target_link_libraries(TestApp ${TestLib} ${TestLibExt})\n")

    def writeToCMakefileAddExecutableStart(self):
        self.writeToFile("add_executable(TestApp\n")


    def writeToCMakefileAddExecutableSutFiles(self, tmpTestSrcFldr):
        sut = self.testCfg.SUT_dict
        self.writeAndProcessListDict(tmpTestSrcFldr,sut)


    def writeAndProcessListDict(self,tmpTestSrcFldr, dict):
        sep = self.mainCfg.separ
        for key in dict:

            pathFileSrc = Path(key)
            fileNameSrc = pathFileSrc.name
            suffixSrc = pathFileSrc.suffix.replace('.','')
            # exlude header files
            if (suffixSrc in self.mainCfg.hsuffix):
                continue

            fileNameDst = fileNameSrc
            pathFileDst = Path(dict[key])
            pathFileDstParts = [part for part in pathFileDst.parts if part]

            pathFile = Path("${CMAKE_SOURCE_DIR}")

            if pathFileDstParts == ['SRC_TEMP']:
                pathFile = pathFile / tmpTestSrcFldr / fileNameDst
            else:
                pathFile = pathFile / dict[key].replace("SRC_TEMP", tmpTestSrcFldr)

            strPathFile = '%s' % str(pathFile.as_posix())
            self.writeToFile("\t" + strPathFile + "\n")


        pass
    def writeToCMakefileAddExecutableOtherFiles(self, tmpTestSrcFldr):
        other = self.testCfg.OTHER_dict
        self.writeAndProcessListDict(tmpTestSrcFldr,other)

    def writeToCMakefileAddExecutableAutomockFiles(self, tmpTestSrcFldr):
        Dict = self.testCfg.AUTOMOCK_dict
        # self.processAutomockDictionary(Dict, tmpTestSrcFldr, getSuffixName)
        self.processAutomockDictionary(Dict, tmpTestSrcFldr)


    def writeToCMakefileAddExecutableAutomockCppFiles(self, tmpTestSrcFldr):
        Dict = self.testCfg.AUTOMOCKCPP_dict
        self.processAutomockDictionary(Dict, tmpTestSrcFldr)


    def processAutomockDictionary(self, Dict, tmpTestSrcFldr, getSuffixNameFnc = getSuffixNameAlwaysCpp):
        for key in Dict:
            pathFileSrc = Path(key)
            fileNameSrc = pathFileSrc.name
            suffixSrc = pathFileSrc.suffix.replace('.','')

            # exclude all files which are not header
            if not (suffixSrc in self.mainCfg.hsuffix):
                continue

            fileNameDst = fileNameSrc.replace(pathFileSrc.suffix,'') + '_MOCK.' + getSuffixNameFnc(suffixSrc)
            pathFileDst = Path(Dict[key])
            pathFileDstParts = [part for part in pathFileDst.parts if part]

            pathFile = Path("${CMAKE_SOURCE_DIR}")

            if pathFileDstParts == ['SRC_TEMP']:
                pathFile = pathFile / tmpTestSrcFldr / fileNameDst
            else:
                pathFile = pathFile / Dict[key].replace("SRC_TEMP", tmpTestSrcFldr)

            strPathFile = '%s' % str(pathFile.as_posix())
            self.writeToFile("\t" + strPathFile + "\n")

    def writeToCMakefileAddExecutableCoreTestFiles(self, tmpTestSrcFldr):
        # add file with test description
        sep = self.mainCfg.separ
        # this files are dependent of test library/framework
        if 'cpputest' == self.testCfg.co_testToolchain.str_testlib:
            pathFile = Path("${CMAKE_SOURCE_DIR}") / tmpTestSrcFldr / 'test.cpp'
            strPathFile = '%s' % str(pathFile.as_posix())
            self.writeToFile(
                "\t"
                + strPathFile
                + "\n"
                )

            pathFile = Path("${CMAKE_SOURCE_DIR}") / tmpTestSrcFldr / 'AllTests.cpp'
            strPathFile = '%s' % str(pathFile.as_posix())
            self.writeToFile(
                "\t"
                + strPathFile
                + "\n"
                )
        else:
            assertUnexpectedBehavior('Wrong testlib %s' % (self.testCfg.co_testToolchain.str_testlib))

    def writeToCMakefileAddExecutableEnd(self):
        self.writeToFile("\t)\n\n")

    def getPathToRootOfIncludeForTestLib(self):

        #TODO this is incorrect can cause crash, because test folder could be in different position
        #TODO should looks like relative from ${CMAKE_SOURCE_DIR} to root of TDD_framework and to include folder
        return  Path('${TDD_FRAMEWORK_ROOT_DIR}')/ "Tools" / "testlibs" / \
            self.testCfg.co_testToolchain.str_testlib / "include"

    def getPathToMemoryLeakDetectionMacros(self):
        pIncludeDir = self.getPathToRootOfIncludeForTestLib()
        return pIncludeDir / 'CppUTest'


    def writeToCMakefileAddIncludeDirsStart(self):
        self.writeToFile("include_directories(" + "\n")

    def writeToCMakefileAddIncludeDirsEnd(self):
        self.writeToFile("\t)\n\n")


    def writeToCMakefileAddIncludeDirsImportantFolders(self, tmpTestSrcFldr):
        pathFile = Path("${CMAKE_SOURCE_DIR}") / tmpTestSrcFldr
        strPathFile = '%s' % str(pathFile.as_posix())
        self.writeToFile(
            "\t"
            + strPathFile
            + "\n"
            )

        pIncludeDir = self.getPathToRootOfIncludeForTestLib()
        strVl = '%s' % str(pIncludeDir.as_posix())
        self.writeToFile("\t" + strVl + "\n")


def getSuffixName(str_header):
    if str_header in ['h','H']:
        return 'c'
    else:
        return 'cpp'
