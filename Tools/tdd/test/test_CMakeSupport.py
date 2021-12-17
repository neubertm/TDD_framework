from .context import cmakeSupport as CS
from .context import TDDConfig as tddc

import unittest
from unittest.mock import patch, mock_open
from unittest import mock

class TestCMakeSupport(unittest.TestCase):

    @patch('cmakeSupport.CCMakeGenerator.closeFile')
    @patch('cmakeSupport.CCMakeGenerator.writeToCMakefileAddFindLinkTestLibrary')
    @patch('cmakeSupport.CCMakeGenerator.writeToCMakefileAddIncludeDirs')
    @patch('cmakeSupport.CCMakeGenerator.writeToCMakefileAddExecutableSection')
    @patch('cmakeSupport.CCMakeGenerator.getSrcTestTempFolderName', return_value='testTmpFldrName')
    @patch('cmakeSupport.CCMakeGenerator.writeToCMakefileUsageOfMemLeakDetectionMacros')
    @patch('cmakeSupport.CCMakeGenerator.writeToCMakefileCoverageSection')
    @patch('cmakeSupport.CCMakeGenerator.writeToCMakefileMinimalRequiredVersion')
    @patch('cmakeSupport.CCMakeGenerator.openFile')
    def test_createCMakeListsFromConfiguration(self,
                                                mock_open,
                                                mock_minVer,
                                                mock_covSect,
                                                mock_memLeak,
                                                mock_fldrName,
                                                mock_execSect,
                                                mock_incDir,
                                                mock_linkLibs,
                                                mock_close):
        cmakeGen = CS.CCMakeGenerator('testFile','testType')


        self.assertEqual('testFile',cmakeGen.fileName)
        self.assertEqual('testType',cmakeGen.str_tType)

        cmakeGen.generate()

        self.assertEqual(1,mock_open.call_count)
        self.assertEqual(1,mock_minVer.call_count)
        self.assertEqual(1,mock_covSect.call_count)
        self.assertEqual(1,mock_memLeak.call_count)
        self.assertEqual(1,mock_fldrName.call_count)
        self.assertEqual(1,mock_execSect.call_count)
        self.assertEqual(1,mock_incDir.call_count)
        self.assertEqual(1,mock_linkLibs.call_count)
        self.assertEqual(1,mock_close.call_count)

        mock_minVer.assert_called_with(3.0)
        mock_execSect.assert_called_with('testTmpFldrName')
        mock_incDir.assert_called_with('testTmpFldrName')



    @patch('cmakeSupport.CCMakeGenerator.writeToFile')
    def test_processAutomockDictionary_cHeader(self, mock_wf):
        cmakeGen = CS.CCMakeGenerator('testFile','testType')
        cmakeGen.AUTOMOCK_dict = {'pooo/Foo.h': 'SRC_TEMP'}

        mock_getSuffix = mock.Mock(return_value='c')

        cmakeGen.processAutomockDictionary(cmakeGen.AUTOMOCK_dict,'TMPSRC',mock_getSuffix)

        mock_wf.assert_called_with('\t${CMAKE_SOURCE_DIR}/TMPSRC/Foo.c\n')
        mock_getSuffix.assert_called_with('h')
        pass

    @patch('cmakeSupport.CCMakeGenerator.writeToFile')
    def test_processAutomockDictionary_cHeader_ignoreNonHeaders(self, mock_wf):
        cmakeGen = CS.CCMakeGenerator('testFile','testType')
        cmakeGen.AUTOMOCK_dict = {'pooo/Foo.h': 'SRC_TEMP', 'pooo/Foo.c': 'SRC_TEMP'}

        mock_getSuffix = mock.Mock(return_value='c')

        cmakeGen.processAutomockDictionary(cmakeGen.AUTOMOCK_dict,'TMPSRC',mock_getSuffix)

        mock_wf.assert_called_with('\t${CMAKE_SOURCE_DIR}/TMPSRC/Foo.c\n')
        mock_getSuffix.assert_called_with('h')
        pass

    @patch('cmakeSupport.CCMakeGenerator.writeToFile')
    def test_processAutomockDictionary_cppHeader(self, mock_wf):
        cmakeGen = CS.CCMakeGenerator('testFile','testType')
        cmakeGen.AUTOMOCK_dict = {'pooo/Foo.h': 'SRC_TEMP'}

        mock_getSuffix = mock.Mock(return_value='cpp')

        cmakeGen.processAutomockDictionary(cmakeGen.AUTOMOCK_dict,'TMPSRC',mock_getSuffix)

        mock_wf.assert_called_with('\t${CMAKE_SOURCE_DIR}/TMPSRC/Foo.cpp\n')
        mock_getSuffix.assert_called_with('h')
        pass


    @patch('cmakeSupport.CCMakeGenerator.processAutomockDictionary')
    @patch('cmakeSupport.getSuffixName')
    def test_writeToCMakefileAddExecutableAutomockFiles(self, mock_gsn, mock_pad):
        cmakeGen = CS.CCMakeGenerator('testFile','testType')
        cmakeGen.testCfg.AUTOMOCK_dict = {'pooo/Foo.h': 'SRC_TEMP'}

        cmakeGen.writeToCMakefileAddExecutableAutomockFiles('TMPSRC')
        mock_pad.assert_called_with(cmakeGen.testCfg.AUTOMOCK_dict,'TMPSRC', mock_gsn)
        pass


    @patch('cmakeSupport.CCMakeGenerator.processAutomockDictionary')
    @patch('cmakeSupport.getSuffixNameAlwaysCpp')
    def test_writeToCMakefileAddExecutableAutomockCppFiles(self, mock_gsn, mock_pad):
        cmakeGen = CS.CCMakeGenerator('testFile','testType')
        cmakeGen.testCfg.AUTOMOCKCPP_dict = {'pooo/Foo.h': 'SRC_TEMP'}

        cmakeGen.writeToCMakefileAddExecutableAutomockCppFiles('TMPSRC')
        mock_pad.assert_called_with(cmakeGen.testCfg.AUTOMOCKCPP_dict,'TMPSRC', mock_gsn)
        pass
