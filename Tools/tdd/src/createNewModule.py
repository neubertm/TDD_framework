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

from TDDConfig import CTestPkgDescription
from TDDConfig import CTestConfig
from TDDConfig import CCovCfg
from TDDConfig import CStaticAnalysisCfg
from TDDConfig import CFormaterGuidelineCheckerCfg
from TDDConfig import CTestToolchainCfg
from TDDConfig import CCodeStatisticsCfg


def printout(text):
    print(text)

def get_input(text):
    return input(text)

def questionYesNo(QuestionOfText):
    bRetVal = False
    while(1):
        answer = get_input(QuestionOfText + " [yes(y)|no(n)]:")
        if answer == "yes" or answer == 'y':
            bRetVal = True
            break
        elif answer == "no" or answer == 'n':
            break
        else:
            printout("Incorrect input value.")
    return (bRetVal)


def questionWithList(QuestionOfText,list,default):
    str_RetVal = default

    str_choises = '|'.join(list)
    while(1):
        answer = get_input(QuestionOfText + " ( %s ) default[%s]:" % (str_choises, str_RetVal))
        if answer == "":
            printout('Using default value.')
            break
        elif answer in list:
            str_RetVal = answer
            break
        else:
            printout("Incorrect input value.")
    return (str_RetVal)

class CreateNewModule():
    str_SRC_FOLDER: str
    str_HEADER_FOLDER: str
    str_FRAMEWORK: str
    str_TOOLCHAIN: str
    str_LANGUAGE: str
    str_COMPONENT_NAME: str
    str_SRC_TYPE: str
    testConfig: CTestConfig
    pkgDesc: CTestPkgDescription

    def __init__(self, cTestPkgDesc: CTestPkgDescription):
        self.str_SRC_FOLDER = ''
        self.str_HEADER_FOLDER = ''
        self.str_FRAMEWORK = "cpputest"
        self.str_TOOLCHAIN = "mingw"
        self.str_LANGUAGE = 'c++'
        self.str_COMPONENT_NAME = ''
        self.str_SRC_TYPE = ''
        self.testConfig = CTestConfig()
        self.pkgDesc = cTestPkgDesc
        pass

    def setModuleConfiguration(self):
        '''
        This function create configuration for creating new module.
        Result will be definition of files, type of source code.
        Complete test configuration

        Function explanation:
        1) define what type of module we want to create. c/c++
        2) define SUT file Configuration
            a) Name, name of class or pkg
            b) Define name of files  NAME.suffix  for hdr and scr
        3) define test configuration for additional steps
        '''
        # define src folder
        ## question if user wants to create C or C++
        self.str_LANGUAGE = questionWithList("What type of code will the new module be?", ['c++','c'], 'c++')

        resLst = defineSUTFileConfiguration()

        testConfig.co_coverage = defineCoverageCfg()

        testConfig.co_staticAnalysis = defineStatAnalysisCfg()

        testConfig.co_testToolchain = defineToolchainCfg()

        testConfig.co_codeStatistics = defineCodeStatisticsCfg()

        pass

    def createNewModule(self):
        '''
        This function create new module according  user ideas.
        1) First user define how it should look like.
        2) Create new SUT object header and source file.
        3) Create new test package folder and fill with default files and user configurations.
        '''
        setModuleConfiguration()

        createFolder_SUT()

        createFolder_TPKG()

        pass

    def defineSutFileConfiguration(self):
        '''
            Function have to create filenames, and folder where will be placed.
            Function have two arguments:
            moduleType: is string variable expected values are c,c++
            cTestPkgDesc: is folder configuration description class, used for default location of files
        '''
        fileLst = defineSutFileNames()

        folderLst = defineSutFolders()

        return [fileLst, folderLst]
        pass

    def defineSutFileNames(self):
        '''
        Function create name of files for sut. Header and Source
        1) check position of sourcefolder from configuration
        2) self.str_LANGUAGE contain type
        3) User define class name or pkg name(c-code)
        4) New file name is proposed, user can define own.
        Name of files will be stored in as attribute.
        '''
        pass

    def defineSutFolders(self):
        '''
        Function define position of sut files(header and source)
        There will be some default choise but user can define. Specific for header and source.
        HeaderFolder and SourceFolder will be stored as attribute
        '''
        pass

    def copyFilesToCorrectPositions(self, resLst):
        pass

    def defineCoverageCfg(self):
        '''
        User can define coverage configuration.
        '''
        pass

    def defineStatAnalysisCfg(self):
        '''
        User can define static analysis configuration.
        '''
        pass

    def defineToolchainCfg(self):
        '''
        User can define toolchain configuration.
        But currently this choise will be disabled.
        '''
        pass

    def defineCodeStatisticsCfg(self):
        '''
        User can define complexity static configuration.
        '''
        pass
