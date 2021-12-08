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

    @patch('createNewModule.questionYesNo', return_value=True)
    def test_defineCoverageCfg_default(self,mock_qyn):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.testConfig.co_coverage.isTurnedOn = False

        newModule.defineCoverageCfg()

        self.assertTrue(mock_qyn.called)
        self.assertEqual(newModule.testConfig.co_coverage.isTurnedOn, True)
        self.assertEqual(newModule.testConfig.co_coverage.uncoveredLineListLength, 0)
        pass

    @patch('createNewModule.questionYesNo', return_value=False)
    def test_defineCoverageCfg_UserTurnOffCoverage(self,mock_qyn):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.testConfig.co_coverage.isTurnedOn = True

        newModule.defineCoverageCfg()

        self.assertTrue(mock_qyn.called)
        self.assertEqual(newModule.testConfig.co_coverage.isTurnedOn, False)
        self.assertEqual(newModule.testConfig.co_coverage.uncoveredLineListLength, 0)
        pass

    @patch('createNewModule.questionYesNo', side_effect=[ True, True])
    @patch('createNewModule.questionWithList', side_effect=['c99t','c++11t'])
    def test_defineStatAnalysisCfg_default(self, mock_qyn, mock_qwl):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.testConfig.co_staticAnalysis.isTurnedOn = False
        newModule.testConfig.co_staticAnalysis.str_tool = 'unknown tools'
        newModule.testConfig.co_staticAnalysis.str_ForcedLang = 'FOO'

        newModule.defineStatAnalysisCfg()

        self.assertTrue(mock_qyn.called)
        self.assertTrue(mock_qwl.called)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.isTurnedOn, True)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.isLanguageDefinedBySuffix, True)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_c_version, 'c99t')
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_cpp_version, 'c++11t')
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_tool, 'cppcheck')
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_ForcedLang, newModule.str_LANGUAGE)
        pass

    @patch('createNewModule.questionYesNo', side_effect=[ True, False])
    @patch('createNewModule.questionWithList', side_effect=['c99t','c++11t'])
    def test_defineStatAnalysisCfg_languageNotDefineBySuffix(self, mock_qyn, mock_qwl):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.testConfig.co_staticAnalysis.isTurnedOn = False
        newModule.testConfig.co_staticAnalysis.str_tool = 'unknown tools'
        newModule.testConfig.co_staticAnalysis.str_ForcedLang = 'FOO'

        newModule.defineStatAnalysisCfg()

        self.assertTrue(mock_qyn.called)
        self.assertTrue(mock_qwl.called)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.isTurnedOn, True)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.isLanguageDefinedBySuffix, False)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_c_version, 'c99t')
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_cpp_version, 'c++11t')
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_tool, 'cppcheck')
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_ForcedLang, newModule.str_LANGUAGE)
        pass

    @patch('createNewModule.questionYesNo', side_effect=[ False ])
    def test_defineStatAnalysisCfg_switchOff(self, mock_qyn):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.testConfig.co_staticAnalysis.isTurnedOn = True

        newModule.defineStatAnalysisCfg()

        self.assertTrue(mock_qyn.called)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.isTurnedOn, False)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.isLanguageDefinedBySuffix, False)
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_c_version, 'c99')
        self.assertEqual(newModule.testConfig.co_staticAnalysis.str_cpp_version, 'c++03')
        pass

    def test_defineToolchainCfg_default(self):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)

        newModule.defineToolchainCfg()

        self.assertEqual(newModule.testConfig.co_testToolchain.str_compiler, 'mingw')
        self.assertEqual(newModule.testConfig.co_testToolchain.str_testlib, 'cpputest')

    @patch('createNewModule.questionYesNo', side_effect=[ True, False, True ])
    @patch('createNewModule.questionReturningPositiveInteger', side_effect=[ 10, 20, 30 ])
    def test_defineCodeStatisticsCfg_allTurnedOn_10_20_30(self, mock_qyn, mock_qrpi):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)

        newModule.defineCodeStatisticsCfg()

        self.assertTrue(mock_qyn.called)
        self.assertTrue(mock_qrpi.called)
        self.assertEqual(newModule.testConfig.co_codeStatistics.isTurnedOn, True)
        self.assertEqual(newModule.testConfig.co_codeStatistics.isUsedTestSpecificOnly, False)
        self.assertEqual(newModule.testConfig.co_codeStatistics.isUsedStricter, True)
        self.assertEqual(newModule.testConfig.co_codeStatistics.int_mccabeComplex, 10)
        self.assertEqual(newModule.testConfig.co_codeStatistics.int_fncLength, 20)
        self.assertEqual(newModule.testConfig.co_codeStatistics.int_paramCnt, 30)

    @patch('createNewModule.questionYesNo', side_effect=[ True, True])
    @patch('createNewModule.questionReturningPositiveInteger', side_effect=[ 10, 20, 30 ])
    def test_defineCodeStatisticsCfg_allTurnedOn_10_20_30_notUseStricter(self, mock_qyn, mock_qrpi):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)

        newModule.defineCodeStatisticsCfg()

        self.assertTrue(mock_qyn.called)
        self.assertTrue(mock_qrpi.called)
        self.assertEqual(newModule.testConfig.co_codeStatistics.isTurnedOn, True)
        self.assertEqual(newModule.testConfig.co_codeStatistics.isUsedTestSpecificOnly, True)
        self.assertEqual(newModule.testConfig.co_codeStatistics.int_mccabeComplex, 10)
        self.assertEqual(newModule.testConfig.co_codeStatistics.int_fncLength, 20)
        self.assertEqual(newModule.testConfig.co_codeStatistics.int_paramCnt, 30)

    @patch('createNewModule.questionYesNo', side_effect=[ False ])
    def test_defineCodeStatisticsCfg_SwitchedOff(self, mock_qyn):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)

        newModule.defineCodeStatisticsCfg()

        self.assertTrue(mock_qyn.called)
        self.assertEqual(newModule.testConfig.co_codeStatistics.isTurnedOn, False)


    @patch('createNewModule.createFolder')
    def test_createFolder_SUT_OK(self, mock_cf):
        testDesc = TDDConfig.CTestPkgDescription()
        newModule = createNewModule.CreateNewModule(testDesc)
        newModule.str_HEADER_FOLDER = 'TEST_NAME.H'
        newModule.str_SRC_FOLDER = 'TEST_NAME.CPP'

        newModule.createFolder_SUT()
        mock_cf_list = mock_cf.call_args_list
        self.assertTrue(len(mock_cf_list), 2)
        mock_cf_list[0].assert_called_with('TEST_NAME.H')
        mock_cf_list[1].assert_called_with('TEST_NAME.CPP')


    @patch('pathlib.Path.__init__', return_value=None)
    @patch('pathlib.Path.is_dir', return_value=True)
    def test_createFolder_dirExitsDoNothing(self, mock_isDir, mock_PathInit):
        createNewModule.createFolder("FOO_FOLDER_NAME")

        mock_PathInit.assert_called_with("FOO_FOLDER_NAME")


    @patch('pathlib.Path.__init__',return_value=None)
    @patch('pathlib.Path.is_dir',side_effect=[False, True])
    @patch('pathlib.Path.mkdir')
    @patch('createNewModule.assertWithText')
    def test_createFolder_dirNotExitSuccesfulCreating(self, mock_awt, mock_mkdir, mock_isDir, mock_PathInit):
        createNewModule.createFolder("FOO_FOLDER_NAME")

        mock_PathInit.assert_called_with("FOO_FOLDER_NAME")
        mock_mkdir.assert_called_with(mode=666,parent=True)
        mock_awt.assert_called_with(True, 'Creating folder FOO_FOLDER_NAME failed!')


    @patch('pathlib.Path.__init__', return_value=None)
    @patch('pathlib.Path.is_dir', return_value=False)
    @patch('createNewModule.createFolder')
    def test_createFolderTpkg_OK(self, mock_cf, mock_isDir, mock_PathInit):
        testDesc = TDDConfig.CTestPkgDescription()
        nm = createNewModule.CreateNewModule(testDesc)
        nm.str_COMPONENT_NAME = 'FOOO'

        nm.createFolder_TPKG()

        mock_PathInit.assert_called_with(nm.pkgDesc.str_testpath)
        self.assertTrue(mock_isDir.called)
        str_fldrName=str(Path(nm.pkgDesc.str_testpath) / (nm.str_COMPONENT_NAME + nm.pkgDesc.str_testfldr_suffix))
        str_fldrNameSrc=str(Path(nm.pkgDesc.str_testpath) / (nm.str_COMPONENT_NAME + nm.pkgDesc.str_testfldr_suffix) / nm.pkgDesc.str_srctestfldr)

        mock_cf_list = mock_cf.call_args_list

        mock_cf_list[0].assert_called_with(str_fldrName)
        self.assertEqual(nm.str_TPKG_FOLDER, str_fldrName)
        mock_cf_list[1].assert_called_with(str_fldrNameSrc)
        pass

    @patch('pathlib.Path.__init__', return_value=None)
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('createNewModule.createFolder')
    @patch('createNewModule.timeInShortString', return_value='00112233445566778899')
    def test_createFolderTpkg_FldrExistsCreateWithTimeStamp(self,mock_timeStr ,mock_cf, mock_isDir, mock_PathInit):
        testDesc = TDDConfig.CTestPkgDescription()
        nm = createNewModule.CreateNewModule(testDesc)
        nm.str_COMPONENT_NAME = 'FOOO'

        nm.createFolder_TPKG()

        mock_PathInit.assert_called_with(nm.pkgDesc.str_testpath)
        self.assertTrue(mock_isDir.called)
        str_fldrName=str(Path(nm.pkgDesc.str_testpath) / (nm.str_COMPONENT_NAME + '00112233445566778899' + nm.pkgDesc.str_testfldr_suffix))
        str_fldrNameSrc=str(Path(nm.pkgDesc.str_testpath) / (nm.str_COMPONENT_NAME + '00112233445566778899' + nm.pkgDesc.str_testfldr_suffix) / nm.pkgDesc.str_srctestfldr)

        mock_cf_list = mock_cf.call_args_list

        mock_cf_list[0].assert_called_with(str_fldrName)
        self.assertEqual(nm.str_TPKG_FOLDER, str_fldrName)
        mock_cf_list[1].assert_called_with(str_fldrNameSrc)
        pass

    @patch('createNewModule.CreateNewModule.createHeaderFile')
    @patch('createNewModule.CreateNewModule.createSourceFile')
    @patch('createNewModule.CreateNewModule.copyAndCreateTestFiles')
    @patch('createNewModule.CreateNewModule.createTestInitFile')
    @patch('createNewModule.CreateNewModule.copyTestCMakefile')
    def test_createAndCopyFiles(self,mock_make, mock_ini, mock_test, mock_source, mock_header):
        testDesc = TDDConfig.CTestPkgDescription()
        nm = createNewModule.CreateNewModule(testDesc)
        nm.createAndCopyFiles()
        self.assertTrue(mock_header.called)
        self.assertTrue(mock_source.called)
        self.assertTrue(mock_test.called)
        self.assertTrue(mock_ini.called)
        self.assertTrue(mock_make.called)
        pass

    @patch('createNewModule.processFile')
    def test_createHeaderFile_cHeader(self, mock_pf):
        testDesc = TDDConfig.CTestPkgDescription()
        nm = createNewModule.CreateNewModule(testDesc)
        nm.str_LANGUAGE = 'c'
        nm.str_HEADER_FOLDER = 'HEADERFOLDER'
        nm.str_HEADER_FILE = 'HEADERfile.H'

        nm.createHeaderFile()

        self.assertTrue(mock_pf.called)
        pf_args = mock_pf.call_args
        str_src = str(Path('Tools') / 'defaults' / 'src_templates' / 'c_file.h')
        str_dst = str(Path(nm.str_HEADER_FOLDER) / nm.str_HEADER_FILE)
        len_dic = 4
        self.assertEqual(str_src, pf_args[0][0])
        self.assertEqual(str_dst, pf_args[0][1])
        self.assertEqual(len_dic, len(pf_args[0][2]))

    @patch('createNewModule.processFile')
    def test_createHeaderFile_cppHeader(self, mock_pf):
        testDesc = TDDConfig.CTestPkgDescription()
        nm = createNewModule.CreateNewModule(testDesc)
        nm.str_LANGUAGE = 'c++'
        nm.str_HEADER_FOLDER = 'HEADERFOLDER'
        nm.str_HEADER_FILE = 'HEADERfile.HPP'

        nm.createHeaderFile()

        self.assertTrue(mock_pf.called)
        pf_args = mock_pf.call_args
        str_src = str(Path('Tools') / 'defaults' / 'src_templates' / 'class.hpp')
        str_dst = str(Path(nm.str_HEADER_FOLDER) / nm.str_HEADER_FILE)
        len_dic = 5
        self.assertEqual(str_src, pf_args[0][0])
        self.assertEqual(str_dst, pf_args[0][1])
        self.assertEqual(len_dic, len(pf_args[0][2]))

    @patch('createNewModule.readFileToStr',return_value="ABC")
    @patch('createNewModule.writeStringToFile')
    @patch('createNewModule.patchString',return_value='ABCD')
    def test_processFile(self, mock_ps, mock_wstf, mock_rfts):
        str_src = 'SRC_FILE'
        str_dst = 'DST_FILE'
        dict = {'KEY0': 'VAL0', 'KEY1': 'VAL1'}

        createNewModule.processFile(str_src, str_dst, dict)

        mock_rfts.assert_called_with(str_src)
        mock_ps.assert_called_with('ABC',dict)
        mock_wstf.assert_called_with('ABCD',str_dst)
        pass

    def test_patchString_simple(self):
        str_test = "00001111222233334444"
        dict = {'0000': '0','1111': '1','2222': '2', '3333': '','4444': ''}
        expected = '012'

        str_out = createNewModule.patchString(str_test,dict)

        self.assertEqual(expected,str_out)

    def test_patchString_checkRepeating(self):
        str_test = "00001111222233334444"
        dict = {'0000': '0','0': 'A','1':'10','2222': '2', '3333': '','4444': ''}
        expected = 'A101010102'

        str_out = createNewModule.patchString(str_test,dict)

        self.assertEqual(expected,str_out)

    @patch('createNewModule.processFile')
    def test_createSourceFile_cSrc(self, mock_pf):
        testDesc = TDDConfig.CTestPkgDescription()
        nm = createNewModule.CreateNewModule(testDesc)
        nm.str_LANGUAGE = 'c'
        nm.str_SOURCE_FOLDER = 'SOURCEFOLDER'
        nm.str_SOURCE_FILE = 'SOURCEfile.C'

        nm.createSourceFile()

        self.assertTrue(mock_pf.called)
        pf_args = mock_pf.call_args
        str_src = str(Path('Tools') / 'defaults' / 'src_templates' / 'c_file.c')
        str_dst = str(Path(nm.str_SOURCE_FOLDER) / nm.str_SOURCE_FILE)
        len_dic = 5
        self.assertEqual(str_src, pf_args[0][0])
        self.assertEqual(str_dst, pf_args[0][1])
        self.assertEqual(len_dic, len(pf_args[0][2]))

    @patch('createNewModule.processFile')
    def test_createSourceFile_cSrc(self, mock_pf):
        testDesc = TDDConfig.CTestPkgDescription()
        nm = createNewModule.CreateNewModule(testDesc)
        nm.str_LANGUAGE = 'c++'
        nm.str_SOURCE_FOLDER = 'SOURCEFOLDER'
        nm.str_SOURCE_FILE = 'SOURCEfile.CPP'

        nm.createSourceFile()

        self.assertTrue(mock_pf.called)
        pf_args = mock_pf.call_args
        str_src = str(Path('Tools') / 'defaults' / 'src_templates' / 'class.cpp')
        str_dst = str(Path(nm.str_SOURCE_FOLDER) / nm.str_SOURCE_FILE)
        len_dic = 6
        self.assertEqual(str_src, pf_args[0][0])
        self.assertEqual(str_dst, pf_args[0][1])
        self.assertEqual(len_dic, len(pf_args[0][2]))

    def test_copyAndCreateTestFiles_cTest(self):
        pass
