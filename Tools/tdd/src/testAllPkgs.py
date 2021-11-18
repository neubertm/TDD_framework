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
import TDDConfig
import tdd_support
import readchar
import os
import time
from tabulate import tabulate
import CodeStatistics
import colorama
from colorama import Fore, Style
from pathlib import Path
import subprocess
import KeyPressThread
import keyboard
# import sys
import cmakeSupport


def testOnePkg(pckgDir, mCfg):
    print(pckgDir)

    kpt = KeyPressThread.KeyboardThread()

    env_bckp = os.environ.copy()
    os.environ['PATH'] = mCfg.co_env.str_cmake + ";" + os.environ['PATH']
    os.environ['PATH'] = mCfg.co_env.str_mingw + ";" + os.environ['PATH']
    os.environ['PATH'] = mCfg.co_env.str_cppcheck + ";" + os.environ['PATH']

    str_testPackagesPath = mCfg.co_pkg.str_testpath
    str_testPackageSuffix = mCfg.co_pkg.str_testfldr_suffix
    len_tpkgS = len(str_testPackageSuffix)

    path_dir = Path(str_testPackagesPath).glob("*_Tpkg")
    dir_lst = [folder for folder in path_dir if folder.is_dir()]

    lst_testDir = []
    for dir in dir_lst:
        strdir = str(dir.stem)
        if (strdir[-len_tpkgS:] == str_testPackageSuffix):
            lst_testDir.append(strdir)

    task_lst = [CTestPkg(pckg, mCfg, kpt) for pckg in lst_testDir]
    pTask = None
    for task in task_lst:
        if task.name == pckgDir:
            pTask = task
            break
    pTask.b_silent = False
    pTask.run()

    # revert environment varaiables
    os.environ = env_bckp

    print("Press any key to quit.\n")
    # keyboard.read_key()
    readchar.readkey()


def debug(lstPackage, mainCfg):
    kpt = KeyPressThread.KeyboardThreadDbg()
    task_lst = [CTestPkg(pckg, mainCfg, kpt) for pckg in lstPackage]
    id = 1
    task_lst[id].b_silent = False
    task_lst[id].run()


def tests_minimized(lstPackage, mainCfg):
    colorama.init()
    env_bckp = os.environ.copy()
    os.environ['PATH'] = mainCfg.co_env.str_cmake + ";" + os.environ['PATH']
    os.environ['PATH'] = mainCfg.co_env.str_mingw + ";" + os.environ['PATH']
    os.environ['PATH'] = mainCfg.co_env.str_cppcheck + ";" + os.environ['PATH']

    kpt = KeyPressThread.KeyboardThread()

    task_lst = [CTestPkgThread(pckg, mainCfg, kpt)
                for pckg in lstPackage]

    numTasks = len(task_lst)
    resultTabRef = []
    tdd_support.clear()
    while(True):
        numOfTerminated = 0
        numOfIdle = 0
        resultTab = []
        for task in task_lst:
            result = [
                task.name,
                task.str_step,
                task.str_status,
                task.str_testStatus,
                task.str_uncoverage,
                task.str_analysis,
                task.str_complexity]
            resultTab.append(result)
            if "Terminated" in task.str_status:
                numOfTerminated += 1
            if "Idle" in task.str_status:
                numOfIdle += 1
        if numOfTerminated == numTasks:
            break

        bRewrite = False
        if not resultTabRef:
            bRewrite = True
        else:
            bIsSame = True
            for idx in range(len(resultTab)):
                for idy in range(len(resultTab[0])):
                    bIsSame *= (resultTab[idx][idy] == resultTabRef[idx][idy])
            if not bIsSame:
                bRewrite = True

        if bRewrite:
            resultTabRef = resultTab
            errPkgList = []
            #tdd_support.clear()
            #print(result[1])
            statusStr = ""
            resultStr = ""
            # for id in range(3):
            #     resultStr += chr(0x00BC + id)
            # resultStr += "|"

            colorChar = Style.RESET_ALL
            for result in resultTab:

                # statusStr += result[1] + " "
                charAsNum = 0x20
                if result[1] in ["CMake", "Makefile"]:
                    # charAsNum = 177
                    charAsNum = 0xBC

                if result[1] == "Test":
                    charAsNum = 0xBD
                    # charAsNum = 66

                if result[1] in ["Coverage", "StaticCheck", "Analysis"]:
                    charAsNum = 0xBE
                    # charAsNum = 67

                if result[1] == "Finished":
                    charAsNum = 0x2588

                statusStr += result[3] + " "
                # StatusList = ["Empty" "Fail" "Pass"]
                if "Empty" in result[3]:
                    colorChar = Fore.YELLOW
                if "Fail" in result[3]:
                    colorChar = Fore.RED
                    errPkgList.append(result[0])
                if "Pass" in result[3]:
                    colorChar = Fore.GREEN

                resultStr += colorChar + chr(charAsNum) + Style.RESET_ALL

            tdd_support.clear()
            print("[%s]" % (resultStr))
            if errPkgList:
                print("Corrupted or incompilable tests:")
                for errPkg in errPkgList:
                    print(Fore.RED + errPkg + Style.RESET_ALL)
            # sys.stdout.write("\r")
            # sys.stdout.flush()
            # sys.stdout.write("\r\r[%s]" % (resultStr))
            # sys.stdout.flush()

            # sys.stdout.write("\r[%s]%s" % (resultStr, 5*" "))
            # print("[%s], [%s]" % (resultStr, statusStr))
            # sys.stdout.write("\r[%s]" % (resultStr))
            # sys.stdout.write("[%s]\n" % (resultStr))

            #sys.stdout.write("[%s] %s\n" % (resultStr, statusStr))

            # print(tabulate(resultTab, headerTab, tablefmt="pretty"))

        time.sleep(0.5)

    # revert environment varaiables
    os.environ = env_bckp

    print("Press any key to quit.\n")
    readchar.readkey()


def tests(lstPackage, mainCfg):
    colorama.init()
    # print("Test all pkgs")
    # print(lstPackage)
    # debug(lstPackage, mainCfg)
    env_bckp = os.environ.copy()
    os.environ['PATH'] = mainCfg.co_env.str_cmake + ";" + os.environ['PATH']
    os.environ['PATH'] = mainCfg.co_env.str_mingw + ";" + os.environ['PATH']
    os.environ['PATH'] = mainCfg.co_env.str_cppcheck + ";" + os.environ['PATH']

    kpt = KeyPressThread.KeyboardThread()

    task_lst = [CTestPkgThread(pckg, mainCfg, kpt) for pckg in lstPackage]

    numTasks = len(task_lst)

    headerTab = [
        "Name",
        "Step",
        "Status",
        "Test Status",
        "Noncovered line",
        "Static err",
        "Complexity err"]
    resultTabRef = []
    while(True):
        numOfTerminated = 0
        resultTab = []
        for task in task_lst:
            result = [
                task.name,
                task.str_step,
                task.str_status,
                task.str_testStatus,
                task.str_uncoverage,
                task.str_analysis,
                task.str_complexity]
            resultTab.append(result)
            if "Terminated" in task.str_status:
                numOfTerminated += 1
        if numOfTerminated == numTasks:
            break

        bRewrite = False
        if not resultTabRef:
            bRewrite = True
        else:
            bIsSame = True
            for idx in range(len(resultTab)):
                for idy in range(len(resultTab[0])):
                    bIsSame *= (resultTab[idx][idy] == resultTabRef[idx][idy])
            if not bIsSame:
                bRewrite = True

        if bRewrite:
            resultTabRef = resultTab
            tdd_support.clear()
            print(tabulate(resultTab, headerTab, tablefmt="pretty"))

        # print(tabulate(resultTab))
        time.sleep(1)

    resultTab = []
    for task in task_lst:
        result = [
            task.name,
            task.str_step,
            task.str_status,
            task.str_testStatus,
            task.str_uncoverage,
            task.str_analysis,
            task.str_complexity]
        resultTab.append(result)
    tdd_support.clear()
    print(tabulate(resultTab, headerTab, tablefmt="pretty"))

    # revert environment varaiables
    os.environ = env_bckp

    print("Press any key to quit.\n")
    readchar.readkey()
    # keyboard.read_key()


class CTestPkg():
    str_step: str
    str_status: str
    str_testBinName: str
    str_uncoverage: str
    str_testStatus: str
    str_analysis: str
    str_complexity: str
    path_buildFldr: Path
    str_srcFldr: str
    str_testRoot: str
    tCfg: TDDConfig.CTestConfig
    b_silent: bool
    str_cmakeName: str
    b_infiniteRun: bool
    LS_chckLFile: [str]
    LS_srcL: [str]
    LS_dstL: [str]
    dic_chckFiles: {}

    def __init__(self, name, mainCfg, kpt):
        # super(CTestPkg, self).__init__(name=name)
        self.mCfg = mainCfg
        self.name = name
        self.str_testBinName = cmakeSupport.getTestBinaryName()
        self.str_step = "Created"
        self.str_status = "Ready"
        self.str_uncoverage = "Empty"
        self.str_testStatus = "Empty"
        self.str_analysis = "Empty"
        self.str_complexity = "Empty"
        self.str_testRoot = ""
        self.path_buildFldr = Path("")
        self.str_srcFldr = ""
        self.tCfg = TDDConfig.CTestConfig()
        self.b_silent = False
        self.str_testType = "single"
        self.str_cmakeName = ""
        self.b_infiniteRun = True
        self.LS_chckLFile = []
        self.LS_srcL = []
        self.LS_dstL = []
        self.dic_chckFiles = {}
        self.thread_keyPress = kpt
        # self.start()

    def __readInit__(self):
        self.__writeStep__("Read inifile")
        path_folder = Path(self.mCfg.co_pkg.str_testpath) / self.name
        self.str_testRoot = str(path_folder)

        iniFile = path_folder / self.mCfg.co_pkg.str_testcfgfilename
        self.tCfg.readCfgFile(str(iniFile))
        pass

    def __createCmake__(self):
        self.__writeStep__("Gen CMake")
        # self.str_cmakeName = tdd_support.getCompilerNameInTestConfig(self.tCfg)
        self.str_cmakeName = self.tCfg.co_testToolchain.str_compiler
        self.str_cmakeName += "_" + self.str_testType
        self.str_cmakeName += ".cmake"
        path_cmakelist = Path(self.mCfg.co_pkg.str_testpath) / \
            self.name / self.str_cmakeName

        str_cmakelist = str(path_cmakelist)
        if path_cmakelist.is_file():
            try:
                path_cmakelist.unlink()
            except BaseException:
                print('Error: removing CMakeLists.txt failed.')
        self.__writeStep__("Creating CMakeLists")
        tdd_support.createCMakeListsFromConfiguration(
            str_cmakelist, self.mCfg, self.tCfg, self.str_testType)
        pass

    def __fileCopying__(self):
        self.__writeStep__("Copy files")

        # copy all files and create lists
        self.LS_srcL, self.LS_dstL, self.LS_chckLFile = tdd_support.copyAllFilesAndReturnListOfThem(
            self.name, self.mCfg, self.tCfg, self.str_testType)

        # create dictionary key is chckLFile, value status_time
        self.dic_chckFiles = {
            chckF: os.stat(chckF).st_mtime for chckF in self.LS_chckLFile}

        compilerName = self.tCfg.co_testToolchain.str_compiler
        # self.str_srcFldr
        self.str_srcFldr = tdd_support.getSrcTestTempFolderName(
            self.tCfg, self.mCfg, self.str_testType)

        bFldr = compilerName + self.mCfg.co_pkg.str_buildsuffix + "_" + self.str_testType
        path_folder = Path(self.mCfg.co_pkg.str_testpath) / self.name
        self.path_buildFldr = path_folder / bFldr
        if self.path_buildFldr.is_dir():
            tdd_support.del_folder(self.path_buildFldr)
            pass

        self.path_buildFldr.mkdir()
        pass

    def __fileCopyingUpdatedOnly__(self):
        locdic_chckFiles = {
            chckF: os.stat(chckF).st_mtime for chckF in self.LS_chckLFile}
        for id_file, str_file in enumerate(self.LS_chckLFile):
            if locdic_chckFiles.get(str_file) != self.dic_chckFiles.get(str_file):
                Path(self.LS_dstL[id_file]).write_text(
                    Path(self.LS_srcL[id_file]).read_text())
        self.dic_chckFiles = locdic_chckFiles

    def __cmake__(self):
        self.__writeStep__("CMake")
        op_cmakeLst = []
        op_cmakeLst.append("cmake")
        # root folder (position of cmakefile)
        op_cmakeLst.append("-S")
        op_cmakeLst.append(self.str_testRoot)

        op_cmakeLst.append("-B")
        op_cmakeLst.append(str(self.path_buildFldr))

        op_cmakeLst.append("-G")
        op_cmakeLst.append(cmakeSupport.getGeneratorName(self.tCfg))

        op_cmakeLst.append("-DCMAKE_CXX_OUTPUT_EXTENSION_REPLACE=ON")

        op_cmakeLst.append("-DCMAKELISTS_NAME=" + self.str_cmakeName)
        if self.b_silent:
            op_cmakeLst.append(">")
            op_cmakeLst.append(str(self.path_buildFldr / "cmake.out"))

            op_cmakeLst.append("2>")
            op_cmakeLst.append(str(self.path_buildFldr / "cmake.err"))

        # print(op_cmakeLst)
        subprocess.call(op_cmakeLst, shell=True)

    def __make__(self):
        self.__writeStep__("Makefile")

        testAppPath = self.path_buildFldr / self.str_testBinName
        if testAppPath.is_file():
            try:
                testAppPath.unlink()
            except BaseException:
                with open("debug.log", "a") as log:
                    log.write("BaseException when trying to delete this file: "
                              + testAppPath + "\n")
                pass
        op_makeLst = []

        op_makeLst.append(cmakeSupport.getMaketoolName(self.tCfg))

        op_makeLst.append('-C')
        op_makeLst.append(str(self.path_buildFldr))
        if self.b_silent:
            op_makeLst.append('>')
            op_makeLst.append(str(self.path_buildFldr / "makefile.out"))

            op_makeLst.append('2>')
            op_makeLst.append(str(self.path_buildFldr / "makefile.err"))

        subprocess.call(op_makeLst, shell=True)

        if not (self.path_buildFldr / self.str_testBinName).is_file():
            self.__writeStatus__("Terminated")
            self.str_testStatus = "Fail"
            return(False)
        return(True)

    def __runTestBin__(self):
        bRetVal = True
        testAppPath = str(self.path_buildFldr / self.str_testBinName)
        outF = str(self.path_buildFldr / "testbin.out")
        errF = str(self.path_buildFldr / "testbin.err")

        self.__writeStep__("Test")

        op_testRunLst = []

        op_testRunLst.append(testAppPath)
        if self.b_silent:
            op_testRunLst.append(">")
            op_testRunLst.append(outF)

            op_testRunLst.append("2>")
            op_testRunLst.append(errF)
        else:
            op_testRunLst.append("-v")
            op_testRunLst.append("-c")
            print(10*'-' + '< ' + self.name + ' >' + 10*'-' + '\n')

        intRetVal = subprocess.call(op_testRunLst, shell=True)

        if self.b_silent:
            testResult = 0
            if intRetVal <= 1 :
                testResult = tdd_support.interpretCPPUTESToutput(outF)
            if testResult == True:
                self.str_testStatus = Fore.GREEN + "Pass" + Style.RESET_ALL
            else:
                self.str_testStatus = Fore.RED + "Fail" + Style.RESET_ALL
                bRetVal = False
        else:
            if intRetVal > 1:
                print(Fore.RED + '\nSomething is rotten in (Denmark) that code.')
                print('Test application terminate with this error: %i' % intRetVal)
                print(Style.RESET_ALL)
        return(bRetVal)

    def __coverage__(self, sutList: [str], silent=True):
        # if tdd_support.isCoverageEnabled(self.tCfg):
        if self.tCfg.co_coverage.isTurnedOn:
            self.__writeStep__("Coverage")

            cover_out = str(self.path_buildFldr / "coverage.out")
            cover_err = str(self.path_buildFldr / "coverage.err")

            covCmdLst = []
            covCmdLst.append("gcov")
            covCmdLst.append("--object-directory")
            covCmdLst.append(
                str(Path("CMakeFiles") / "TestApp.dir" / self.str_srcFldr))
            for sutCovListItem in sutList:
                covCmdLst.append(str(Path(self.str_testRoot, sutCovListItem)))

            covCmdLst.append(">")
            covCmdLst.append("coverage.out")
            covCmdLst.append("2>")
            covCmdLst.append("coverage.err")
            # print(covCmdLst)
            subprocess.call(covCmdLst, shell=True, cwd=self.path_buildFldr)
            lst_file, dict_covFile = tdd_support.interpretGCOV2lists(
                cover_out, self.path_buildFldr)
            if not lst_file:
                self.str_uncoverage = Fore.RED + "Fail" + Style.RESET_ALL
                if not self.b_silent:
                    print(Fore.RED + "Coverage evaluation failed!" + Style.RESET_ALL)
                return
            # self.str_uncoverage = ""
            listLines = []
            # sutFileNames = [sutFileName.split(
            #     "\\")[-1] for sutFileName in sutList]
            sutFileNames = [str(Path(sutFileName).name)
                            for sutFileName in sutList]
            isCoverageProblem = False
            for key in dict_covFile:
                # if not key.contain(".hpp."):
                # if dict_covFile[key] :
                # print( key,"Uncovered lines: ", dict_covFile[key])
                if any(sfname in key for sfname in sutFileNames):
                    cntUncov = len(dict_covFile[key])
                    if cntUncov:
                        str_uncov = Fore.RED
                        isCoverageProblem = True
                    else:
                        str_uncov = Fore.GREEN
                    str_uncov += str(cntUncov) + Style.RESET_ALL
                    listLines.append(str_uncov)
                # else :
                #    listLines.append("0")

            self.str_uncoverage = ','.join(listLines)
            if not self.b_silent:
                print("Non covered lines: " + self.str_uncoverage)
                if isCoverageProblem:
                    print(
                        "Some lines could be duplicite"
                        + " because c++ create multiple implementation of functions")
                for file in dict_covFile:
                    lineLst = dict_covFile[file]
                    res = []
                    [res.append(x) for x in lineLst if x not in res]
                    lenOfLineLst = len(res)
                    if lenOfLineLst != 0:
                        strLineLst = ", ".join(res)
                        print(Fore.LIGHTRED_EX + '.'.join(file.split(".")[
                              :-1]) + " [ " + strLineLst + "]" + Style.RESET_ALL)
        else:
            self.str_uncoverage = Fore.YELLOW + "OFF" + Style.RESET_ALL

    def __staticCheck__(self, sutList: [str]):
        if self.tCfg.co_codeStatistics.isTurnedOn:
            self.__writeStep__("StaticCheck")
            op_lst = []
            op_lst.append("cppcheck")

            op_lst.append("--enable=all")
            op_lst.append("--inconclusive")
            op_lst.append("--library=posix")

            if not self.tCfg.co_staticAnalysis.isLanguageDefinedBySuffix:
                op_lst.append("--language="
                              + self.tCfg.co_staticAnalysis.str_ForcedLang)

            op_lst.append("--std=" + self.tCfg.co_staticAnalysis.str_c_version)
            op_lst.append(
                "--std=" + self.tCfg.co_staticAnalysis.str_cpp_version)

            for supp in self.tCfg.co_staticAnalysis.suppressionLst:
                op_lst.append("--suppress=" + supp)
            # TODO add switch for turning all to C++ file. Configurable from test.ini
            # add c++ version standard
            # op_statCheck += "--std=c++11 "
            check_out = str(self.path_buildFldr / "cppcheck.out")
            check_err = str(self.path_buildFldr / "cppcheck.err")
            for sutListItem in sutList:
                op_lst.append(str(self.path_buildFldr / sutListItem))

            op_lst.append("-I")
            op_lst.append(str(self.path_buildFldr / ".." / self.str_srcFldr))

            op_lst.append(">")
            op_lst.append(check_out)

            op_lst.append("2>")
            op_lst.append(check_err)

            # print(op_lst)
            subprocess.call(op_lst, shell=True)

            numOfError = tdd_support.interpretCPPCHECKerrors(check_err)
            if numOfError != 0:
                self.str_analysis = Fore.RED
            else:
                self.str_analysis = Fore.GREEN
            self.str_analysis += str(numOfError) + Style.RESET_ALL

            if not self.b_silent:
                print("Number of static check errors: ", self.str_analysis)
                if numOfError:
                    numL = 40
                    print(numL*'-' + '\n')
                    with open(check_err, 'r') as fin:
                        print(fin.read())
                    print(numL*'-')
        else:
            self.str_analysis = Fore.YELLOW + "OFF" + Style.RESET_ALL

    def __codeAnalysis__(self, sutList: [str]):
        if self.tCfg.co_codeStatistics.isTurnedOn:
            self.__writeStep__("Analysis")

            lizardCsv = str(self.path_buildFldr / "lizard.csv")
            lizard_out = str(self.path_buildFldr / "lizard.out")
            lizard_err = str(self.path_buildFldr / "lizard.err")

            # choose used parameters
            if self.tCfg.co_codeStatistics.isUsedTestSpecificOnly == True:
                int_McCabeCompl = self.tCfg.co_codeStatistics.int_mccabeComplex
                int_FncLen = self.tCfg.co_codeStatistics.int_fncLength
                int_ParCnt = self.tCfg.co_codeStatistics.int_paramCnt
            else:
                if self.tCfg.co_codeStatistics.isUsedStricter == True:
                    int_McCabeCompl = min(self.tCfg.co_codeStatistics.int_mccabeComplex, self.mCfg.co_stat.int_mccabeComplex)
                    int_FncLen = min(self.tCfg.co_codeStatistics.int_fncLength, self.mCfg.co_stat.int_fncLength)
                    int_ParCnt = min(self.tCfg.co_codeStatistics.int_paramCnt, self.mCfg.co_stat.int_paramCnt)
                else:
                    int_McCabeCompl = self.mCfg.co_stat.int_mccabeComplex
                    int_FncLen = self.mCfg.co_stat.int_fncLength
                    int_ParCnt = self.mCfg.co_stat.int_paramCnt

            op_lst = []
            op_lst.append('lizard')
            for sutListItem in sutList:
                op_lst.append(str(self.path_buildFldr / sutListItem))

            op_lst.append("-C")
            op_lst.append(str(int_McCabeCompl))

            op_lst.append("-L")
            op_lst.append(str(int_FncLen))

            op_lst.append("-a")
            op_lst.append(str(int_ParCnt))

            op_lst.append("-o")
            op_lst.append(lizardCsv)

            op_lst.append(">")
            op_lst.append(lizard_out)

            op_lst.append("2>")
            op_lst.append(lizard_err)

            subprocess.call(op_lst, shell=True)

            errTab = CodeStatistics.interpretLIZARDoutfile(
                lizardCsv, int_McCabeCompl, int_ParCnt, int_FncLen)
            cntError = len(errTab)
            if cntError:
                self.str_complexity = Fore.RED
            else:
                self.str_complexity = Fore.GREEN
            self.str_complexity += str(cntError) + Style.RESET_ALL
            if not self.b_silent:
                print("Code analysis error cnt: ", self.str_complexity)
                if cntError:
                    CodeStatistics.printLIZARDerrArrayShortAndColor(errTab,
                            int_McCabeCompl, int_ParCnt, int_FncLen)
        else:
            self.str_complexity = Fore.YELLOW + "OFF" + Style.RESET_ALL

    def __codeEvaluation__(self):
        sutList = tdd_support.createSutList(
            self.tCfg, self.mCfg, self.str_testType)
        self.__coverage__(sutList)
        self.__staticCheck__(sutList)
        self.__codeAnalysis__(sutList)

    def __writeStatus__(self, status: str):
        lStatus = status
        colDict = {"Start": Fore.YELLOW, "Run": Fore.GREEN, "Idle": Fore.MAGENTA,
                   "Error": Fore.RED, "Failure": Fore.RED, "Terminated": Fore.LIGHTYELLOW_EX}
        if lStatus in colDict:
            lStatus = colDict.get(status) + lStatus + Style.RESET_ALL
        else:
            lStatus = Fore.CYAN + lStatus + Style.RESET_ALL
        self.str_status = lStatus

    def __writeStep__(self, step: str):
        self.str_step = step
        if not self.b_silent:
            print("\n" + Fore.YELLOW + self.str_step + Style.RESET_ALL)
        pass

    def __checkExternalTerminationCondition__(self):
        if self.thread_keyPress.isAnyKeyPressed():
            return(False)
        else:
            return(True)

    def __checkIniFileChanged__(self):
        locdic_chckFiles = {
            chckF: os.stat(chckF).st_mtime for chckF in self.LS_chckLFile}
        if locdic_chckFiles.get(self.LS_chckLFile[-1]) == self.dic_chckFiles.get(self.LS_chckLFile[-1]):
            return(False)
        else:
            return(True)

    def __cleanStatusVariables__(self):
        self.str_uncoverage = "Empty"
        self.str_testStatus = "Empty"
        self.str_analysis = "Empty"
        self.str_complexity = "Empty"

    def __cleanTmpSource__(self):
        path_srcFldr = Path(self.mCfg.co_pkg.str_testpath) / self.name / tdd_support.getSrcTestTempFolderName(
            self.tCfg, self.mCfg, self.str_testType)

        # print(str(path_srcFldr.resolve()))
        if path_srcFldr.is_dir():
            # print("Deleting tmp source folder :" + str(path_srcFldr.resolve()))
            tdd_support.del_folder(path_srcFldr)
        assert not path_srcFldr.is_dir(), "Something went wrong. Temp source was not deleted!"

    def __checkSrcFileChanged__(self):
        locdic_chckFiles = {
            chckF: os.stat(chckF).st_mtime for chckF in self.LS_chckLFile}
        for str_file in self.LS_chckLFile:
            if locdic_chckFiles.get(str_file) != self.dic_chckFiles.get(str_file):
                return(True)
        return(False)

    def __cleanScreenBeforeRerun__(self):
        if not self.b_silent:
            tdd_support.clear()

    def __runTest__(self):
        b_buildStatus = False
        self.__writeStep__("Start")
        self.__writeStatus__("Run")
        self.__readInit__()
        self.__createCmake__()
        self.__cleanTmpSource__()
        self.__fileCopying__()
        self.__cmake__()
        while True:
            b_buildStatus = self.__make__()
            if b_buildStatus is True:
                b_buildStatus = self.__runTestBin__()
            if b_buildStatus is True:
                self.__codeEvaluation__()
                self.__writeStatus__("Idle")
            else:
                self.__writeStatus__("Error")
            self.__writeStep__("Finished")
            while True:
                time.sleep(1)
                self.b_infiniteRun = self.__checkExternalTerminationCondition__()
                if not self.b_infiniteRun:
                    return
                if self.__checkIniFileChanged__():
                    self.__cleanStatusVariables__()
                    return
                if self.__checkSrcFileChanged__():
                    self.__cleanStatusVariables__()
                    self.__fileCopyingUpdatedOnly__()
                    self.__cleanScreenBeforeRerun__()
                    break

    def run(self):

        while self.b_infiniteRun:
            self.__runTest__()
        self.__writeStep__("Finished")
        self.__writeStatus__("Terminated")
        # print("\n",self.name, " Finished!")


class CTestPkgThread(CTestPkg, threading.Thread):
    def __init__(self, name, mainCfg, kpt):
        threading.Thread.__init__(self, name=name)
        CTestPkg.__init__(self, name=name, mainCfg=mainCfg, kpt=kpt)
        self.b_silent = True
        self.str_testType = "summary"
        self.start()


class CTestPkgThreadMinimal(CTestPkg, threading.Thread):
    def __init__(self, name, mainCfg, kpt):
        threading.Thread.__init__(self, name=name)
        CTestPkg.__init__(self, name=name, mainCfg=mainCfg, kpt=kpt)
        self.b_silent = True
        self.str_testType = "minimal"
        self.start()


if __name__ == "__main__":
    mainConfig = TDDConfig.CMainConfig("project.ini")

    os.environ['PATH'] += ";" + mainConfig.co_env.str_cmake
    os.environ['PATH'] += ";" + mainConfig.co_env.str_mingw
    os.environ['PATH'] += ";" + mainConfig.co_env.str_cppcheck
    scrP = "C:\\Users\\z003ukaz\\AppData\\Local"
    scrP += "\\Programs\\Python\\Python39\\Scripts"
    os.environ['PATH'] += ";" + scrP

    str_testPackagesPath = mainConfig.co_pkg.str_testpath
    str_testPackageSuffix = mainConfig.co_pkg.str_testfldr_suffix
    len_tpkgS = len(str_testPackageSuffix)

    path_dir = Path(str_testPackagesPath).glob("*_Tpkg")
    dir_lst = [folder for folder in path_dir if folder.is_dir()]

    lst_testDir = []
    for dir in dir_lst:
        strdir = str(dir.stem)
        if (strdir[-len_tpkgS:] == str_testPackageSuffix):
            lst_testDir.append(strdir)

    debug(lst_testDir, mainConfig)
    debug(lst_testDir, mainConfig)
