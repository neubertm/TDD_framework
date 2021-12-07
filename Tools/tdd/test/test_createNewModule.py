from .context import createNewModule
from .context import TDDConfig

import unittest
from unittest.mock import patch

import sys
import os

from pathlib import Path


class TestCreateNewModule(unittest.TestCase):

    @patch('createNewModule.get_input', return_value='yes')
    def test_questionYesNo_answerYes(self, get_input):
        self.assertEqual(createNewModule.questionYesNo("TEST_TEXT"), True)

    @patch('createNewModule.get_input', return_value='y')
    def test_questionYesNo_answerY(self, input):
        self.assertEqual(createNewModule.questionYesNo("TEST_TEXT"), True)

    @patch('createNewModule.get_input', return_value='no')
    def test_questionYesNo_answerNo(self, input):
        self.assertEqual(createNewModule.questionYesNo("TEST_TEXT"), False)

    @patch('createNewModule.get_input', return_value='n')
    def test_questionYesNo_answerN(self, input):
        self.assertEqual(createNewModule.questionYesNo("TEST_TEXT"), False)

    @patch('createNewModule.get_input', return_value='')
    def test_questionWithList_UseDefault(self, input):
        default = 'HOO'
        list = ['FOO', 'HOO', 'POO']
        with patch('createNewModule.printout'):
            self.assertEqual(createNewModule.questionWithList("TEST_TEXT",list,default), default)

    @patch('createNewModule.get_input', return_value='FOO')
    def test_questionWithList_UseFOO(self, input):
        default = 'HOO'
        list = ['FOO', 'HOO', 'POO']
        self.assertEqual(createNewModule.questionWithList("TEST_TEXT",list,default), 'FOO')

    @patch('createNewModule.get_input', return_value='POO')
    def test_questionWithList_UsePOO(self, input):
        default = 'HOO'
        list = ['FOO', 'HOO', 'POO']
        self.assertEqual(createNewModule.questionWithList("TEST_TEXT",list,default), 'POO')

    def test_createNewModule_initToDefaultParameters(self):
        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)
        self.assertEqual(newModule.str_SRC_FOLDER,"")
        self.assertEqual(newModule.str_HEADER_FOLDER,"")
        self.assertEqual(newModule.str_SRC_FILE,"")
        self.assertEqual(newModule.str_HEADER_FILE,"")
        self.assertEqual(newModule.str_FRAMEWORK,"cpputest")
        self.assertEqual(newModule.str_TOOLCHAIN,"mingw")
        self.assertEqual(newModule.str_LANGUAGE,"c++")
        self.assertEqual(newModule.str_COMPONENT_NAME,"")
        self.assertEqual(newModule.str_SRC_TYPE,"")
        self.assertEqual(newModule.copyFileLst,[])

    @patch('createNewModule.CreateNewModule.setModuleConfiguration')
    @patch('createNewModule.CreateNewModule.createFolder_SUT')
    @patch('createNewModule.CreateNewModule.createFolder_TPKG')
    @patch('createNewModule.CreateNewModule.createAndCopyFiles')
    def test_createNewModule_testTopFunctionForCreateNewModule(self, mock_input1,  mock_input2,  mock_input3, mock_input4):
        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.createNewModule()
        pass

    @patch('createNewModule.questionWithList', return_value='c')
    @patch('createNewModule.CreateNewModule.defineSutFileConfiguration')
    @patch('createNewModule.CreateNewModule.defineCoverageCfg', return_value=TDDConfig.CCovCfg())
    @patch('createNewModule.CreateNewModule.defineStatAnalysisCfg', return_value=TDDConfig.CStaticAnalysisCfg())
    @patch('createNewModule.CreateNewModule.defineToolchainCfg', return_value=TDDConfig.CTestToolchainCfg())
    @patch('createNewModule.CreateNewModule.defineCodeStatisticsCfg', return_value=TDDConfig.CCodeStatisticsCfg())
    def test_createNewModule_setModuleConfiguration_setC(self,mock_qList,mock_files,mock_cover,mock_statA,mock_toolCH,mock_codeStat):
        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.setModuleConfiguration()

        self.assertEqual(newModule.str_LANGUAGE,"c")
        self.assertTrue(mock_qList.called)
        self.assertTrue(mock_files.called)
        self.assertTrue(mock_cover.called)
        self.assertTrue(mock_statA.called)
        self.assertTrue(mock_toolCH.called)
        self.assertTrue(mock_codeStat.called)
        pass

    @patch('createNewModule.questionWithList', return_value='c++')
    @patch('createNewModule.CreateNewModule.defineSutFileConfiguration')
    @patch('createNewModule.CreateNewModule.defineCoverageCfg', return_value=TDDConfig.CCovCfg())
    @patch('createNewModule.CreateNewModule.defineStatAnalysisCfg', return_value=TDDConfig.CStaticAnalysisCfg())
    @patch('createNewModule.CreateNewModule.defineToolchainCfg', return_value=TDDConfig.CTestToolchainCfg())
    @patch('createNewModule.CreateNewModule.defineCodeStatisticsCfg', return_value=TDDConfig.CCodeStatisticsCfg())
    def test_createNewModule_setModuleConfiguration_setCPP(self,mock_qList,mock_files,mock_cover,mock_statA,mock_toolCH,mock_codeStat):
        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.setModuleConfiguration()

        self.assertEqual(newModule.str_LANGUAGE,"c++")
        self.assertTrue(mock_qList.called)
        self.assertTrue(mock_files.called)
        self.assertTrue(mock_cover.called)
        self.assertTrue(mock_statA.called)
        self.assertTrue(mock_toolCH.called)
        self.assertTrue(mock_codeStat.called)
        pass

    @patch('createNewModule.CreateNewModule.setModuleConfiguration')
    @patch('createNewModule.CreateNewModule.createFolder_SUT')
    @patch('createNewModule.CreateNewModule.createFolder_TPKG')
    @patch('createNewModule.CreateNewModule.createAndCopyFiles')
    def test_createNewModule_testTopFunctionForCreateNewModule(self, mock_setModule, mock_createSutFolder, mock_createPkgFolder,  mock_fileCopy):
        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.createNewModule()
        self.assertTrue(mock_setModule.called)
        self.assertTrue(mock_createSutFolder.called)
        self.assertTrue(mock_createPkgFolder.called)
        self.assertTrue(mock_fileCopy.called)
        pass

    @patch('createNewModule.CreateNewModule.defineSutFileNames')
    @patch('createNewModule.CreateNewModule.defineSutFolders')
    def test_defineSutFileConfiguration(self, mock_SFileName, mock_SFlds):
        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.defineSutFileConfiguration()

        self.assertTrue(mock_SFileName.called)
        self.assertTrue(mock_SFlds.called)
        pass

    @patch('createNewModule.printout')
    @patch('createNewModule.questionWithList', side_effect=['cpp','hpp'])
    @patch('createNewModule.questionReturnString', return_value='FOOO')
    @patch('createNewModule.questionYesNo', return_value=True)
    def test_defineSutFileNames_defaultAndFoooName(self, mock_printout, mock_qwl, mock_qrs, mock_qYN):
        #mock_qwl.side_effect = ['cpp','hpp']

        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)

        newModule.defineSutFileNames()

        #Check printout function
        #mprintout_args,mprintout_kwargs  = mock_printout.call_args
        str_fullSrcName = '.'.join([newModule.str_COMPONENT_NAME,"cpp"])
        str_fullHeaderName = '.'.join([newModule.str_COMPONENT_NAME,'hpp'])
        #self.assertEqual(mprintout_args, ['New SUT object definition:','New SUT file are: \n\t%s\n\t%s' % (str_fullHeaderName, str_fullSrcName)])
        self.assertTrue(mock_printout.called)
        self.assertTrue(mock_qrs.called)
        self.assertTrue(mock_qYN.called)


        #other Assertion
        self.assertEqual(newModule.str_LANGUAGE, 'c++')
        self.assertEqual(newModule.str_COMPONENT_NAME, 'FOOO')
        self.assertEqual(newModule.str_SRC_FILE, 'FOOO.cpp')
        self.assertEqual(newModule.str_HEADER_FILE, 'FOOO.hpp')

    @patch('createNewModule.printout')
    @patch('createNewModule.questionWithList', side_effect=['c','h'])
    @patch('createNewModule.questionReturnString', return_value='POOO')
    @patch('createNewModule.questionYesNo', return_value=True)
    def test_defineSutFileNames_cAndPoooName(self, mock_printout, mock_qwl, mock_qrs, mock_qYN):
        #mock_qwl.side_effect = ['cpp','hpp']

        testDesc = TDDConfig.CTestPkgDescription
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.str_LANGUAGE = 'c'

        newModule.defineSutFileNames()

        #Check printout function
        #mprintout_args,mprintout_kwargs  = mock_printout.call_args
        str_fullSrcName = '.'.join([newModule.str_COMPONENT_NAME,"cpp"])
        str_fullHeaderName = '.'.join([newModule.str_COMPONENT_NAME,'hpp'])
        #self.assertEqual(mprintout_args, ['New SUT object definition:','New SUT file are: \n\t%s\n\t%s' % (str_fullHeaderName, str_fullSrcName)])
        self.assertTrue(mock_printout.called)
        self.assertTrue(mock_qrs.called)
        self.assertTrue(mock_qYN.called)


        #other Assertion
        self.assertEqual(newModule.str_LANGUAGE, 'c')
        self.assertEqual(newModule.str_COMPONENT_NAME, 'POOO')
        self.assertEqual(newModule.str_SRC_FILE, 'POOO.c')
        self.assertEqual(newModule.str_HEADER_FILE, 'POOO.h')

    @patch('createNewModule.printout')
    @patch('createNewModule.questionYesNo', return_value=True)
    def test_defineSutFolders_default(self, mock_printout, mock_qyn):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)

        # this fake calling defineSutNames function
        newModule.str_COMPONENT_NAME =  'FOOO'
        newModule.str_SRC_FILE = 'FOOO.cpp'
        newModule.str_HEADER_FILE = 'FOOO.hpp'

        newModule.defineSutFolders()
        self.assertTrue(mock_printout.called)
        self.assertTrue(mock_qyn.called)

        self.assertEqual( str(Path(newModule.pkgDesc.str_srcfldr) / 'src'), newModule.str_SRC_FOLDER )
        self.assertEqual( str(Path(newModule.pkgDesc.str_srcfldr) / 'include'), newModule.str_HEADER_FOLDER )
        pass

    @patch('createNewModule.printout')
    @patch('createNewModule.questionYesNo', return_value=False)
    @patch('createNewModule.questionReturnString', side_effect=['INCLUDE', 'SOURCE'])
    def test_defineSutFolders_UserDefinedSutFolders(self, mock_printout, mock_qyn, mock_qrs):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)

        # this fake calling defineSutNames function
        newModule.str_COMPONENT_NAME =  'FOOO'
        newModule.str_SRC_FILE = 'FOOO.cpp'
        newModule.str_HEADER_FILE = 'FOOO.hpp'

        newModule.defineSutFolders()
        self.assertTrue(mock_printout.called)
        self.assertTrue(mock_qyn.called)
        self.assertTrue(mock_qrs.called)

        self.assertEqual( str(Path(newModule.pkgDesc.str_srcfldr) / 'SOURCE'), newModule.str_SRC_FOLDER )
        self.assertEqual( str(Path(newModule.pkgDesc.str_srcfldr) / 'INCLUDE'), newModule.str_HEADER_FOLDER )
        pass
