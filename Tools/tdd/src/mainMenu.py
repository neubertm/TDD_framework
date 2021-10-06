#!/usr/bin/python
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

from pathlib import Path

from TDDConfig import CSetupsCfg
from TDDConfig import CEnvCfg

from testMenu import createTestMenu


def testFunc():
    pass


def stripStrName(str_name: str, int_maxLen=20):
    if len(str_name) > int_maxLen:
        hashNum = 4
        hashSign = '*'
        stripName = str_name[0:int((int_maxLen/2) - (hashNum/2))] + \
            hashNum * hashSign + str_name[int(-(int_maxLen/2) + (hashNum/2)):]
        # stripName = str_name[0:5] + hashNum * hashSign + str_name[-5:]
    else:
        stripName = str_name
    return stripName
    pass


class MainMenu:
    co_env: CEnvCfg
    co_setups: CSetupsCfg
    contentLst: []
    menu: ConsoleMenu

    def __init__(self, envCfg: CEnvCfg, setupCfg: CSetupsCfg):
        self.co_env = envCfg
        self.co_setups = setupCfg
        self.contentLst = []
        self.menu = ConsoleMenu("TDDRealm is C++ unit test framework.",
                                "Choose test packages configuration file.",
                                show_exit_option=False)

    def createAndShow(self):
        # create list of file from cfg file
        fileLst = []
        for file in self.co_setups.userSpecifiedSetupFiles:
            fileLst.append(file)

        if self.co_setups.useAllSetups:
            folder = Path(self.co_setups.folder)
            for sub in folder.iterdir():
                if sub.is_file():
                    sfx = sub.suffix
                    if sfx[0] == ".":
                        sfx = sfx[1:]
                    if sfx in self.co_setups.recognizeSetupSuffixes:
                        fileLst.append(sub.name)

        self.__createContentList__(fileLst)

        assert len(self.contentLst) != 0, "Zero configuration files found."
        self.__prepareMenu__()
        self.__showMenu__()

    def __createContentList__(self, fileLst):
        self.contentLst = []
        folderPath = Path(self.co_setups.folder)
        for file in fileLst:
            filePath = folderPath / file
            item = [file, filePath.is_file(), stripStrName(str(filePath))]
            self.contentLst.append(item)

    def __prepareMenu__(self):
        self.menu = ConsoleMenu("TDDRealm is C++ unit test framework.",
                                "Choose test packages configuration file.",
                                show_exit_option=False)
        exit = ExitItem("Auf wiedersehen!!", menu=None)
        self.menu.append_item(exit)
        for item in self.contentLst:
            strTxt = "%s exists( %s )" % (item[0], item[1])
            fileIni = Path(self.co_setups.folder) / item[0]
            pkgItem = FunctionItem(strTxt, createTestMenu, [
                                   self.co_env, fileIni])
            self.menu.append_item(pkgItem)
        pass

    def __showMenu__(self):
        if (len(self.contentLst) == 1) and (self.co_setups.showMenuEvenForOneSetup == False):
            print('Calling testmenu is currently not implemented.')
            filePath = Path(self.co_setups.folder) / self.contentLst[0][0]
            createTestMenu(self.co_env, filePath)
            pass
        else:
            self.menu.show()
        pass
        # read content of folder
        ## load all manualy defined config files
        ## select files with correct suffix, if switch allow it
