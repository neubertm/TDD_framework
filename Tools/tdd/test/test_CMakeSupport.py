from .context import cmakeSupport as CS
from .context import TDDConfig as tddc

import unittest
from unittest.mock import patch, mock_open

class TestCMakeSupport(unittest.TestCase):

    @patch('cmakeSupport.writeToCMakefileAddFindLinkTestLibrary')
    @patch('cmakeSupport.writeToCMakefileAddIncludeDirs')
    @patch('cmakeSupport.writeToCMakefileAddExecutableSection')
    @patch('cmakeSupport.getSrcTestTempFolderName', return_value='testTmpFldrName')
    @patch('cmakeSupport.writeToCMakefileUsageOfMemLeakDetectionMacros')
    @patch('cmakeSupport.writeToCMakefileCoverageSection')
    @patch('cmakeSupport.writeToCMakefileMinimalRequiredVersion')
    @patch('builtins.open', new_callable=mock_open)
    def test_createCMakeListsFromConfiguration(self,
                                                mock_bopen,
                                                mock_minVer,
                                                mock_covSect,
                                                mock_memLeak,
                                                mock_fldrName,
                                                mock_execSect,
                                                mock_incDir,
                                                mock_linkLibs):
        mCfg = tddc.CMainConfig()
        tCfg = tddc.CTestConfig()
        CS.createCMakeListsFromConfiguration('testFile', mCfg, tCfg, 'testType')

        mock_bopen.assert_called_with('testFile','w')

        # mock_minVer.assert_called_with(mock_bopen,3.0)
        args, kwargs = mock_minVer.call_args
        print(args[1])
        print(args[0])
        print(mock_open)
        print(mock_bopen)
        self.assertEqual(args[1],3.0)

        args, kwargs = mock_covSect.call_args
        # mock_covSectLst[0].assert_called_with((mock_open,tCfg))
        self.assertEqual(args[1],tCfg)

        args, kwargs = mock_memLeak.call_args
        self.assertEqual(args[1],tCfg)
        # mock_memLeakLst = mock_memLeak.call_args_list
        # mock_memLeakLst[0].assert_called_with((mock_open,tCfg))

        mock_fldrName.assert_called_with(tCfg,mCfg,'testType')

        args, kwargs = mock_execSect.call_args
        #self.assertEqual(args[1:],(tCfg,mCfg,'testTmpFldrName'))
        self.assertEqual(args[1:],(tCfg,mCfg,'testTmpFldrName'))




        pass
    pass
