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

import threading
import readchar
import os
import filecmp
from pathlib import Path
from TDDConfig import CTestConfig
from TDDConfig import CMainConfig


def del_folder(path: Path):
    for sub in path.iterdir():
        if sub.is_dir():
            del_folder(sub)
        else:
            sub.unlink()
    path.rmdir()


def my_callback(inp):
    global readedChar
    #  print("You Entered: ",inp, " Counter is at:", showcounter )
    readedChar = inp
    #  print(readedChar)


def getSrcTestTempFolderName(testCfg: CTestConfig, mainCfg: CMainConfig, str_testType: str):
    """Function create string for temporary test folder."""
    toolchain_str = testCfg.co_testToolchain.str_compiler
    suff = mainCfg.co_pkg.str_srctmp_suffix
    return toolchain_str + suff + "_" + str_testType


def interpretGCOV2lists(gcvOutFileName, pathBuildFolder):
    """Funtion interpret gcov files expect string gcov file name."""
    try:
        with open(gcvOutFileName, "r") as cof:
            cofLines = cof.readlines()
            lst_cov = []
            lst_covFiles = []
            for line in cofLines:
                splitedLine = line.split(" ")

                if splitedLine[0] == "Lines":
                    lst_cov.append(line)

                if splitedLine[0] == "Creating":
                    lst_covFiles.append(splitedLine[1][1:-2])
    except IOError:
        with open("debug.log", "a") as log:
            log.write("IOError when trying to read this file: "
                      + gcvOutFileName + "\n")
            log.write("Current folder is: "
                      + os.getcwd() + "\n")
        return [], {}
    lst_uncovLines = []
    for covf in lst_covFiles:
        covFileName = str(pathBuildFolder / covf)
        cf = open(covFileName, "r")
        cfLines = cf.readlines()
        uncovered_lines = []
        for line in cfLines:
            splitedLine = line.split(":")
            if splitedLine[0].lstrip() == "#####":
                uncovered_lines.append(splitedLine[1].lstrip())
        cf.close()
        lst_uncovLines.append(uncovered_lines.copy())
    dict_covFile = dict(zip(lst_covFiles, lst_uncovLines))

    return lst_cov, dict_covFile


def createSutList(testCfg: CTestConfig, mainCfg: CMainConfig, str_tType):
    """Function creating list of stringFileName for subject under test."""
    sut = testCfg.SUT_dict
    tmpTstFolder = getSrcTestTempFolderName(testCfg, mainCfg, str_tType)
    sutList = []
    for key in sut:
        keyPath = Path(key)
        sutName = keyPath.name
        sutList.append(str(Path("..") / tmpTstFolder / sutName))
    return sutList


def isCppcheckEnabled(testCfg: CTestConfig):
    """Logic function return true or false base on configuration file."""
    return testCfg.co_staticAnalysis.isTurnedOn


def isCoverageEnabled(testCfg: CTestConfig):
    """Logic function return true or false base on configuration file."""
    return testCfg.co_coverage.isTurnedOn


def isCodeStatisticEnabled(testCfg: CTestConfig):
    """Logic function return true or false base on configuration file."""
    return testCfg.co_codeStatistics.isTurnedOn


def getCompilerNameInTestConfig(testCfg: CTestConfig):
    """Function return string with name of compiler
    , input arg is test configuration"""
    return testCfg.co_testToolchain.str_compiler


def createCMakeListsFromConfiguration(fileName: str, mainCfg: CMainConfig(), testCfg: CTestConfig, str_tType: str):
    """This function generate CMakelists file."""
    sep = mainCfg.separ
    with open(fileName, "w") as cmFile:
        # start of CMakeLists is version of CMakeLists. We have to confirm but
        # i expect we can use very old version
        cmFile.write("cmake_minimum_required(VERSION " + "3.00" + ")\n\n")

        # set the project name

        # Add switches to generate gcov files
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

        # next include macro header is code injection in to production code. Overriding malloc and operator new.
        str_frameworkFolderName = "cpputest"
        pIncludeDir = Path.cwd()
        pIncludeDir = pIncludeDir / "Tools" / "testlibs" / \
            str_frameworkFolderName / "include"
        memLeakDetectionInclude = pIncludeDir / 'CppUTest'
        cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorNewMacros.h")))
        cmFile.write('SET(CMAKE_CXX_FLAGS  \"${CMAKE_CXX_FLAGS} -include %s\")\n' % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h")))
        cmFile.write("SET(CMAKE_C_FLAGS  \"${CMAKE_C_FLAGS} -include %s\")\n\n" % ('%r' % str(memLeakDetectionInclude / "MemoryLeakDetectorMallocMacros.h")))

        # add executable
        # # open add_executable
        cmFile.write("add_executable(" + "TestApp" + "\n")

        # this generate root folder of test compilation, all files for
        # compilation have to placed here.
        tmpTestSrcFldr = getSrcTestTempFolderName(
            testCfg, mainCfg, str_tType)

        # # add all files from SUT except headers
        # sut = testCfg["SUT"]
        sut = testCfg.SUT_dict
        # for all SUT file
        for key in sut:
            # exclude header files
            if not (key.split(sep)[-1].split(".")[-1] in mainCfg.hsuffix):
                if sut[key].split(sep)[-1]:
                    # this is work if we define path only
                    cmFile.write(
                        "\t"
                        + "${CMAKE_SOURCE_DIR}"
                        + sep
                        + sut[key].replace("SRC_TEMP", tmpTestSrcFldr)
                        + sep
                        + key.split(sep)[-1]
                        + "\n"
                    )
                else:
                    # this is used when is used path with name
                    cmFile.write(
                        "\t"
                        + "${CMAKE_SOURCE_DIR}"
                        + sep
                        + sut[key].replace("SRC_TEMP", tmpTestSrcFldr)
                        + "\n"
                    )
        # # add all source files in OTHER sections
        other = testCfg.OTHER_dict
        # print(other)
        for key in other:
            # check if it is header file
            if not (key.split(sep)[-1].split(".")[-1] in mainCfg.hsuffix):
                # check if use specify position of file in test environment
                if "SRC_TEMP" in other[key]:
                    # print(key)
                    # print(other[key])
                    cmFile.write(
                        "\t"
                        + "${CMAKE_SOURCE_DIR}"
                        + sep
                        + other[key].replace("SRC_TEMP", tmpTestSrcFldr)
                        + sep
                        + key.split(sep)[-1]
                        + "\n"
                    )
                else:
                    # non default -> store in default src folder
                    if other[key].split(sep)[-1]:
                        cmFile.write(
                            "\t"
                            + "${CMAKE_SOURCE_DIR}"
                            + sep
                            + other[key].replace("SRC_TEMP", tmpTestSrcFldr)
                            + "\n"
                        )
        # # add file with test description
        cmFile.write(
            "\t"
            + "${CMAKE_SOURCE_DIR}"
            + sep
            + tmpTestSrcFldr
            + sep
            + "test.cpp"
            + "\n"
        )
        # # add Test runner file. TODO: check!!!
        #   This could be dependent on framework
        cmFile.write(
            "\t"
            + "${CMAKE_SOURCE_DIR}"
            + sep
            + tmpTestSrcFldr
            + sep
            + "AllTests.cpp"
            + "\n"
        )
        cmFile.write("\t)\n\n")

        # add include directories
        cmFile.write("include_directories(" + "\n")
        # # add source folder
        cmFile.write(
            "\t" + '"' + "${CMAKE_SOURCE_DIR}"
            + sep + tmpTestSrcFldr + '"' + "\n"
        )

        strVl = '%r' % str(pIncludeDir)
        cmFile.write("\t\"" + strVl[1: -1] + "\"\n")

        cmFile.write("\t)\n\n")

        # add find utest library TODO add switch if to use cpputest | gtest and
        # specify compiler

        ##
        str_compilerName = testCfg.co_testToolchain.str_compiler
        pathToTestLibs = Path.cwd() / "Tools" / "testlibs" / \
            str_frameworkFolderName / str_compilerName

        strPathToTestLibs = '%r' % str(pathToTestLibs)
        strPathToTestLibs = strPathToTestLibs[1:-1]
        cmFile.write(
            'find_library(TestLib    libCppUTest    "'
            + strPathToTestLibs + '")\n'
        )
        cmFile.write(
            'find_library(TestLibExt libCppUTestExt "'
            + strPathToTestLibs + '")\n\n'
        )

        # add target link library
        cmFile.write(
            "target_link_libraries(TestApp ${TestLib}" " ${TestLibExt})\n")


def copyAllFilesAndReturnListOfThem(str_pkgName: str, mainCfg: CMainConfig, testCfg: CTestConfig, str_tType: str):
    # Create listOfSource and listOfDestination
    srcLst = []
    dstLst = []
    chckLst = []
    # sep = mainCfg.separ

    # create folder strings
    tmpTestSrcFldr = getSrcTestTempFolderName(testCfg, mainCfg, str_tType)
    pPathToTmpTestSrcFldr = Path(mainCfg.co_pkg.str_testpath) / str_pkgName
    strPathToTmpTestSrcFldr = str(pPathToTmpTestSrcFldr)
    pTmpTestSrcFullPath = pPathToTmpTestSrcFldr / tmpTestSrcFldr
    strTmpTestSrcFullPath = str(pTmpTestSrcFullPath)

    # # start with SUT
    sut = testCfg.SUT_dict
    for key in sut:
        srcLst.append(
            str(Path(key.replace("SRCFLDR", mainCfg.co_pkg.str_srcfldr))))
        if "SRC_TEMP" in sut[key]:
            dstLst.append(
                str(
                    Path(sut[key].replace("SRC_TEMP", strTmpTestSrcFullPath))
                    / Path(key).name
                )
            )
        else:
            if sut[key].split(mainCfg.separ)[-1]:
                dstLst.append(sut[key].replace(
                    "SRC_TEMP", strTmpTestSrcFullPath))

    # print("\n", srcLst, "\n")
    # print("\n", dstLst, "\n")
    # exit(0)

    # # start with OTHER
    other = testCfg.OTHER_dict
    for key in other:
        keyStr = (
            key.replace("SRCFLDR", mainCfg.co_pkg.str_srcfldr)
            .replace("SRC_TEMP", strTmpTestSrcFullPath)
            .replace("TPKG_FOLDER", strPathToTmpTestSrcFldr)
        )
        valStr = (
            other[key]
            .replace("TESTPATH", mainCfg.co_pkg.str_testpath)
            .replace("TPKG_FOLDER", strPathToTmpTestSrcFldr)
            .replace("SRC_TEMP", strTmpTestSrcFullPath)
        )

        # check if valStr contain specific destination folderPath
        pathSrc = Path(keyStr)
        pathDst = Path(valStr)
        # print(keyStr)
        # print(valStr)
        if len(pathDst.parts) > 0:  # unempty list path
            if len(pathDst.name.split(".")) < 2:
                pathDst = pathDst / pathSrc.name
        srcLst.append(str(pathSrc))
        dstLst.append(str(pathDst))

    for srcFile in srcLst:
        pSrcFile = Path(srcFile)
        # print(str(pSrcFile), pSrcFile.exists())
        # if not pSrcFile.exists():
        assert pSrcFile.exists(), "Unexisting file: %s. Please check %s\\test.ini file." % (
            srcFile, str_pkgName)
    # copy test.cpp and AllTests.cpp to tmpSourceFolder
    srcLst.append(str(pPathToTmpTestSrcFldr
                  / mainCfg.co_pkg.str_srctestfldr / "test.cpp"))
    srcLst.append(str(pPathToTmpTestSrcFldr
                  / mainCfg.co_pkg.str_srctestfldr / "AllTests.cpp"))

    dstLst.append(str(pTmpTestSrcFullPath / "test.cpp"))
    dstLst.append(str(pTmpTestSrcFullPath / "AllTests.cpp"))

    # before copy we check if folder exists, if not we have to create it.
    if not pTmpTestSrcFullPath.is_dir():
        pTmpTestSrcFullPath.mkdir()

    # do copy operation for all files
    assert len(srcLst) == len(dstLst), (
        "Source list and Destination list" "must have the same lenght!"
    )
    for iter in range(len(srcLst)):
        dPath = Path(dstLst[iter]).parent
        if not dPath.exists():
            dPath.mkdir()
        if (not Path(dstLst[iter]).is_file()) or (
            not filecmp.cmp(srcLst[iter], dstLst[iter])
        ):
            Path(dstLst[iter]).write_text(Path(srcLst[iter]).read_text())

    chckLst = srcLst.copy()
    chckLst.append(str(pPathToTmpTestSrcFldr
                   / mainCfg.co_pkg.str_testcfgfilename))
    return srcLst, dstLst, chckLst


def interpretCPPUTESToutput(resultFile: str):
    with open(resultFile, "r") as File:
        resultData = File.read()

    resultSplit = resultData.split("\n")

    statusTest = False
    if len(resultSplit) >= 2:
        if resultSplit[1].split(" ")[0] == "OK":
            statusTest = True
    return statusTest


def interpretCPPCHECKerrors(errorFile: str):
    with open(errorFile, "r") as File:
        errData = File.read()

    errLines = errData.split("\n")
    # print(errLines)

    # remove Unmatched hit
    errLines = [line for line in errLines if "Unmatched" not in line]
    # print(errLines)
    errLines = [line for line in errLines if line]  # remove empty lines
    # print(errLines)
    return int(len(errLines) / 3)

    # errLines = list(filter(None, errLines))


# define our clear function
def clear():

    # for windows
    if os.name == "nt":
        _ = os.system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system("clear")
