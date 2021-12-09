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
from consolemenu import ConsoleMenu
from consolemenu.items import ExitItem
from consolemenu.items import FunctionItem

from TDDConfig import CEnvCfg
from TDDConfig import CCodeStatParamMinValue
from TDDConfig import CTestPkgDescription
from TDDConfig import CMainConfig

from createNewModule import CreateNewModule

from pathlib import Path

import testAllPkgs as tall

import versionSupport as vs


def createTestMenu(coEnv: CEnvCfg, filePath: Path):
    print(str(filePath))
    assert filePath.is_file(), "Configuration file doesn exists. %s" % (str(filePath))

    tMenu = TestMenu(coEnv, filePath)
    tMenu.createAndShow()

    # input("waiting until keypress")
    pass


class TestMenu:
    co_env: CEnvCfg
    co_codeStatistics: CCodeStatParamMinValue
    co_pkg: CTestPkgDescription
    contentLst: []
    menu: ConsoleMenu
    obj_createModule: CreateNewModule

    def __init__(self, coEnv: CEnvCfg, pathFileTestPkg: Path):
        self.co_env = coEnv
        self.co_codeStatistics = CCodeStatParamMinValue()
        self.co_codeStatistics.readFromFile(str(pathFileTestPkg))
        self.co_pkg = CTestPkgDescription()
        self.co_pkg.readFromFile(str(pathFileTestPkg))
        self.contentLst = []
        o_vd = vs.VersionRelease()
        self.menu = ConsoleMenu("eTDD is C++ unit test framework. %s" % (o_vd.getStrReleaseVersion()),
                                "Choose test packag/es variant.", show_exit_option=False)
        self.obj_createModule = CreateNewModule(self.co_pkg)

    def __getTestPackageList__(self, str_path, str_suff):
        regExpPattern = "*" + str_suff
        path_dir = Path(str_path).glob(regExpPattern)
        len_tpkgS = len(str_suff)

        dir_lst = [folder for folder in path_dir if folder.is_dir()]
        testDirList = []
        for dir in dir_lst:
            # strip path
            strDir = str(dir.stem)
            if (strDir[-len_tpkgS:] == str_suff):
                testDirList.append(strDir)
        testNameList = [dir[:-len_tpkgS] for dir in testDirList]
        return testDirList, testNameList

    def __prepareMenu__(self, testDirList, testNameList):
        o_vr = vs.VersionRelease()
        o_dv = vs.VersionDevelopment()
        verDevFile = Path('.') / "Tools" / "tdd" / "devVersion.txt"

        self.menu = ConsoleMenu("eTDD is C++ unit test framework. (%s)" % (o_vr.getStrReleaseVersion()),
                            "Choose test packag/es variant.", show_exit_option=False)

        if True == o_dv.readVersionFile(verDevFile):
            self.menu.epilogue_text = "DVer[%s, %s]" %(o_dv.getTime(), o_dv.getHash()[:7])

        exit = ExitItem("Auf wiedersehen!!", menu=None)
        self.menu.append_item(exit)

        self.obj_createModule = CreateNewModule(self.co_pkg)
        addNewModule_item = FunctionItem('Create new module from templates',
                                    self.obj_createModule.createNewModule
                                    ,[])
        self.menu.append_item(addNewModule_item)

        mCfg = CMainConfig()
        mCfg.co_env = self.co_env
        mCfg.co_pkg = self.co_pkg
        mCfg.co_stat = self.co_codeStatistics

        # A FunctionItem runs a Python function when selected
        AllTestMinimized_item = FunctionItem("Run all tests(minimized)",
                                             tall.tests_minimized,
                                             [testDirList, mCfg])
        self.menu.append_item(AllTestMinimized_item)

        AllTest_item = FunctionItem("Run all tests",
                                    tall.tests,
                                    [testDirList, mCfg])
        self.menu.append_item(AllTest_item)

        for num, testDir in enumerate(testDirList):
            testItem = FunctionItem("Test " + testNameList[num],
                                    tall.testOnePkg,
                                    [testDir, mCfg])
            self.menu.append_item(testItem)

    def createAndShow(self):
        str_testPackagesPath = self.co_pkg.str_testpath
        str_testPackageSuffix = self.co_pkg.str_testfldr_suffix
        testDirList, testNameList = self.__getTestPackageList__(
            str_testPackagesPath, str_testPackageSuffix)
        print(testDirList)
        print(testNameList)
        self.__prepareMenu__(testDirList, testNameList)
        self.menu.show()
        pass
