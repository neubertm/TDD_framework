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

# =============================================================================
#  Header
# =============================================================================

import os
import sys
import subprocess
from pathlib import Path
import re


# Ideas
# Common, Universal
#   automock
#   cmake
#   clang features
#   clang as compiler

# =============================================================================
#  Public Functions
# =============================================================================

def log(b_value=True):
    Shell.isVerbose = b_value

def include(cmd_name: str):
    pass

def prepare(cmd: str):
    return Shell(cmd)

# =============================================================================
#  Shell - Public
# =============================================================================

class Shell:
    isVerbose = False

    def __init__(self, cmd):
        self.isGettingOuput = False
        self.isCheckingFail = False
        self.TypeOfOuput = None
        self.out = ""
        if isinstance(cmd, str):
            self.cmd = cmd.split(" ")
        elif isinstance(cmd, list):
            self.cmd = cmd
        else:
            raise BaseException("Invalid type of parameter, only string or list")
        self.chroot = "./"



    def run(self):
        # Verbose
        if Shell.isVerbose == True:
            print(self.cmd)

        # open the process
        proc = subprocess.Popen(self.cmd, cwd=self.chroot, stdout=subprocess.PIPE)
        #stdout, stderr = fp.communicate()

        # read the stdout
        if self.TypeOfOuput == "str":
            self.out = ""
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                self.out += line.decode("UTF-8")

        if self.TypeOfOuput == "list":
            self.out = []
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                self.out.append(line.decode("UTF-8"))
        else:
            proc.communicate()

        # check if the command failed
        if self.isCheckingFail:
            code = proc.returncode
            if code != 0:
                raise BaseException("ERROR")

        return self.out

    def outAsStr(self):
        self.isGettingOuput = True
        self.TypeOfOuput = "str"
        return self

    def outAsList(self):
        self.isGettingOuput = True
        self.TypeOfOuput = "list"
        return self

    def checkFail(self):
        self.isCheckingFail = True

    def cd(self, path: str):
        self.chroot = path
        return self


# =============================================================================
#  Where Command - Public
# =============================================================================

class where:
    @staticmethod
    def run(cmd_name):
        if sys.platform == "windows":
            ret = Shell(["where", cmd_name]).readlines()
        else:
            ret = Shell(["whereis", cmd_name]).readlines()
            ret = ret[0].split(' ')[1]
        return ret


# =============================================================================
#  CMake Command - Public
# =============================================================================

class CMake:
    def __init__(self, build_path, cmake_generator_list=[]):
        self.build_path = Path(build_path)
        os.makedirs(build_path, exist_ok = True)
        self.cmake_generator = self.checkGeneratorAvaliable(cmake_generator_list)
        print("Makefile generator:", self.cmake_generator)

    def prepare(self, cmakelists_path, *options):
        makefile_path = Path(self.build_path) / "Makefile"
        if makefile_path.exists():
            return;
        print(options)

        op_cmakeLst = ["cmake"
            , "-S", Path(cmakelists_path)
            , "-B", self.build_path
            , "-G", self.cmake_generator
        ] + list(options)
        Shell(op_cmakeLst).run()

    def make(self):
        Shell("make").cd(self.build_path).run()

    def test(self):
        Shell("make test").cd(self.build_path).run()

    def install(self):
        Shell("make install").cd(self.build_path).run()

    def path():
        ret = where.exec("cmake")
        print(ret)

    def checkGeneratorAvaliable(self, generators: list) -> str:
        text = Shell("cmake --help").outAsStr().run()
        retval = None
        for name in generators:
            query = re.search(name+".* =", text)
            if query != None:
                #print(query.)
                retval = query.group(0).split("=")[0].strip()
                break

        if retval == None:
            raise BaseException("No CMake generator avaliable in this list")

        return retval


# =============================================================================
#  Convert the Module for CallableModule
# =============================================================================

#class CallableModule:
#    def __call__(self, cmd: str):
#        return Shell(cmd)

#sys.modules[__name__].__class__ = CallableModule
