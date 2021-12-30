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
import subprocess
from pathlib import Path
from TDDConfig import CTestConfig
from TDDConfig import CMainConfig


def getRightSourceSuffixFromHeader(hSuf):
    suffixDict = {'h': 'c', 'H': 'C', 'hpp': 'cpp', 'HPP': 'CPP'}
    stripSuff = hSuf.replace('.','')
    assert suffixDict.has_key(stripSuff), 'Unexisting header suffix(%s)!' % (stripSuff)
    return suffixDict[stripSuff]

def getCppSuffix(hSuf):
    return 'cpp'


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



def processAllFilesAndReturnListOfThem(str_pkgName: str, mainCfg: CMainConfig, testCfg: CTestConfig, str_tType: str):
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
    str_TstSrcPth = str(pTmpTestSrcFullPath)

    # # start with SUT
    dict = testCfg.SUT_dict
    for key in dict:
        # adding processed path from key to srcLst
        srcLst.append(
            str(Path(key.replace("SRCFLDR", mainCfg.co_pkg.str_srcfldr))))
        #get key as Path
        pathFileSrc = Path(key)
        #extract source pure name
        fileNameSrc = pathFileSrc.name
        #purename for src and dst is same
        fileNameDst = fileNameSrc
        #get destination as Path
        pathFileDst = Path(dict[key])

        fileNameDst = pathFileDst.name
        fileNameDstSuffix = pathFileDst.suffix
        # here we check if in key is file name or only path
        pathFileDst = Path(dict[key].replace("SRC_TEMP", str_TstSrcPth))
        if '' == fileNameDstSuffix:
            # here we have only path, so we use pure name of source file
            pathFileDst = pathFileDst / fileNameSrc

        dstLst.append( str(pathFileDst) )

    # print("\n", srcLst, "\n")
    # print("\n", dstLst, "\n")
    # exit(0)

    # # start with OTHER
    other = testCfg.OTHER_dict
    for key in other:
        keyStr = (
            key.replace("SRCFLDR", mainCfg.co_pkg.str_srcfldr)
            .replace("SRC_TEMP", str_TstSrcPth)
            .replace("TPKG_FOLDER", strPathToTmpTestSrcFldr)
            .replace("TESTPATH", mainCfg.co_pkg.str_testpath)
        )
        valStr = (
            other[key]
            .replace("TESTPATH", mainCfg.co_pkg.str_testpath)
            .replace("TPKG_FOLDER", strPathToTmpTestSrcFldr)
            .replace("SRC_TEMP", str_TstSrcPth)
        )

        # check if valStr contain specific destination folderPath
        pathSrc = Path(keyStr)
        pathDst = Path(valStr)
        # print(keyStr)
        # print(valStr)
        if len(pathDst.parts) > 0:  # unempty list path
            #if len(pathDst.name.split(".")) < 2:
            if '' == pathDst.suffix:
                pathDst = pathDst / pathSrc.name
        srcLst.append(str(pathSrc))
        dstLst.append(str(pathDst))

    # TODO add section with creating Automocks and create new lists for that
    subsDict = {"SRCFLDR": mainCfg.co_pkg.str_srcfldr,
                "SRC_TEMP": str_TstSrcPth,
                "TPKG_FOLDER": strPathToTmpTestSrcFldr,
                "TESTPATH": mainCfg.co_pkg.str_testpath}
    dict = testCfg.AUTOMOCK_dict
    mockSrcLst, mockDstLst, automDic = processMockDictionary(dict, subsDict, getRightSourceSuffixFromHeader)
    srcLst = srcLst + mockSrcLst
    dstLst = dstLst + mockDstLst

    dictCPP = testCfg.AUTOMOCKCPP_dict
    mockSrcCPPLst, mockDstCPPLst, automCppDic = processMockDictionary(dictCPP, subsDict, getCppSuffix)
    srcLst = srcLst + mockSrcCPPLst
    dstLst = dstLst + mockDstCPPLst

    MockIncLst = [patchStrByDict(incItem,subsDict) for incItem in testCfg.AUTOMOCKFLDRINC_lst]

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
    copeListOfFiles(srcLst, dstLst)

    createAutomocks(automDic,MockIncLst)
    createAutomocks(automCppDic,MockIncLst,forcedCpp=True)

    chckLst = srcLst.copy()
    chckLst.append(str(pPathToTmpTestSrcFldr
                   / mainCfg.co_pkg.str_testcfgfilename))


    # define mock src file (HEADER)
    # define mock dst file (C ot C++ SOURCE)
    # automock dictionary
    # run creating automock file based on automockDict
    return srcLst, dstLst, chckLst

def copeListOfFiles(srcLst, dstLst):
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
    pass

def processMockDictionary(dict, subsDict, fnc_suffix):
    srcLst = []
    dstLst = []
    mockDict = {}
    for key in dict:
        procKey = patchStrByDict(key, subsDict)
        procVal = patchStrByDict(dict[key], subsDict)
        pathSrc = Path(procKey)
        str_SrcFileName = pathSrc.name
        str_SrcSuffix = pathSrc.suffix
        str_SrcStripName = str_SrcFileName.replace(pathSrc.suffix, '')
        pathDst = Path(procVal)
        dstFileName = ''
        if '' != pathDst.suffix:
            #extract file name
            dstFileName = pathDst.name
            #remove filename from path
            pathDst = pathDst.parents[0]

        pathHeaderDst = pathDst / str_SrcFileName
        pathMockDst = pathDst / (str_SrcStripName + '_MOCK.' + fnc_suffix(str_SrcSuffix))

        srcLst.append(procKey)
        dstLst.append(str(pathHeaderDst))
        mockDict[procKey] = str(pathMockDst)

    return srcLst, dstLst, mockDict

def createAutomocks(mockDict,incLst,strCppStd = 'c++11', strCStd = 'c99', forcedCpp = False):
    for key in mockDict:
        callAutomockTool(key, mockDict[key], incLst, strCppStd, strCStd, forcedCpp)

def callAutomockTool(headerName, mockName, incList, strCppStd, strCStd, forcedCpp):
    str_PathCppUMockGen = Path('Tools') / 'programs' / 'CppUMockGen-0.4-win64' / 'bin' / 'CppUMockGen.exe'
    op_lst = [str(str_PathCppUMockGen)]

    # i is input
    op_lst.append('--input')
    op_lst.append(headerName)

    # m is mocked file
    op_lst.append('--mock-output')
    op_lst.append(mockName)

    # forced cpp
    if True == forcedCpp:
        op_lst.append('--cpp')
    else:
        op_lst.append('--std')
        op_lst.append(strCStd)

    op_lst.append('--std')
    op_lst.append(strCppStd)



    for incPath in incList:
        op_lst.append('--include-path')
        op_lst.append(incPath)

    # print(op_lst)
    subprocess.call(op_lst, shell=True)

def patchStrByDict(strPath, subsDict):
    strArg = strPath
    for key in subsDict:
        strArg = strArg.replace(key,subsDict[key])

    return strArg

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
