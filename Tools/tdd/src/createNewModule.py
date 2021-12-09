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

from pathlib import Path
from datetime import datetime

def copyTxtFile(str_src, str_dst):
    dest = Path('str_dst')
    src = Path('str_src')
    dest.write_text(src.read_text())


def readFileToStr(str_src: str):
    retStr = ''
    with open(str_src, 'r') as ftext:
        retStr = ftext.read()

    return retStr

def writeStringToFile(strVar,str_dst):
    with open(str_dst, 'w') as ftext:
        ftext.write(strVar)


def patchString(strVar,patchDict):
    for key in patchDict.keys():
        strVar = strVar.replace(key,patchDict[key])
    return strVar


def timeInShortString():
    now = datetime.now()
    return now.strftime('%y%m%d%H%M%S')

def assertWithText(condition, text):
    assert condition, text

def printout(text):
    print(text)

def get_input(text):
    return input(text)

def createFolder(str_folder):
    '''
        Function returning True when folder already exists or is succesfuly created.
        False - file doesnt exist and mkdir failed.
    '''
    pHeaderFolder = Path(str_folder)
    if not pHeaderFolder.is_dir():
        pHeaderFolder.mkdir(mode=666,parent=True)
        assertWithText(pHeaderFolder.is_dir(), 'Creating folder %s failed!' % (str_folder))

def processFile(str_src, str_dest, dic):
    '''
    Function copy file from src position to dest position. In file make changes when it find a key from dic rewrites by value.
    '''
    #1 open file and read to string variable
    strVar = readFileToStr(str_src)
    #2 patch string with dictionary
    patchStrVar = patchString(strVar,dic)
    #3 store string in file str_dest
    writeStringToFile(patchStrVar,str_dest)

    pass

def questionReturningPositiveInteger(questionText):
    b_confirm = False

    int_retVal = -1

    while not b_confirm:
        str_retVal = get_input(questionText + ' [Fill positive number]:')
        if str_retVal.isDecimal():
            int_retVal = int(str_retVal)
        else:
            printout('Invalid input try it again.')
            continue

        if 0 < int_retVal :
            b_confirm = questionYesNo('Confirm this value: %i' % (int_retVal))

    pass

def questionReturnString(questionText):
    '''
    Function ask user to fill string value. User have to confirm his choice.
    '''
    b_confirm = False
    str_retVal = ''

    while not b_confirm:
        str_retVal = get_input(questionText)
        b_confirm = questionYesNo('Confirm this value: %s' % (str_retVal))

    return str_retVal

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
    str_TPKG_FOLDER: str
    copyFileLst: [(str,str)]
    testConfig: CTestConfig
    pkgDesc: CTestPkgDescription

    def __init__(self, cTestPkgDesc: CTestPkgDescription):
        self.str_SRC_FOLDER = ''
        self.str_HEADER_FOLDER = ''
        self.str_SRC_FILE = ''
        self.str_HEADER_FILE = ''
        self.str_FRAMEWORK = "cpputest"
        self.str_TOOLCHAIN = "mingw"
        self.str_LANGUAGE = 'c++'
        self.str_COMPONENT_NAME = ''
        self.str_SRC_TYPE = ''
        self.str_TPKG_FOLDER = ''
        self.copyFileLst = []
        self.testConfig = CTestConfig()
        self.pkgDesc = cTestPkgDesc
        pass

    def createAndCopyFiles(self):
        self.createHeaderFile()
        self.createSourceFile()
        self.copyAndCreateTestFiles()
        self.createTestInitFile()
        self.createTestCMakefile()
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

        self.defineSutFileConfiguration()

        self.testConfig.co_coverage = self.defineCoverageCfg()

        self.testConfig.co_staticAnalysis = self.defineStatAnalysisCfg()

        self.testConfig.co_testToolchain = self.defineToolchainCfg()

        self.testConfig.co_codeStatistics = self.defineCodeStatisticsCfg()

        pass

    def createNewModule(self):
        '''
        This function create new module according  user ideas.
        1) First user define how it should look like.
        2) Create new SUT object header and source file.
        3) Create new test package folder and fill with default files and user configurations.
        '''
        self.setModuleConfiguration()

        self.createFolder_SUT()

        self.createFolder_TPKG()

        self.createAndCopyFiles()

        pass

    def defineSutFileConfiguration(self):
        '''
            Function have to create filenames, and folder where will be placed.
        '''
        # this fill self.str_SRC_FILE
        #           self.str_HEADER_FILE
        self.defineSutFileNames()

        # this fill self.str_SRC_FOLDER
        #           self.str_HEADER_FOLDER
        self.defineSutFolders()
        pass


    def createFolder_SUT(self):
        '''
            This function check if exist SUT folders. If not create them.
        '''
        createFolder(self.str_HEADER_FOLDER)
        createFolder(self.str_SRC_FOLDER)

    def createFolder_TPKG(self):
        '''
            This function create TPKG folder and subfolder.
            When TPKG folder exist, create new and push current date
            in to the name.
        '''
        pTpkgFldr = Path(self.pkgDesc.str_testpath) / (self.str_COMPONENT_NAME + self.pkgDesc.str_testfldr_suffix)

        if pTpkgFldr.is_dir():
            pTpkgFldr = Path(self.pkgDesc.str_testpath) / (self.str_COMPONENT_NAME + timeInShortString() + self.pkgDesc.str_testfldr_suffix)

        self.str_TPKG_FOLDER = str(pTpkgFldr)

        createFolder(self.str_TPKG_FOLDER)
        createFolder(str(pTpkgFldr / self.pkgDesc.str_srctestfldr))



    def defineSutFileNames(self):
        '''
        Function create name of files for sut. Header and Source
        Name of files will be stored in as attribute.
        '''
        str_srcsuff = ''
        str_headersuff = ''
        printout("New SUT object definition:")
        if self.str_LANGUAGE == 'c++':
            str_srcsuff = questionWithList('Choose suffix for src file.',['cpp', 'CPP', 'cc', 'CC'],'cpp')
            #print(str_srcsuff)
            str_headersuff = questionWithList('Choose suffix for header file.',['hpp','HPP','h','H'],'hpp')
            #print(str_headersuff)
        elif self.str_LANGUAGE == 'c':
            str_srcsuff = questionWithList('Choose suffix for src file.',['c', 'C'],'c')
            str_headersuff = questionWithList('Choose suffix for header file.',['h','H'],'h')
            pass
        else:
            assert False, 'Currently not supported source file type.'

        self.str_COMPONENT_NAME = questionReturnString('Define class/module name.')

        #print([self.str_COMPONENT_NAME,str_srcsuff])
        str_fullSrcName = '.'.join([self.str_COMPONENT_NAME,str_srcsuff])
        str_fullHeaderName = '.'.join([self.str_COMPONENT_NAME,str_headersuff])

        printout("New SUT file are: \n\t%s\n\t%s" % (str_fullHeaderName, str_fullSrcName))
        if not questionYesNo('Are names correct?'):
            str_fullHeaderName = questionReturnString('Define full name for header (name.suff).')
            str_fullSrcName = questionReturnString('Define full name for source (name.suff).')

        self.str_SRC_FILE = str_fullSrcName
        self.str_HEADER_FILE = str_fullHeaderName

    def defineSutFolders(self):
        '''
        Function define position of sut files(header and source)
        There will be some default choise but user can define. Specific for header and source.
        HeaderFolder and SourceFolder will be stored as attribute
        '''

        path_SrcFolder    = Path(self.pkgDesc.str_srcfldr) / 'src'
        path_HeaderFolder = Path(self.pkgDesc.str_srcfldr) / 'include'
        str_SrcFolder = str(path_SrcFolder)
        str_HeaderFolder = str(path_HeaderFolder)

        printout("Default folders:\n\tHeader: %s\n\tSource: %s" % (str_HeaderFolder, str_SrcFolder))
        if not questionYesNo('Are folders correct?'):
            path_HeaderFolder = Path(self.pkgDesc.str_srcfldr) / questionReturnString('Define folder name for header. (inside \"%s\" folder):' % (self.pkgDesc.str_srcfldr))
            path_SrcFolder    = Path(self.pkgDesc.str_srcfldr) / questionReturnString('Define folder name for source. (inside \"%s\" folder):' % (self.pkgDesc.str_srcfldr))
            str_SrcFolder = str(path_SrcFolder)
            str_HeaderFolder = str(path_HeaderFolder)

        self.str_SRC_FOLDER = str_SrcFolder
        self.str_HEADER_FOLDER = str_HeaderFolder

        pass


    def defineCoverageCfg(self):
        '''
        User can define coverage configuration.
        '''
        self.testConfig.co_coverage.isTurnedOn = questionYesNo('Do you want to enable coverage:')
        self.testConfig.co_coverage.uncoveredLineListLength = 0
        pass

    def defineStatAnalysisCfg(self):
        '''
        User can define static analysis configuration.
        '''

        self.testConfig.co_staticAnalysis.isTurnedOn  = questionYesNo('Do you want to enable static analysis:')
        # configuration make sence only when static analysis is turned on. we can let it in default state.
        if self.testConfig.co_staticAnalysis.isTurnedOn:
            self.testConfig.co_staticAnalysis.isLanguageDefinedBySuffix = questionYesNo('Should be language recognized from suffix:')
            self.testConfig.co_staticAnalysis.str_c_version = questionWithList('Choose version of c.',['c89', 'c99', 'c11'],'c99')
            self.testConfig.co_staticAnalysis.str_cpp_version = questionWithList('Choose version of c++.',['c++03', 'c++11', 'c++17', 'c++20'],'c++11')

        self.testConfig.co_staticAnalysis.str_tool = 'cppcheck'
        self.testConfig.co_staticAnalysis.str_ForcedLang = self.str_LANGUAGE


    def defineToolchainCfg(self):
        '''
        User can define toolchain configuration.
        But currently this choises will be disabled.
        '''
        self.testConfig.co_testToolchain.str_compiler = 'mingw'
        self.testConfig.co_testToolchain.str_testlib = 'cpputest'
        pass

    def defineCodeStatisticsCfg(self):
        '''
        User can define complexity static configuration.
        '''
        self.testConfig.co_codeStatistics.isTurnedOn = questionYesNo('Do you want to enable code quality parameters:')

        if self.testConfig.co_codeStatistics.isTurnedOn:
            self.testConfig.co_codeStatistics.isUsedTestSpecificOnly = questionYesNo('Do you want to use only test specific parameters:')
            if not self.testConfig.co_codeStatistics.isUsedTestSpecificOnly:
                self.testConfig.co_codeStatistics.isUsedStricter = questionYesNo('Do you want to use harder criteries(test vs. project):')
            self.testConfig.co_codeStatistics.int_mccabeComplex = questionReturningPositiveInteger('Define McCabe complexity')
            self.testConfig.co_codeStatistics.int_fncLength = questionReturningPositiveInteger('Define function length')
            self.testConfig.co_codeStatistics.int_paramCnt  = questionReturningPositiveInteger('Define maximum function params')
            pass
        pass

    def createHeaderFile(self):
        '''
        Function check kind of language, choose correct default template file.
        Sed correct value from configuration.
        '''
        str_src = ''
        path_src = Path('Tools') / 'defaults' / 'src_templates'
        dict = {'%COMPONENT_NAME': self.str_COMPONENT_NAME
                ,'%FILENAME': self.str_HEADER_FILE.split('.')[0]
                ,'%DATE':datetime.now().strftime('%d.%m.%y %H:%M:%S')
                ,'%YEAR':datetime.now().strftime('%Y')
                }
        if 'c++' == self.str_LANGUAGE:
            dict['%CLASSNAME'] = self.str_COMPONENT_NAME
            path_src = path_src / 'class.hpp'
        elif 'c' == self.str_LANGUAGE:
            path_src = path_src / 'c_file.h'
        else:
            assertWithText(False, 'Invalid language type.')

        str_src = str(path_src)
        str_dst = str(Path(self.str_HEADER_FOLDER) / self.str_HEADER_FILE)
        processFile(str_src,str_dst, dict)
        pass

    def createSourceFile(self):
        '''
        Copy and process source file.
        '''
        str_src = ''
        path_src = Path('Tools') / 'defaults' / 'src_templates'
        dict = {'%COMPONENT_NAME': self.str_COMPONENT_NAME
                ,'%FILENAME': self.str_SRC_FILE.split('.')[0]
                ,'%DATE':datetime.now().strftime('%d.%m.%y %H:%M:%S')
                ,'%YEAR':datetime.now().strftime('%Y')
                ,'%HEADER_FILENAME': self.str_HEADER_FILE
                }
        if 'c++' == self.str_LANGUAGE:
            dict['%CLASSNAME'] = self.str_COMPONENT_NAME
            path_src = path_src / 'class.cpp'
        elif 'c' == self.str_LANGUAGE:
            path_src = path_src / 'c_file.c'
        else:
            assertWithText(False, 'Invalid language type.')

        str_src = str(path_src)
        str_dst = str(Path(self.str_SOURCE_FOLDER) / self.str_SOURCE_FILE)
        processFile(str_src,str_dst, dict)

    def copyAndCreateTestFiles(self):
        '''
        Copy and process test.cpp and AllTests.cpp
        '''
        #0 check if exists _Tpkg/src folder, but if this is correctly called its not necessary
        pTestFldr = Path(self.str_TPKG_FOLDER) / self.pkgDesc.str_srctestfldr
        if not pTestFldr.is_dir():
            pTestFldr.mkdir()

        #1 copy AllTests.cpp
        str_allTsts = 'AllTests.cpp'
        str_allTestFileDst = str(pTestFldr / str_allTsts)
        str_allTestFileSrc = str(Path('Tools') / 'defaults' / 'src_templates' / str_allTsts)

        copyTxtFile(str_allTestFileSrc,str_allTestFileDst)

        #2 process test file according language
        str_src = ''
        path_src = Path('Tools') / 'defaults' / 'src_templates'
        dict = {'%COMPONENT_NAME': self.str_COMPONENT_NAME
                ,'%FILENAME': self.str_SRC_FILE.split('.')[0]
                ,'%DATE':datetime.now().strftime('%d.%m.%y %H:%M:%S')
                ,'%YEAR':datetime.now().strftime('%Y')
                ,'%HEADER_FILENAME': self.str_HEADER_FILE
                }
        if 'c++' == self.str_LANGUAGE:
            dict['%CLASSNAME'] = self.str_COMPONENT_NAME
            path_src = path_src / 'test.cpp'
        elif 'c' == self.str_LANGUAGE:
            path_src = path_src / 'c_test.cpp'
        else:
            assertWithText(False, 'Invalid language type.')

        str_src = str(path_src)
        str_dst = str(pTestFldr / 'test.cpp')
        processFile(str_src,str_dst, dict)


    def createTestInitFile(self):
        pTestFldr = Path(self.str_TPKG_FOLDER)
        if not pTestFldr.is_dir():
            pTestFldr.mkdir()

        dict = { '%SRC_FLDR%': self.str_SRC_FOLDER
                ,'%SRC_FILENAME%': self.str_SRC_FILE
                ,'%HEADER_FLDR%': self.str_HEADER_FOLDER
                ,'%HEADER_FILENAME%': self.str_HEADER_FILE
                ,'%COVERAGE_IS_USED%': self.testConfig.co_coverage.isTurnedOn
                ,'%COVERAGE_UNCOVLISTLEN%': self.testConfig.co_coverage.uncoveredLineListLength
                ,'%CHECKCODE_IS_USED%': self.testConfig.co_staticAnalysis.isTurnedOn
                ,'%CHECKCODE_TOOL%': self.testConfig.co_staticAnalysis.str_tool
                ,'%CHECKCODE_FORCEDLANG%': self.testConfig.co_staticAnalysis.str_ForcedLang
                ,'%CHECKCODE_C_VERSION%': self.testConfig.co_staticAnalysis.str_c_version
                ,'%CHECKCODE_CPP_VERSION%': self.testConfig.co_staticAnalysis.str_cpp_version
                ,'%TOOLCHAIN%': self.testConfig.co_testToolchain.str_compiler
                ,'%FRAMEWORK%': self.testConfig.co_testToolchain.str_testlib
                ,'%STATISTICS_IS_USED%': self.testConfig.co_codeStatistics.isTurnedOn
                ,'%STATISTICS_USE_SPECIFIC_ONLY%': self.testConfig.co_codeStatistics.isUsedTestSpecificOnly
                ,'%STATISTICS_USE_STRICTER%': self.testConfig.co_codeStatistics.isUsedStricter
                ,'%STATISTICS_MCCAVE_LEVEL%': self.testConfig.co_codeStatistics.int_mccabeComplex
                ,'%STATISTICS_FNCLEN_LEVEL%': self.testConfig.co_codeStatistics.int_fncLength
                ,'%STATISTICS_PARAM_CNT%': self.testConfig.co_codeStatistics.int_paramCnt
                }

        str_src = str(Path('Tools') / 'defaults' / 'src_templates' / 'test.ini')
        str_dst = str(pTestFldr / self.pkgDesc.str_testcfgfilename)
        processFile(str_src,str_dst,dict)
        pass

    def createTestCMakefile(self):
        dict = {'%TESTPACKAGENAME%': self.str_COMPONENT_NAME}
        str_src = str(Path('Tools') / 'defaults' / 'src_templates' / 'CMakeLists.txt')
        str_dst = str(Path(self.str_TPKG_FOLDER) / 'CMakeLists.txt')
        processFile(str_src,str_dst,dict)
        pass
