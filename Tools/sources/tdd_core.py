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

# import os
from pathlib import Path
from consolemenu import ConsoleMenu
from consolemenu.items import ExitItem
from consolemenu.items import FunctionItem
# import testOnePkg as to
import testAllPkgs as tall
import TDDConfig


def testfnc(str_path):
    print("Hello in " + str_path)
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

# Funkcionalita:
# 1) Vycist konfiguracni soubory a vytvorit globalni promenne
# 2) Kontrola obsahu testovaciho adresare -> vytorit seznam
# 3) Schopnost spustit jednotlive testy
# 4) Spustit vicero testu najednou
# 5) Lizard, cppcheck, clang-formater
# 6) Complete package statistika

# Zde by mely byt nacteny promenne ze souboru(v budoucnu)


# mainConfig = TDDConfig.readMainConfigFileOrUseDefault("project.ini")
assert Path("project.ini").exists(), "Unexisting config file: %s." % (
                                        "project.ini")
mainConfig = TDDConfig.CMainConfig("project.ini")

str_testPackagesPath = mainConfig.co_pkg.str_testpath
str_testPackageSuffix = mainConfig.co_pkg.str_testfldr_suffix
len_tpkgS = len(str_testPackageSuffix)

path_dir = Path(str_testPackagesPath).glob("*_Tpkg")
dir_lst = [folder for folder in path_dir if folder.is_dir()]

lst_testDir = []
for dir in dir_lst:
    strDir = str(dir.stem)

    if (strDir[-len_tpkgS:] == str_testPackageSuffix):
        lst_testDir.append(strDir)
    # print(strDir)

# Create the menu
menu = ConsoleMenu("Main - TDDR",
                   "TDDRealm is C++ unit test framework.",
                   show_exit_option=False)


exit = ExitItem("Auf wiedersehen!!", menu=None)
menu.append_item(exit)

# A FunctionItem runs a Python function when selected
AllTestMinimized_item = FunctionItem("Run all tests(minimized)",
                                     tall.tests_minimized,
                                     [lst_testDir, mainConfig])
menu.append_item(AllTestMinimized_item)

AllTest_item = FunctionItem("Run all tests",
                            tall.tests,
                            [lst_testDir, mainConfig])
menu.append_item(AllTest_item)

for testDir in lst_testDir:
    # testItem = FunctionItem("Test " + testDir[:-len_tpkgS],
    #                        to.testPkg,
    #                        [testDir, mainConfig])
    testItem = FunctionItem("Test " + testDir[:-len_tpkgS],
                            tall.testOnePkg,
                            [testDir, mainConfig])
    menu.append_item(testItem)


# Finally, we call show to show the menu and allow the user to interact
menu.show()
