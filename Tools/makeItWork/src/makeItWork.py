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

import os
import sys
import subprocess
from pathlib import Path
from shutil import rmtree # shutil has been included in Python since before 2.3.

toolsFldr = "Tools"
rootLibsFldr = os.path.join(toolsFldr, "testlibs")
tmp_folder = os.path.join(toolsFldr, "makeItWorkTmp")


# =============================================================================
#  Functions to install the Python Packages
# =============================================================================

def termination():
    # input("Press any key to finish.")
    print("Script will be terminated.")
    exit(-1)


def checkPathOrCreate(head):
    path = ""
    folder_list = head.split(os.sep)
    for folder in folder_list:
        path = os.path.join(path, folder)
        if not os.path.exists(path):
            os.mkdir(path)


def checkPathToFile_orCreate(fileName):
    head, tail = os.path.split(fileName)

    if head:
        checkPathOrCreate(head)


def installPythonPackageCheckResult(outFile):
    pipData = ""
    with open(outFile, "r") as File:
        pipData = File.read()
    pipLines = pipData.split("\n")
    pipLines = [line for line in pipLines if line]
    result_lst = pipLines[-1].split(" ")

    # installed
    if result_lst[0] == "Successfully" and result_lst[1] == "installed":
        return(True)

    for line in pipLines:
        lineSplited = line.split(" ")
        if (not lineSplited[0] == "Requirement") or \
           (not lineSplited[1] == "already") or \
           (not lineSplited[2] == "satisfied:"):
            return(False)
        return(True)
    return (False)


def installPythonPackage(packageName):
    print("Installing python package :", packageName)
    bRetVal = False
    pip_out = os.path.join(tmp_folder, "pipinstall.out")
    pip_err = os.path.join(tmp_folder, "pipinstall.err")
    checkPathToFile_orCreate(pip_out)

    op_pip = "pip install " + packageName
    op_pip += "  > " + pip_out
    op_pip += " 2> " + pip_err

    os.system(op_pip)

    bRetVal = installPythonPackageCheckResult(pip_out)
    if not bRetVal:
        print("pip install ", packageName, " failed")
        termination()


# =============================================================================
#  Script to install the missed python packages
# =============================================================================

# Section of trying include packages when it failed. We try it install.
# # Section of includes important for this script them self.
try:
    import requests
except ImportError:
    installPythonPackage("requests")
    import requests

try:
    import subprocess
except ImportError:
    installPythonPackage("subprocess")
    import subprocess

try:
    import readchar
except ImportError:
    installPythonPackage("readchar")
    import readchar

try:
    import colorama
    from colorama import Fore, Style
except ImportError:
    installPythonPackage("colorama")
    import colorama
    from colorama import Fore, Style

try:
    import keyboard
except ImportError:
    installPythonPackage("keyboard")
    import keyboard

try:
    import pathlib
except ImportError:
    installPythonPackage("pathlib")
    import pathlib

# NOTE: this has to be on beginning, but at first we have to load module

try:
    import zipfile
except ImportError:
    installPythonPackage("zipfile")
    import zipfile

try:
    import shutil
except ImportError:
    installPythonPackage("shutil")
    import shutil

# # Section of includes important for TDD framework
try:
    import consolemenu
except ImportError:
    installPythonPackage("console-menu")
    import consolemenu

try:
    import configparser
except ImportError:
    installPythonPackage("configparser")
    import configparser

try:
    import threading
except ImportError:
    installPythonPackage("threading")
    import threading

try:
    import readchar
except ImportError:
    installPythonPackage("readchar")
    import readchar

try:
    import time
except ImportError:
    installPythonPackage("time")
    import time

try:
    import filecmp
except ImportError:
    installPythonPackage("filecmp")
    import filecmp

try:
    import tabulate
except ImportError:
    installPythonPackage("tabulate")
    import tabulate

try:
    import functools
except ImportError:
    installPythonPackage("functools")
    import functools

try:
    import re
except ImportError:
    installPythonPackage("re")
    import re

try:
    import lizard
except ImportError:
    installPythonPackage("lizard")
    import lizard


try:
    import multimetric
except ImportError:
    installPythonPackage("multimetric")
    import multimetric


def del_folder(path):
    for sub in path.iterdir():
        if sub.is_dir():
            del_folder(sub)
        else:
            sub.unlink()
    path.rmdir()

# =============================================================================
#  SoftwareAndTools
# =============================================================================

class SoftwareAndTools:
    str_appName: str
    str_pathInSystem: str
    str_installerSuff: str
    str_installerRoot: str
    str_installerFullName: str

    def __init__(self, str_name, fnc_checkVer=None, str_linkInstaller=""):
        self.str_appName = str_name
        self.str_pathInSystem = ""
        self.fnc_checkVer = fnc_checkVer
        self.str_linkInstaller = str_linkInstaller
        self.str_installerRoot = "_installer"
        if str_linkInstaller:
            self.str_installerSuff = str_linkInstaller.split("/")[-1] \
                                                      .split(".")[-1]
        else:
            self.str_installerSuff = "exe"
        self.str_installerFullName = ''.join((str_name,
                                              self.str_installerRoot,
                                              ".",
                                              self.str_installerSuff))

        pass

    def checkInPath(self):
        return(self.fnc_checkVer())

    def check(self):
        status, path = self.checkInPath()
        if not status:
            print(self.str_appName, " is not in system path.")
            str_question = "Is " + self.str_appName + " installed in system?"
            if questionYesNo(str_question):
                status, path = self.findInSystem()
                if status:
                    print(self.str_appName, " found in this path: ", path)
                    status, path = self.fnc_checkVer(path)
                    os.environ['PATH'] = str(Path(path).parent) + ';' + os.environ['PATH']
        return(status, path)

    def findInSystem(self):
        bRetVal, file_lst = findApp(self.str_appName)
        #print("Finding: %s(%r)" % (self.str_appName, bRetVal) )
        if bRetVal:
            self.str_pathInSystem = file_lst[0]

        return(bRetVal, self.str_pathInSystem)

    def downloadInstalator(self):
        bRetVal = False
        if questionYesNo("Do you want install " + self.str_appName + "?"):
            installerName = self.str_installerFullName
            fileName = os.path.join("Tools", "Downloads", installerName)
            print("Downloading: ", self.str_appName)
            bRetVal = downloadUrlToFile(self.str_linkInstaller, fileName)
            if bRetVal:
                print(Fore.GREEN + ("Downloading of " + self.str_appName
                                    + " is successful."))
            else:
                print(Fore.RED + "Downloading of " + self.str_appName
                      + " failed.")
                print(Fore.BLUE + "Try to repeate or install manually.")
        else:
            print("Install " + self.str_appName + " manualy.")
            termination()

        return(bRetVal)

    def install(self):
        print("Trying to install: ", self.str_appName)
        installerName = self.str_installerFullName
        fileName = os.path.join("Tools", "Downloads", installerName)

        Inst_out = os.path.join(tmp_folder, self.str_appName + "Inst.out")
        Inst_err = os.path.join(tmp_folder, self.str_appName + "Inst.err")

        op_inst = fileName

        op_inst += "  > " + Inst_out
        op_inst += " 2> " + Inst_err
        # print(op_inst)
        os.system(op_inst)
        print("Instal finished. Going to check if installed properly.")
        return(self.check())

    def checkDownloadInstall(self):
        appname = self.str_appName.upper()
        print(Fore.YELLOW + appname + " check:")
        status, path = self.check()
        # print(status, " & ", path)

        if (not status):
            status = self.downloadInstalator()
            if status:
                status = self.install()
        else:
            self.str_pathInSystem = path

        if not status:
            print(Fore.RED + (appname
                              + " is still missing. "
                              + "Script will be terminated!"))
            termination()


# =============================================================================
#  TestingLibrary
# =============================================================================

class TestingLibrary():
    # str_libName : str
    # str_url : str
    # str_downloadedFile : str
    # b_isDownloaded : bool
    # str_pathToUnpackedSrc : str

    def __init__(self, str_libName, str_url, fnc_copyLib=None):
        self.str_libName = str_libName
        self.str_url = str_url
        self.b_isDownloaded = False
        self.str_downloadedFile = ""
        self.str_pathToUnpackedSrc = ""
        self.fnc_copyLib = fnc_copyLib

    def makeItReady(self, compiler="mingw"):
        bRetVal = self.download()

        if not bRetVal:
            termination()

        destFldr = os.path.join(tmp_folder, "libs")
        bRetVal = self.unpack(destFldr)

        if not bRetVal:
            termination()

        bRetVal = self.build(compiler)

    def download(self):
        print(Fore.YELLOW + "Downloading " + self.str_libName + " library.")
        bRetVal = False
        if questionYesNo("Do you want download " + self.str_libName + "?"):
            libPkgName = self.str_url.split("/")[-1]
            self.str_downloadedFile = os.path.join("Tools", "Downloads",
                                                   libPkgName)
            print("Downloading: ", self.str_libName)
            bRetVal = downloadUrlToFile(self.str_url, self.str_downloadedFile)
            if bRetVal:
                print(Fore.GREEN + "Downloading of " + libPkgName
                      + " is successful.")
            else:
                print(Fore.RED + "Downloading of " + libPkgName
                      + " failed.")
        else:
            print("Download, compile and set properly " + self.str_libName
                  + " manualy.")

        self.b_isDownloaded = bRetVal
        return(bRetVal)

    def unpack(self, destFolder):
        bRetVal = False
        if not self.b_isDownloaded:
            print(Fore.RED + "Cant unpack library wasnt downloaded.")
            return(bRetVal)

        print(Fore.YELLOW + "Extracting " + self.str_libName + " library.")
        checkPathOrCreate(destFolder)
        try:
            with zipfile.ZipFile(self.str_downloadedFile, 'r') as zipObj:
                # print(zipObj.infolist()[0].filename)
                zipObj.extractall(destFolder)
                bRetVal = True
                self.str_pathToUnpackedSrc = destFolder
                print(Fore.GREEN + "Extraction of " + self.str_libName
                      + " successful.")
        except zipfile.BadZipFile:
            print(Fore.RED + "Compressed file " + self.str_downloadedFile
                  + " is corrupted.")

        return(bRetVal)

    def build(self, compiler="mingw"):
        bRetVal = False
        print(Fore.YELLOW + Style.BRIGHT + "Building lib(" + self.str_libName
              + ") with " + compiler)
        dirLst = os.listdir(self.str_pathToUnpackedSrc)

        if not dirLst:
            return (bRetVal)
        folder = ""
        for dir in dirLst:
            if self.str_libName in dir:
                folder = dir
                break

        if not folder:
            print(Fore.RED + "Source folder for library(" + self.str_libName
                  + ") not found.")
            termination()

        sourceFolder = os.path.join(self.str_pathToUnpackedSrc, folder)
        buildFolder = os.path.join(sourceFolder, compiler + "_build")
        checkPathOrCreate(buildFolder)

        print(Fore.YELLOW + "  CMake")
        self.__cmake__(sourceFolder, buildFolder, compiler)
        print(Fore.YELLOW + "  Make")
        self.__make__(buildFolder, compiler)
        print(Fore.YELLOW + "  Copy to correct position.")
        self.__copyLib__(compiler, sourceFolder)

    def copy2position(self, compiler):
        pass

    def __cmake__(self, sFldr, bFldr, compiler="mingw"):
        cmakeSwitcher = {
            "mingw": "\"MinGW Makefiles\"",
            "msvc": "\"NMake Makefiles\"",
            "gnu": "\"Unix Makefiles\""
        }
        op = "cmake "  # call cmake binary
        op += " -S " + sFldr  # root folder (position of cmakefile)
        op += " -B " + bFldr  # build folder
        op += " -G "  # compiler dependent

        #print ("Compiler name: ",compiler)
        if cmakeSwitcher.get(compiler, ""):
            op += cmakeSwitcher.get(compiler)
        else:
            print(Fore.RED + "Unknown cmake switch: " + compiler)
            termination()

        op += " -DCMAKE_CXX_OUTPUT_EXTENSION_REPLACE=ON"
        op += " >  " + os.path.join(bFldr, "cmake.out")  # stdout
        op += " 2> " + os.path.join(bFldr, "cmake.err")  # stderr

        # print(op)
        os.system(op)

    def __make__(self, bFldr, compiler="mingw"):
        makeTools = {
            "mingw": "mingw32-make",
            "msvc": "nmake",
            "gnu": "make"
        }

        if makeTools.get(compiler, ""):
            op = makeTools.get(compiler)
        else:
            print(Fore.RED + "Unknown compiler setting.")
            termination()

        op += " -j4 "

        if self.str_libName == "cpputest":
            op += " CppUTest CppUTestExt "

        op += " -C " + bFldr
        op += " >  " + os.path.join(bFldr, "makefile.out")  # stdout
        op += " 2> " + os.path.join(bFldr, "makefile.err")  # stderr
        # print(op)
        os.system(op)

    def __copyLib__(self, compiler, srcFldr):
        if None is self.fnc_copyLib:
            print(
                Fore.RED
                + "Function for copy library to correct possition is not defined!")
            return
        self.fnc_copyLib(compiler, srcFldr)

# =============================================================================
#  Util Functions
# =============================================================================

def questionYesNo(QuestionOfText):
    bRetVal = False
    while(1):
        answer = input(QuestionOfText + " [yes(y)|no(n)]:")
        if answer == "yes" or answer == 'y':
            bRetVal = True
            break
        elif answer == "no" or answer == 'n':
            break
        else:
            print("Incorrect input value.")
    return (bRetVal)


def find_file_all(fileName, search_path):
    result = []
    for root, dir, files in os.walk(search_path):
        if fileName in files:
            result.append(os.path.join(root, fileName))
    return(result)


def find_files_all(fileNames, search_path):
    result = []
    for root, dir, files in os.walk(search_path):
        for fName in fileNames:
            if fName in files:
                result.append(os.path.join(root, fName))
    return(result)


def find_file_firstOnly(fileName, search_path, exclude_fldrs=[]):
    # print(fileName, " ", search_path)
    result = []
    for root, dirs, files in os.walk(search_path):
        if exclude_fldrs:
            dirs[:] = [d for d in dirs if d not in exclude_fldrs]
        if fileName in files:
            result.append(os.path.join(root, fileName))
            break
    return(result)


def find_files_firstOnly(fileNames, search_path):
    result = []
    locFileNames = fileNames
    for root, dir, files in os.walk(search_path):
        if locFileNames:
            for fName in locFileNames:
                if fName in files:
                    result.append(os.path.join(root, fName))
                    locFileNames.remove(fName)
        else:
            break
    return(result)


def python_version():
    return (sys.version.split(" ")[0])


def checkPythonVersion():
    bRetVal = False
    pVer = python_version()
    pVerSplit = pVer.split(".")
    if pVerSplit[0] == "3":
        print(Fore.GREEN + "Python version is correct: " + pVer)
        bRetVal = True
    else:
        print(Fore.GREEN + "Python version is incorrect: " + pVer)

    return(bRetVal)


def checkPipVersion():
    bRetVal = False
    pipVer = ""
    pip_out = os.path.join(tmp_folder, "pip.out")
    pip_err = os.path.join(tmp_folder, "pip.err")
    checkPathToFile_orCreate(pip_out)

    op_pip = "pip --version "
    op_pip += "  > " + pip_out
    op_pip += " 2> " + pip_err

    os.system(op_pip)
    with open(pip_out, "r") as File:
        pipData = File.read()
        pipInfo = pipData.split(" ")
        if pipInfo[0] == "pip":
            bRetVal = True
            pipVer = pipInfo[1]
    if bRetVal is True:
        print(Fore.GREEN + "Pip ok. Version: " + pipVer)
    else:
        print(Fore.RED + "Error: Pip not found.")
    return(bRetVal)


def checkCppcheck(Path=""):
    toolName = "cppcheck"
    strVersion = ""
    argVersion = " --version "
    bRetVal = False
    retPath = ""
    out = os.path.join(tmp_folder, toolName + ".out")
    err = os.path.join(tmp_folder, toolName + ".err")

    if not Path:
        op_tool = toolName
    else:
        op_tool = "\"" + Path + "\""

    op_tool += argVersion
    op_tool += "  > " + out
    op_tool += " 2> " + err

    # print(op_tool)
    os.system(op_tool)
    with open(out, "r") as File:
        Data = File.read()
        Info = Data.split("\n")[0].split(" ")
        if Info[0].upper() == "CPPCHECK":
            bRetVal = True
            strVersion = Info[1]
    if bRetVal is True:
        print(Fore.GREEN + toolName.upper() + " ok. Version: " + strVersion)
        if not Path:
            retPath = os.popen("where " + toolName).readlines().split("\n")[0]
        else:
            retPath = Path

    return(bRetVal, retPath)

def checkCppUMockGen(Path=''):
    bRetVal = False
    #print('checking CppUMockGen')
    toolName = "CppUMockGen"
    strVersion = ""
    argVersion = "--version"
    bRetVal = False
    retPath = ""
    out = os.path.join(tmp_folder, toolName + ".out")
    err = os.path.join(tmp_folder, toolName + ".err")

    op_lst = []
    if not Path:
        op_tool = toolName
    else:
        op_tool = Path
    op_lst.append(op_tool)

    op_tool += argVersion
    op_lst.append(argVersion)

    op_tool += "  > " + out
    op_lst.append(">")
    op_lst.append(out)


    op_tool += " 2> " + err
    op_lst.append("2>")
    op_lst.append(err)

    # print(op_tool)
    # os.system(op_lst)
    tCode = subprocess.call(op_lst,shell=True)
    #print(op_lst)
    #print('return code =%i' % tCode)

    if (0 == tCode):
        bRetVal = True
        with open(out, 'r') as File:
            Data = File.read()
            Info = Data.split('\n')[0].split(' ')
            if (Info[0] == 'CppUMockGen') and (Info[1] == 'v0.4'):
                bRetVal = True
                print('%s is ok. Version: %s' % (toolName, Info[1]) )

    if (-1073741515 == tCode) or (3221225781 == tCode):
        bRetVal = True
        print(Fore.MAGENTA + '%s exists. But clang is not in path yet.' % (toolName) )

    if (bRetVal is True):
        if not Path:
            retPath = os.popen(
                "where " + toolName).readlines()[0].split("\n")[0]
        else:
            retPath = Path


    return(bRetVal, retPath)

def checkCMake(Path=""):
    toolName = "cmake"
    argVersion = " --version "
    bRetVal = False
    strVersion = ""
    retPath = ""
    out = os.path.join(tmp_folder, toolName + ".out")
    err = os.path.join(tmp_folder, toolName + ".err")

    if not Path:
        op_tool = toolName
    else:
        op_tool = "\"" + Path + "\""

    op_tool += argVersion
    op_tool += "  > " + out
    op_tool += " 2> " + err

    # print(op_cmake)
    os.system(op_tool)
    with open(out, "r") as File:
        Data = File.read()
        Info = Data.split("\n")[0].split(" ")
        if Info[0] == "cmake":
            bRetVal = True
            strVersion = Info[2]
    if bRetVal is True:
        print(Fore.GREEN + toolName + " ok. Version: " + strVersion)
        if not Path:
            retPath = os.popen(
                "where " + toolName).readlines()[0].split("\n")[0]
        else:
            retPath = Path

    return(bRetVal, retPath)


def checkGnuCompiler(defName, binPath):
    argVersion = " --version "
    bRetVal = False
    retPath = ""
    out = os.path.join(tmp_folder, defName + ".out")
    err = os.path.join(tmp_folder, defName + ".err")

    if not binPath:
        op_bin = defName
    else:
        op_bin = "\"" + binPath + "\""

    op_bin += argVersion
    op_bin += "  > " + out
    op_bin += " 2> " + err

    os.system(op_bin)

    with open(err, "r") as File:
        errData = File.read()
        if not errData:
            bRetVal = True

    if bRetVal:
        with open(out, "r") as File:
            outData = File.read()
            print(Fore.GREEN + outData.split("\n")[0])
        if not binPath:
            retPath = os.popen("where " + defName).readlines()[0][:-1]
            print(retPath)
            # termination()
        else:
            retPath = binPath
    return(bRetVal, retPath)


def checkGcc(binPath=""):
    defName = "gcc"
    return(checkGnuCompiler(defName, binPath))


def checkClang(binPath=""):
    defName = "clang"
    return(checkGnuCompiler(defName, binPath))


def findApp(AppName):
    bRetVal = False
    exclude_lst = []
    file_list = []
    Name = AppName

    if os.name == 'nt':
        Name += ".exe"

        searchFolder = "Program Files"
        file_list = find_file_firstOnly(
            Name, os.path.join("c:\\", searchFolder))
        if file_list:
            bRetVal = True
        else:
            exclude_lst.append(searchFolder)

        if not bRetVal:
            searchFolder = "Program Files (x86)"
            file_list = find_file_firstOnly(
                Name, os.path.join(
                    "c:\\", "Program Files (x86)"))
            if file_list:
                bRetVal = True
            else:
                exclude_lst.append(searchFolder)

        if not bRetVal:
            exclude_lst.append("Windows")
            file_list = find_file_firstOnly(Name, "c:\\", exclude_lst)
            if file_list:
                bRetVal = True

        if not bRetVal:
            file_list = find_file_firstOnly(Name, "d:\\")
            if file_list:
                bRetVal = True
    else:
        file_list = find_file_firstOnly(Name, "/")
        if file_list:
            bRetVal = True

    return(bRetVal, file_list)


def downloadUrlToFile(url, fileName):
    bRetVal = False
    checkPathToFile_orCreate(fileName)
    # r = requests.get(url, allow_redirects=True)
    # if r.content :
    #    open(fileName, 'wb').write(r.content)
    #    bRetVal = True
    print(url)
    with open(fileName, "wb") as f:
        # response = requests.get(url,stream=True,verify=False)
        try:
            response = requests.get(url, stream=True)
        except requests.exceptions.SSLError:
            print("SSL download error. Trying to download without SSL.")
            response = requests.get(url, stream=True, verify=False)

        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]%iMB" % (
                    '=' * done, ' ' * (50 - done), total_length / (1024 * 1024)))
                sys.stdout.flush()
            sys.stdout.write("\n")
            sys.stdout.flush()
            bRetVal = True

    if not bRetVal:
        if os.path.getsize(fileName):
            bRetVal = True

    return(bRetVal)


def downloadLibrary(libName, libUrl):
    bRetVal = False
    if questionYesNo("Do you want download " + libName + "?"):
        libPkgName = libUrl.split("/")[-1]
        fileName = os.path.join("Tools", "Downloads", libPkgName)
        print("Downloading: ", libName)
        bRetVal = downloadUrlToFile(libUrl, fileName)
        if bRetVal:
            print(
                (Fore.GREEN
                 + "Downloading of "
                 + libPkgName
                 + " is successful."))
        else:
            print(Fore.RED + "Downloading of " + libPkgName + " failed.")
    else:
        print("Download, compile and set properly " + libName + " manualy.")
        termination()

    return(bRetVal)


def unpackFile(packedFile, destFolder):
    # bRetVal = False
    with zipfile.ZipFile(packedFile, 'r') as zipObj:
        # zipObj.printdir()
        print("Extracting all file now...")
        zipObj.extractall(destFolder)


def copyCppUTestLib(compiler, srcFldr):
    cpputestFldr = os.path.join(rootLibsFldr, "cpputest")
    # includeFldr = os.path.join(cpputestFldr,"include")
    staticLibFldr = os.path.join(cpputestFldr, compiler)
    buildFldr = os.path.join(srcFldr, compiler + "_build")
    # checkPathOrCreate(includeFldr)
    checkPathOrCreate(staticLibFldr)

    LibCpp = os.path.join(buildFldr, "src", "CppUTest", "libCppUTest.a")
    LibCppE = os.path.join(buildFldr, "src", "CppUTestExt", "libCppUTestExt.a")
    libLst = [LibCpp, LibCppE]
    for lib in libLst:
        if os.path.exists(lib):
            # print( "copy ", lib, " => ", staticLibFldr)
            shutil.copy(lib, staticLibFldr)
        else:
            print(Fore.RED + "Error trying to copy unexisting file: " + lib)

    srcF = os.path.join(srcFldr, "include")
    dstF = os.path.join(cpputestFldr, "include")
    if os.path.exists(dstF):
        try:
            shutil.rmtree(dstF)
        except OSError as e:
            print(Fore.RED + "Error: %s : %s" % (dstF, e.strerror))
    # print( "copytree ", srcF, " => ", dstF)
    pathDst = pathlib.Path(dstF)
    if pathDst.exists():
        del_folder(pathDst)
    # path.mkdir()
    shutil.copytree(srcF, dstF)


def createCfgFromTemplate(sfDic):
    # print(sfDic)
    bckpFile = os.path.join(toolsFldr, "envPath_bckp.ini")
    newIniFile = "envPath.ini"
    Data = ""
    with open(bckpFile, "r") as File:
        Data = File.read()

    switcher = {
        "cmake": "CMAKE_SYSTEM_PATH",
        "msvc": "MSVC_SYSTEM_PATH",
        "gcc": "MINGW_SYSTEM_PATH",
        "mingw": "MINGW_SYSTEM_PATH",
        "cppcheck": "CPPCHECK_SYSTEM_PATH",
        "clang": "CLANG_SYSTEM_PATH",
        "CppUMockGen": "CPPUMOCKGEN_SYSTEM_PATH"
    }
    for key in sfDic:
        print(key, switcher[key], sfDic[key])
        Data = Data.replace(switcher[key], sfDic[key])

    with open(newIniFile, "w") as File:
        File.write(Data)


def updateConfigFile(sfDic):
    iniFile = pathlib.Path('envPath.ini')
    if iniFile.is_file():
        print("Project ini file exists. Do you want to create the new one?")
        if questionYesNo("Should i delete old and create the new one?"):
            createCfgFromTemplate(sfDic)
            pass
        else:
            return
    else:
        print("Project ini file not found?!! Creating new one.")
        createCfgFromTemplate(sfDic)

# =============================================================================
#  Log Functions
# =============================================================================

def printError(text, *args):
    print(Fore.RED + text, *args)
    termination()

def printWarn(text, *args):
    print(Fore.YELLOW + text, *args)

def printInfo(text, *args):
    print(Fore.MAGENTA + text, *args)

def printOk(text, *args):
    print(Fore.GREEN + text, *args)

def printAlert(text, *args):
    print(Fore.RED + text, *args)

# =============================================================================
#  Main
# =============================================================================

colorama.init(autoreset=True)
printInfo("Finding or installing & checking important tools.")

# Check python version and if it is installed and path is set or in variable
printWarn("Python check version:")
ST_python = SoftwareAndTools("python", checkPythonVersion)
if not ST_python.checkInPath():
    termination()

# Check that pip is installed in path
printWarn("Python pip check version:")
ST_pip = SoftwareAndTools("pip", checkPipVersion)
if not ST_pip.checkInPath():
    termination()

ST_list = []

# Check if CMake is installed in path
cmakeLink = ('https://github.com/Kitware/CMake/releases/download/v3.20.3/'
             + 'cmake-3.20.3-windows-x86_64.msi')
ST_cmake = SoftwareAndTools("cmake", checkCMake, cmakeLink)
ST_list.append(ST_cmake)
# ST_cmake.checkDownloadInstall()

# Check if gcc is installed in path
gccLink = ('https://sourceforge.net/projects/mingw-w64/files/'
           + 'Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/'
           + 'installer/mingw-w64-install.exe')
ST_gcc = SoftwareAndTools("gcc", checkGcc, gccLink)
ST_list.append(ST_gcc)
# ST_gcc.checkDownloadInstall()

# check clang
clangLink = ("https://github.com/llvm/llvm-project/releases/download/"
             + "llvmorg-12.0.0/LLVM-12.0.0-win64.exe")
ST_clang = SoftwareAndTools("clang", checkClang, clangLink)
ST_list.append(ST_clang)

# check cppcheck
cppcheckLink = ("https://github.com/danmar/cppcheck/releases/download/"
                + "2.4.1/cppcheck-2.4.1-x64-Setup.msi")
ST_cppcheck = SoftwareAndTools("cppcheck", checkCppcheck, cppcheckLink)
ST_list.append(ST_cppcheck)

cppumockgenLink = ('https://github.com/jgonzalezdr/CppUMockGen/releases/'
                   + 'download/v0.4/Install.CppUMockGen.0.4.x64.exe')
ST_cppumockgen = SoftwareAndTools('CppUMockGen', checkCppUMockGen, cppumockgenLink)
ST_list.append(ST_cppumockgen)

libCppUTest = TestingLibrary(
    'cpputest',
    ("https://github.com/cpputest/cpputest/releases/download/"
     + "v3.8/cpputest-3.8.zip"),
    copyCppUTestLib)

# Rebuild Command
if len(sys.argv) > 1 and sys.argv[1] == "rebuild":
    # get the name of config file
    configfile = './envPath.ini'
    if len(sys.argv) > 2:
        configfile = sys.argv[2]

    # parse the configuration file
    parser = configparser.ConfigParser()
    if not Path(configfile).exists():
        printError("File {} not found".format(configfile))
    parser.read(configfile)

    # Delete old tmp_folder/libs
    tmp_lib_path = Path(tmp_folder) / "libs"
    if tmp_lib_path.exists():
        printAlert("Deleting the old temporary folder {}".format(tmp_lib_path))
        rmtree(tmp_lib_path)

    try:
        # get the GCC Path
        gcc_path = parser["MINGW"]["ENV_CONFIG_SCRIPT"]
        printInfo("using compiler in {}".format(gcc_path))
        os.environ['PATH'] = gcc_path + ';' + os.environ['PATH']

        # get the CMake Path
        cmake_path = parser["CMAKE"]["ENV_CONFIG_SCRIPT"]
        printInfo("using cmake in {}".format(cmake_path))
        os.environ['PATH'] = cmake_path + ';' + os.environ['PATH']

        # check CMake and install the libCppUTest
        libCppUTest.makeItReady()
        termination()

    except KeyError as field:
        print("Parameter ",field," not found in the file envPath.ini")
        termination()


# Normal Execution
for sw in ST_list:
    sw.checkDownloadInstall()

printOk("Minimal toolchain is complete.\n")

printInfo("Downloading unpacking & compiling testing libraries.")

# adding toolchain to the local path
for sw in ST_list:
    head, tail = os.path.split(sw.str_pathInSystem)
    os.environ['PATH'] = head + ";" + os.environ['PATH']

swPathDict = {sw.str_appName: os.path.split(sw.str_pathInSystem)[
    0] for sw in ST_list}
print("Check inifile.")
updateConfigFile(swPathDict)

libGTest = TestingLibrary(
    'googletest',
    "https://github.com/google/googletest/archive/refs/heads/master.zip")

libCppUTest.makeItReady("mingw")
# libGTest.makeItReady("mingw")


# # update configuration file according found software path

termination()
