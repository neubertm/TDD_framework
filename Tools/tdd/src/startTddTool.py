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


import sys

from pathlib import Path

from TDDConfig import CEnvCfg
from TDDConfig import CSetupsCfg

from mainMenu import MainMenu

# TODO here we need argument parser
# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

# Section loading Environment path - compilers and other important tool


def assertFilePathExists(str_filePath):
    assert Path(str_filePath).exists(), "Unexisting config file: %s." % (
                                            str_filePath)


def printoutTextWhenDefaultFileIsUsed(str_file,str_type):
    print("Not enough arguments, we expect cfg file name"
          + " for environment path.")
    print("Default name for %s config file will be used: %s" % (str_type,
                                                                str_file))


def main():
    str_envCfgFile = 'envPath.ini'
    arguments = sys.argv[1:]
    if len(arguments) > 0:
        str_envCfgFile = arguments[0]
    else:
        printoutTextWhenDefaultFileIsUsed(str_envCfgFile, 'environment')

    assertFilePathExists(str_envCfgFile)

    str_testSetupsFile = 'testSetups.ini'
    if len(arguments) > 1:
        str_testSetupsFile = arguments[1]
    else:
        printoutTextWhenDefaultFileIsUsed(str_testSetupsFile, 'setups')

    assertFilePathExists(str_testSetupsFile)

    # Reading env variables
    co_env = CEnvCfg()
    co_env.readFromFile(str_envCfgFile)

    # Reading test setups configuration file
    co_testSetups = CSetupsCfg()
    co_testSetups.readFromFile(str_testSetupsFile)
    assert co_testSetups._checkConfiguration_(
    ), "Somethin wrong in test setup file %s" % (str_testSetupsFile)

    o_menu = MainMenu(co_env, co_testSetups)
    o_menu.createAndShow()


if __name__ == "__main__":
    main()
