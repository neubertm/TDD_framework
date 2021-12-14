from .context import testAllPkgs as tap
from .context import TDDConfig as tddc
from .context import tdd_support as tdds

import unittest
from unittest.mock import patch

from pathlib import Path
import pathlib

import time

class TestAllPkgs(unittest.TestCase):

    @patch('pathlib.Path.is_dir', return_value=False)
    def test_removeDirectory_folderDoesntExits(self, mock_isDir):
        path_testDir = Path("testDir")
        tap.removeDirectory(path_testDir)
        self.assertTrue(mock_isDir.called)

    @patch('pathlib.Path.is_dir', side_effect=[True, False])
    @patch('tdd_support.del_folder')
    @patch('testAllPkgs.assertWithText')
    def test_removeDirectory_folderExists(self, mock_assert, mock_delFolder, mock_isDir):
        path_testDir = Path("testDir")
        tap.removeDirectory(path_testDir)

        self.assertEqual(2,len(mock_isDir.call_args_list))
        self.assertEqual(1,len(mock_delFolder.call_args_list))
        self.assertEqual(1,len(mock_assert.call_args_list))
        #self.assertTrue(mock_isDir.called)

    @patch('testAllPkgs.CTestPkg.__writeStep__')
    @patch('testAllPkgs.CTestPkg.__writeStatus__')
    @patch('testAllPkgs.CTestPkg.__readInit__')
    @patch('testAllPkgs.CTestPkg.__createCmake__')
    @patch('testAllPkgs.CTestPkg.__cleanTmpSource__')
    @patch('testAllPkgs.CTestPkg.__fileCopying__')
    @patch('testAllPkgs.CTestPkg.__automocks__')
    @patch('testAllPkgs.CTestPkg.__cmake__')
    @patch('testAllPkgs.CTestPkg.__make__', return_value = True)
    @patch('testAllPkgs.CTestPkg.__runTestBin__', return_value = True)
    @patch('testAllPkgs.CTestPkg.__codeEvaluation__')
    @patch('time.sleep')
    @patch('testAllPkgs.CTestPkg.__checkExternalTerminationCondition__', return_value = False)
    def test_runTest_OK_terminationInFirstLoop(self,
                                                mock_checkCond,
                                                mock_sleep,
                                                mock_codeEval,
                                                mock_rtb,
                                                mock_make,
                                                mock_cmake,
                                                mock_automocks,
                                                mock_fCp,
                                                mock_cts,
                                                mock_cc,
                                                mock_ri,
                                                mock_wStatus,
                                                mock_wStep):
        mainConfing = tddc.CMainConfig()
        o_testPkg = tap.CTestPkg('testName', mainConfing, None)
        o_testPkg.__runTest__()

        mock_wStep_args_lst = mock_wStep.call_args_list
        mock_wStep_args_lst[0].assert_called_with('Start')
        mock_wStep_args_lst[1].assert_called_with('Finished')

        mock_wStatus_args_lst = mock_wStatus.call_args_list
        mock_wStatus_args_lst[0].assert_called_with('Run')
        mock_wStatus_args_lst[1].assert_called_with('Idle')

        self.assertEqual(1,mock_ri.call_count)
        self.assertEqual(1,mock_cc.call_count)
        self.assertEqual(1,mock_cts.call_count)
        self.assertEqual(1,mock_fCp.call_count)
        self.assertEqual(1,mock_automocks.call_count)
        self.assertEqual(1,mock_cmake.call_count)
        self.assertEqual(1,mock_make.call_count)
        self.assertEqual(1,mock_rtb.call_count)
        self.assertEqual(1,mock_codeEval.call_count)
        self.assertEqual(1,mock_sleep.call_count)
        self.assertEqual(1,mock_checkCond.call_count)


    @patch('testAllPkgs.CTestPkg.__writeStep__')
    @patch('testAllPkgs.CTestPkg.__writeStatus__')
    @patch('testAllPkgs.CTestPkg.__readInit__')
    @patch('testAllPkgs.CTestPkg.__createCmake__')
    @patch('testAllPkgs.CTestPkg.__cleanTmpSource__')
    @patch('testAllPkgs.CTestPkg.__fileCopying__')
    @patch('testAllPkgs.CTestPkg.__automocks__')
    @patch('testAllPkgs.CTestPkg.__cmake__')
    @patch('testAllPkgs.CTestPkg.__make__', return_value = True)
    @patch('testAllPkgs.CTestPkg.__runTestBin__', return_value = True)
    @patch('testAllPkgs.CTestPkg.__codeEvaluation__')
    @patch('time.sleep')
    @patch('testAllPkgs.CTestPkg.__checkExternalTerminationCondition__', return_value = True)
    @patch('testAllPkgs.CTestPkg.__checkIniFileChanged__', return_value = True)
    @patch('testAllPkgs.CTestPkg.__cleanStatusVariables__')
    def test_runTest_OK_terminationBecauseInifileUpdated(self,
                                                mock_csv,
                                                mock_checkIni,
                                                mock_checkCond,
                                                mock_sleep,
                                                mock_codeEval,
                                                mock_rtb,
                                                mock_make,
                                                mock_cmake,
                                                mock_automocks,
                                                mock_fCp,
                                                mock_cts,
                                                mock_cc,
                                                mock_ri,
                                                mock_wStatus,
                                                mock_wStep):
        mainConfing = tddc.CMainConfig()
        o_testPkg = tap.CTestPkg('testName', mainConfing, None)
        o_testPkg.__runTest__()

        mock_wStep_args_lst = mock_wStep.call_args_list
        mock_wStep_args_lst[0].assert_called_with('Start')
        mock_wStep_args_lst[1].assert_called_with('Finished')

        mock_wStatus_args_lst = mock_wStatus.call_args_list
        mock_wStatus_args_lst[0].assert_called_with('Run')
        mock_wStatus_args_lst[1].assert_called_with('Idle')

        self.assertEqual(1,mock_ri.call_count)
        self.assertEqual(1,mock_cc.call_count)
        self.assertEqual(1,mock_cts.call_count)
        self.assertEqual(1,mock_fCp.call_count)
        self.assertEqual(1,mock_automocks.call_count)
        self.assertEqual(1,mock_cmake.call_count)
        self.assertEqual(1,mock_make.call_count)
        self.assertEqual(1,mock_rtb.call_count)
        self.assertEqual(1,mock_codeEval.call_count)
        self.assertEqual(1,mock_sleep.call_count)
        self.assertEqual(1,mock_checkCond.call_count)
        self.assertEqual(1,mock_checkIni.call_count)
        self.assertEqual(1,mock_csv.call_count)


    @patch('testAllPkgs.CTestPkg.__writeStep__')
    @patch('testAllPkgs.CTestPkg.__writeStatus__')
    @patch('testAllPkgs.CTestPkg.__readInit__')
    @patch('testAllPkgs.CTestPkg.__createCmake__')
    @patch('testAllPkgs.CTestPkg.__cleanTmpSource__')
    @patch('testAllPkgs.CTestPkg.__fileCopying__')
    @patch('testAllPkgs.CTestPkg.__automocks__')
    @patch('testAllPkgs.CTestPkg.__cmake__')
    @patch('testAllPkgs.CTestPkg.__make__', side_effect = [True, True])
    @patch('testAllPkgs.CTestPkg.__runTestBin__', side_effect = [True, True])
    @patch('testAllPkgs.CTestPkg.__codeEvaluation__')
    @patch('time.sleep')
    @patch('testAllPkgs.CTestPkg.__checkExternalTerminationCondition__', side_effect = [True, False])
    @patch('testAllPkgs.CTestPkg.__checkIniFileChanged__', return_value = False)
    @patch('testAllPkgs.CTestPkg.__checkSrcFileChanged__', return_value = True)
    @patch('testAllPkgs.CTestPkg.__cleanStatusVariables__')
    @patch('testAllPkgs.CTestPkg.__fileCopyingUpdatedOnly__')
    @patch('testAllPkgs.CTestPkg.__updateAutomocks__')
    @patch('testAllPkgs.CTestPkg.__cleanScreenBeforeRerun__')
    def test_runTest_OK_changedSourceFilesAndTerminate(self,
                                                mock_cleanScreen,
                                                mock_updateAutomock,
                                                mock_fcuo,
                                                mock_cleanStat,
                                                mock_checkSrc,
                                                mock_checkIni,
                                                mock_checkCond,
                                                mock_sleep,
                                                mock_codeEval,
                                                mock_rtb,
                                                mock_make,
                                                mock_cmake,
                                                mock_automocks,
                                                mock_fCp,
                                                mock_cts,
                                                mock_cc,
                                                mock_ri,
                                                mock_wStatus,
                                                mock_wStep):
        mainConfing = tddc.CMainConfig()
        o_testPkg = tap.CTestPkg('testName', mainConfing, None)
        o_testPkg.__runTest__()

        mock_wStep_args_lst = mock_wStep.call_args_list
        mock_wStep_args_lst[0].assert_called_with('Start')
        mock_wStep_args_lst[1].assert_called_with('Finished')

        mock_wStatus_args_lst = mock_wStatus.call_args_list
        mock_wStatus_args_lst[0].assert_called_with('Run')
        mock_wStatus_args_lst[1].assert_called_with('Idle')

        self.assertEqual(1,mock_ri.call_count)
        self.assertEqual(1,mock_cc.call_count)
        self.assertEqual(1,mock_cts.call_count)
        self.assertEqual(1,mock_fCp.call_count)
        self.assertEqual(1,mock_automocks.call_count)
        self.assertEqual(1,mock_cmake.call_count)
        self.assertEqual(2,mock_make.call_count)
        self.assertEqual(2,mock_rtb.call_count)
        self.assertEqual(2,mock_codeEval.call_count)
        self.assertEqual(2,mock_sleep.call_count)
        self.assertEqual(2,mock_checkCond.call_count)
        self.assertEqual(1,mock_checkIni.call_count)
        self.assertEqual(1,mock_cleanScreen.call_count)
        self.assertEqual(1,mock_updateAutomock.call_count)
        self.assertEqual(1,mock_fcuo.call_count)
        self.assertEqual(1,mock_cleanStat.call_count)
        self.assertEqual(1,mock_checkSrc.call_count)
