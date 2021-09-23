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
import os


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
