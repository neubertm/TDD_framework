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

from configparser import ConfigParser
from pathlib import Path


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'. Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError(f"invalid truth value {val!r}")


def StrToBool(strVal: str):
    return(strtobool(strVal.lower()) == 1)


class CSetupsCfg:
    folder: str
    useAllSetups: bool
    recognizeSetupSuffixes: [str]
    userSpecifiedSetupFiles: [str]
    showMenuEvenForOneSetup: bool

    def __init__(self):
        self.folder = "Tools/TestConfigs"
        self.useAllSetups = True
        self.recognizeSetupSuffixes = [".tcfg"]
        self.userSpecifiedSetupFiles = []
        self.showMenuEvenForOneSetup = True

    def _read_(self, CPS: ConfigParser):
        b_return = False
        if 'SETUP_CFG' in CPS.keys():
            CPS_SC = CPS['SETUP_CFG']
            if 'folder' in CPS_SC.keys():
                self.folder = CPS_SC['folder']
            if 'useAllSetups' in CPS_SC.keys():
                self.useAllSetups = StrToBool(CPS_SC['useAllSetups'])
            if 'recognizeSetupSuffixes' in CPS_SC.keys():
                self.recognizeSetupSuffixes = CPS_SC['recognizeSetupSuffixes'].split(
                    " ")
            if 'userSpecifiedSetupFiles' in CPS_SC.keys():
                lst = CPS_SC['userSpecifiedSetupFiles'].split(" ")
                self.userSpecifiedSetupFiles = [item for item in lst if item]
            if 'showMenuEvenForOneSetup' in CPS_SC.keys():
                self.showMenuEvenForOneSetup = StrToBool(
                    CPS_SC['showMenuEvenForOneSetup'])
            b_return = True
        return b_return

    def _checkConfiguration_(self):
        b_return = True
        b_return *= Path(self.folder).is_dir()
        assert Path(self.folder).is_dir(
        ), "TestConfig folder doesnt exists %s." % (self.folder)
        # TODO:
        # check that minimaly one configuration exists
        return b_return

    def readFromFile(self, fileName: str):
        parser = ConfigParser()
        parser.optionxform = str
        parser.read(fileName)
        CPS = parser._sections
        self._read_(CPS)


class CEnvCfg:
    str_cmake: str
    b_cmakeCheck: bool
    str_mingw: str
    b_mingwCheck: bool
    str_msvc: str
    b_msvcCheck: bool
    str_clang: str
    b_clangCheck: bool
    str_cppcheck: str
    b_cppcheckCheck: bool
    str_cppumockgen: str
    b_cppumockgen: bool

    def __init__(self):
        self.str_cmake = ""
        self.str_mingw = ""
        self.str_msvc = ""
        self.str_clang = ""
        self.str_cppcheck = ""
        self.str_cppumockgen = ""
        self.b_cmakeCheck = True
        self.b_mingwCheck = True
        self.b_msvcCheck = True
        self.b_clangCheck = True
        self.b_cppcheckCheck = True
        self.b_cppumockgen = True

    def _readMingw_(self, CPS: ConfigParser):
        bRetVal = False
        if "MINGW" in CPS.keys():
            CPS_MINGW = CPS['MINGW']
            if 'ENV_CONFIG_SCRIPT' in CPS_MINGW:
                self.str_mingw = CPS_MINGW['ENV_CONFIG_SCRIPT']
                bRetVal = True
            if 'check' in CPS_MINGW:
                self.b_mingwCheck = StrToBool(CPS_MINGW['check'])
        return(bRetVal)

    def _checkMingw_(self):
        b_return = False
        # TODO
        return b_return

    def _readClang_(self, CPS: ConfigParser):
        strVarName = "CLANG"
        bRetVal = False
        if strVarName in CPS.keys():
            CPS_CLANG = CPS[strVarName]
            if 'ENV_CONFIG_SCRIPT' in CPS_CLANG:
                self.str_clang = CPS_CLANG['ENV_CONFIG_SCRIPT']
                bRetVal = True
            if 'check' in CPS_CLANG:
                self.b_clangCheck = StrToBool(CPS_CLANG['check'])
        return(bRetVal)

    def _checkClang_(self):
        b_return = False
        # TODO
        return b_return

    def _readMsvc_(self, CPS: ConfigParser):
        bRetVal = False
        if "MSVC" in CPS.keys():
            CPS_MSVC = CPS['MSVC']
            if 'ENV_CONFIG_SCRIPT' in CPS_MSVC:
                self.str_msvc = CPS_MSVC['ENV_CONFIG_SCRIPT']
                bRetVal = True
            if 'check' in CPS_MSVC:
                self.b_msvcCheck = StrToBool(CPS_MSVC['check'])
        return(bRetVal)

    def _checkMsvc_(self):
        b_return = False
        # TODO
        return b_return

    def _readCppcheck_(self, CPS: ConfigParser):
        bRetVal = False
        if "CPPCHECK" in CPS.keys():
            CPS_CPPCHCK = CPS['CPPCHECK']
            if 'ENV_CONFIG_SCRIPT' in CPS_CPPCHCK:
                self.str_cppcheck = CPS_CPPCHCK['ENV_CONFIG_SCRIPT']
                bRetVal = True
            if 'check' in CPS_CPPCHCK:
                self.b_cppcheckCheck = StrToBool(CPS_CPPCHCK['check'])
        return(bRetVal)

    def _checkCppcheck_(self):
        b_return = False
        # TODO
        return b_return

    def _readCppUMockGen_(self, CPS: ConfigParser):
        bRetVal = False
        if "CPPUMOCKGEN" in CPS.keys():
            CPS_CPPUMOCKGEN = CPS['CPPUMOCKGEN']
            if 'ENV_CONFIG_SCRIPT' in CPS_CPPUMOCKGEN:
                self.str_cppumockgen = CPS_CPPUMOCKGEN['ENV_CONFIG_SCRIPT']
                bRetVal = True
            if 'check' in CPS_CPPUMOCKGEN:
                self.b_cppumockgen = StrToBool(CPS_CPPUMOCKGEN['check'])
        return bRetVal

    def _checkCppUMockGen_(self):
        return True
        pass

    def _readCMake_(self, CPS: ConfigParser):
        bRetVal = False
        if "CMAKE" in CPS.keys():
            CPS_CMAKE = CPS['CMAKE']
            if 'ENV_CONFIG_SCRIPT' in CPS_CMAKE:
                self.str_cmake = CPS_CMAKE['ENV_CONFIG_SCRIPT']
                bRetVal = True
            if 'check' in CPS_CMAKE:
                self.b_cmakeCheck = StrToBool(CPS_CMAKE['check'])
        return(bRetVal)

    def _checkCMake_(self):
        b_return = False
        # TODO
        return b_return

    def _read_(self, CPS: ConfigParser):
        self._readMingw_(CPS)
        if self.b_mingwCheck:
            assert self._checkMingw_(), "Error config for mingw failed -> %s" % (self.str_mingw)

        self._readMsvc_(CPS)
        if self.b_msvcCheck:
            assert self._checkMsvc_(), "Error config for msvc failed -> %s" % (self.str_msvc)
        self._readClang_(CPS)
        if self.b_clangCheck:
            assert self._checkClang_(), "Error config for clang failed -> %s" % (self.str_clang)
        self._readCMake_(CPS)
        if self.b_cmakeCheck:
            assert self._checkCMake_(), "Error config for clang failed -> %s" % (self.str_cmake)
        self._readCppcheck_(CPS)
        if self.b_cppcheckCheck:
            assert self._checkCppcheck_(), "Error config for cppcheck failed -> %s" % (self.str_cppcheck)

        self._readCppUMockGen_(CPS)
        if self.b_cppumockgen:
            assert self._checkCppUMockGen_(), "Error config for cppumockgen failed -> %s" % (self.str_cppcheck)

    def readFromFile(self, str_fileName: str):
        parser = ConfigParser()
        parser.optionxform = str
        parser.read(str_fileName)
        CPS = parser._sections
        self._read_(CPS)


class CCodeStatParamMinValue:
    int_mccabeComplex: int
    int_fncLength: int
    int_paramCnt: int

    def __init__(self):
        self.int_mccabeComplex = 7
        self.int_fncLength = 30
        self.int_paramCnt = 4

    def _read_(self, CPS: ConfigParser):
        bRetVal = False
        cnt = 0
        if "CODE_STATISTICS" in CPS.keys():
            CPS_CS = CPS['CODE_STATISTICS']
            if 'MCCABE' in CPS_CS:
                self.int_mccabeComplex = int(CPS_CS['MCCABE'])
                cnt += 1
            if 'FNC_LENGTH' in CPS_CS:
                self.int_fncLength = int(CPS_CS['FNC_LENGTH'])
                cnt += 1
            if 'PARAM_NUM' in CPS_CS:
                self.int_paramCnt = int(CPS_CS['PARAM_NUM'])
                cnt += 1
        if cnt == 3:
            bRetVal = True

        return(bRetVal)

    def readFromFile(self, str_fileName: str):
        parser = ConfigParser()
        parser.optionxform = str
        parser.read(str_fileName)
        CPS = parser._sections
        return (self._read_(CPS))


class CTestPkgDescription:
    str_srcfldr: str
    str_srctestfldr: str
    str_srctmp_suffix: str
    str_testfldr_suffix: str
    str_testpath: str
    str_testcfgfilename: str
    str_buildsuffix: str
    pass

    def __init__(self):
        self.str_srcfldr = "project"
        self.str_srctestfldr = "./src"
        self.str_srctmp_suffix = "tmp"
        self.str_testfldr_suffix = "_Tpkg"
        self.str_testpath = "TESTs"
        self.str_testcfgfilename = "test.ini"
        self.str_buildsuffix = "_build"
        pass

    def _read_(self, CPS: ConfigParser):
        bRetVal = False
        cnt = 0
        if "PATH" in CPS.keys():
            CPS_Path = CPS['PATH']
            if 'SRCFLDR' in CPS_Path:
                self.str_srcfldr = CPS_Path['SRCFLDR']
                cnt += 1
            if 'SRCTESTFLDR' in CPS_Path:
                self.str_srctestfldr = CPS_Path['SRCTESTFLDR']
                cnt += 1
            if 'SRCTMP_SUFFIX' in CPS_Path:
                self.str_srctmp_suffix = CPS_Path['SRCTMP_SUFFIX']
                cnt += 1
            if 'TESTFLDR_SUFFIX' in CPS_Path:
                self.str_testfldr_suffix = CPS_Path['TESTFLDR_SUFFIX']
                cnt += 1
            if 'TESTPATH' in CPS_Path:
                self.str_testpath = CPS_Path['TESTPATH']
                cnt += 1
            if 'BUILD_SUFFIX' in CPS_Path:
                self.str_buildsuffix = CPS_Path['BUILD_SUFFIX']
                cnt += 1
            if 'TEST_INI_FILE_NAME' in CPS_Path:
                self.str_testcfgfilename = CPS_Path['TEST_INI_FILE_NAME']
                cnt += 1

        if cnt == 7:
            bRetVal = True

        return(bRetVal)

    def readFromFile(self, str_fileName: str):
        parser = ConfigParser()
        parser.optionxform = str
        parser.read(str_fileName)
        CPS = parser._sections
        return (self._read_(CPS))


class CMainConfig:

    separ: str
    hsuffix: []
    co_env: CEnvCfg
    co_stat: CCodeStatParamMinValue
    co_pkg: CTestPkgDescription

    def __init__(self, str_fName=""):
        self.separ = "/"
        self.hsuffix = ['h', 'hpp', 'H', 'HPP']
        self.co_stat = CCodeStatParamMinValue()
        self.co_env = CEnvCfg()
        self.co_pkg = CTestPkgDescription()
        if str_fName:
            self.readCfgFile(str_fName)

    def readCfgFile(self, str_fName: str):
        mainConfigParser = ConfigParser()
        mainConfigParser.optionxform = str
        mainConfigParser.read(str_fName)
        CPS = mainConfigParser._sections
        self.co_pkg._read_(CPS)
        self.co_env._read_(CPS)
        self.co_stat._read_(CPS)


class MainConfigsLists:
    listOfMainCfg: [CMainConfig]

    def __init__(self, str_syscfg):
        pass


class CBaseToolCfg:
    isTurnedOn: bool
    str_toolName: str
    str_sectionName: str
    str_turnOnKeyName: str

    def __init__(self, str_name: str, b_state=True):
        self.isTurnedOn = b_state
        self.str_toolName = str_name
        self.str_sectionName = str_name.upper()
        self.str_turnOnKeyName = str_name.lower()

    def _readState_(self, CPS: ConfigParser):
        # print(self.str_sectionName)
        if self.str_sectionName in CPS.keys():
            CPS_SEC = CPS[self.str_sectionName]
            if self.str_turnOnKeyName in CPS_SEC:
                self.isTurnedOn = dict(CPS_SEC).get(
                    self.str_turnOnKeyName) == 'True'


class CCovCfg(CBaseToolCfg):
    uncoveredLineListLength: int

    def __init__(self):
        CBaseToolCfg.__init__(self, "COVERAGE")
        self.uncoveredLineListLength = 30

    def _read_(self, CPS: ConfigParser):
        self._readState_(CPS)

        if 'uncoveredLineListLength' in CPS:
            self.uncoveredLineListLength = int(CPS['uncoveredLineListLength'])
        # TODO in future here we have to add more configuration for other coverage tools
        pass


class CStaticAnalysisCfg(CBaseToolCfg):
    isLanguageDefinedBySuffix: bool
    str_tool: str
    str_ForcedLang: str
    str_c_version: str
    str_cpp_version: str
    suppressionLst: [str]

    def __init__(self):
        CBaseToolCfg.__init__(self, "CHECKCODE")
        self.isLanguageDefinedBySuffix = False
        self.str_tool = "cppcheck"
        self.str_ForcedLang = "c++"
        self.str_c_version = "c99"
        self.str_cpp_version = "c++03"
        self.suppressionLst = []

    def _read_(self, CPS: ConfigParser):
        self._readState_(CPS)
        if self.str_sectionName in CPS.keys():
            CPS_SEC = CPS[self.str_sectionName]
            if 'isLanguageDefinedBySuffix' in CPS_SEC:
                self.isLanguageDefinedBySuffix = StrToBool(
                    CPS_SEC['isLanguageDefinedBySuffix'])
            if 'tool' in CPS_SEC:
                self.str_tool = CPS_SEC['tool']
            if 'forcedLanguage' in CPS_SEC:
                self.str_ForcedLang = CPS_SEC['forcedLanguage']
            if 'c_version' in CPS_SEC:
                self.str_c_version = CPS_SEC['c_version']
            if 'cpp_version' in CPS_SEC:
                self.str_cpp_version = CPS_SEC['cpp_version']
            if 'suppress_list' in CPS_SEC:
                suppStr = CPS_SEC['suppress_list']
                suppStr = suppStr.replace(" ", "")
                self.suppressionLst = suppStr.split(",")
        pass


class CFormaterGuidelineCheckerCfg(CBaseToolCfg):
    isTurnedOnInplaceSrcEdit: bool
    str_tool: str
    str_configFile: str

    def __init__(self):
        CBaseToolCfg.__init__(self, "CODINGGUIDELINES", False)
        self.isTurnedOnInplaceSrcEdit = False
        self.str_tool = "clang-formater"
        self.str_configFile = "Tools/.clang-format"
        pass

    def _read_(self, CPS: ConfigParser):
        self._readState_(CPS)
        if self.str_sectionName in CPS.keys():
            CPS_SEC = CPS[self.str_sectionName]
            if 'inplaceSrcEdit' in CPS_SEC:
                self.isTurnedOnInplaceSrcEdit = StrToBool(
                    CPS_SEC['inplaceSrcEdit'])
            if 'tool' in CPS_SEC:
                self.str_tool = CPS_SEC['tool']
            if 'configFile' in CPS_SEC:
                self.str_configFile = CPS_SEC['configFile']


class CTestToolchainCfg(CBaseToolCfg):
    str_compiler: str
    str_testlib:  str
    str_automock: str

    def __init__(self):
        CBaseToolCfg.__init__(self, "TOOLCHAIN")
        self.str_compiler = "gcc"
        self.str_testlib = "cpputest"
        self.str_automock = 'cppumockgen'

    def _read_(self, CPS: ConfigParser):
        if self.str_sectionName in CPS.keys():
            CPS_SEC = CPS[self.str_sectionName]
            if 'framework' in CPS_SEC:
                self.str_testlib = CPS_SEC['framework']
            if 'toolchain' in CPS_SEC:
                self.str_compiler = CPS_SEC['toolchain']
            if 'automock' in CPS_SEC:
                self.str_automock = CPS_SEC['automock']



class CCodeStatisticsCfg(CBaseToolCfg, CCodeStatParamMinValue):
    isUsedTestSpecificOnly: bool
    isUsedStricter: bool

    def __init__(self):
        CBaseToolCfg.__init__(self, "STATISTICS")
        CCodeStatParamMinValue.__init__(self)
        self.isUsedTestSpecificOnly = False
        self.isUsedStricter = True

    def _read_(self, CPS: ConfigParser):
        self._readState_(CPS)
        if self.str_sectionName in CPS.keys():
            CPS_SEC = CPS[self.str_sectionName]

            if 'useTestSpecificOnly' in CPS_SEC:
                self.isUsedTestSpecificOnly = StrToBool(
                    CPS_SEC['useTestSpecificOnly'])

            if 'useStricter' in CPS_SEC:
                self.isUsedStricter = StrToBool(
                    CPS_SEC['useStricter'])

            if 'MCCABE' in CPS_SEC:
                self.int_mccabeComplex = int(CPS_SEC['MCCABE'])

            if 'FNC_LENGTH' in CPS_SEC:
                self.int_fncLength = int(CPS_SEC['FNC_LENGTH'])

            if 'PARAM_NUM' in CPS_SEC:
                self.int_paramCnt = int(CPS_SEC['PARAM_NUM'])


class CDebugConfig():
    isDebugConfigOn: bool

    def __init__(self):
        self.isDebugConfigOn = False

    def _read_(self, CPS: ConfigParser):
        if "BUILD_CONFIG" in CPS.keys():
            BUILD_SEC = CPS["BUILD_CONFIG"]
            if 'DEBUG_MODE' in BUILD_SEC:
                self.isDebugConfigOn = StrToBool(BUILD_SEC['DEBUG_MODE'])


class CTestConfig:
    SUT_dict: {str: str}
    OTHER_dict: {str: str}
    AUTOMOCK_dict: {str: str}
    AUTOMOCKCPP_dict: {str: str}
    AUTOMOCKFLDRINC_lst: [str]
    co_debugconfig: CDebugConfig
    co_coverage: CCovCfg
    co_staticAnalysis: CStaticAnalysisCfg
    co_guidelineFormat: CFormaterGuidelineCheckerCfg
    co_testToolchain: CTestToolchainCfg
    co_codeStatistics: CCodeStatisticsCfg
    pass

    def __init__(self):
        self.SUT_dict = {}
        self.OTHER_dict = {}
        self.AUTOMOCK_dict = {}
        self.AUTOMOCKCPP_dict = {}
        self.AUTOMOCKFLDRINC_lst = []
        self.co_debugconfig = CDebugConfig()
        self.co_coverage = CCovCfg()
        self.co_staticAnalysis = CStaticAnalysisCfg()
        self.co_guidelineFormat = CFormaterGuidelineCheckerCfg()
        self.co_testToolchain = CTestToolchainCfg()
        self.co_codeStatistics = CCodeStatisticsCfg()

    def readCfgFile(self, str_fName: str):
        CP = readAndFixTestConfigFile(str_fName)
        CPS = CP._sections
        assert 'SUT' in CPS, "Assertion missing SUT section in test configuration file %s" % (
            str_fName)
        self.SUT_dict = dict(CPS['SUT'])

        if 'OTHER' in CPS:
            self.OTHER_dict = dict(CPS['OTHER'])

        if 'AUTOMOCK' in CPS:
            self.AUTOMOCK_dict = dict(CPS['AUTOMOCK'])

        if 'AUTOMOCKCPP' in CPS:
            self.AUTOMOCKCPP_dict = dict(CPS['AUTOMOCKCPP'])

        if 'AUTOMOCKFLDRINC' in CPS:
            self.AUTOMOCKFLDRINC_lst = list(dict(CPS['AUTOMOCKFLDRINC']).keys())
        # print(self.SUT_dict)
        # print(self.OTHER_dict)
        self.co_debugconfig._read_(CPS)
        self.co_coverage._read_(CPS)
        self.co_staticAnalysis._read_(CPS)
        self.co_guidelineFormat._read_(CPS)
        self.co_testToolchain._read_(CPS)
        self.co_codeStatistics._read_(CPS)
        # exit(0)


def readAndFixTestConfigFile(cfgFileName):
    """Read init file for specific test."""
    with open(cfgFileName) as cfgFile:
        cfgdta = cfgFile.read()

    # Replace => to =
    cfgdta = cfgdta.replace('=>', '=')
    # Split to list of line
    cfglst = cfgdta.split("\n")
    cfgUpdateLst = []
    for text in cfglst:  # for each line in list
        if len(text) != 0:  # if non empty lines
            if text.find("[") == -1:  # if line doesnt open section
                if text.find("=") == -1:  # if line doesnt contain equal sign
                    text += " = " + "SRC_TEMP"

                # line contain equal sign,
                # we have to check if right side is nonempty
                else:
                    text__ = text.replace(" ", "")   # remove spaces
                    contentList = text__.split("=")  # split according equal
                    # this operation remove empty item
                    contentList = [s for s in contentList if s]
                    # now we check that is necessary to update right side
                    if len(contentList) == 1:
                        text += " " + "SRC_TEMP"
        # add fixed or unfixed line to configuration string
        cfgUpdateLst.append(text + "\n")
    o_testConfig = ConfigParser()
    o_testConfig.optionxform = str
    o_testConfig.read_string("".join(cfgUpdateLst))
    # print(cfgUpdateLst)
    return(o_testConfig)
