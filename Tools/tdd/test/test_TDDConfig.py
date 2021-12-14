from .context import TDDConfig

from pathlib import Path
import unittest

class TestTDDConfig(unittest.TestCase):

    def test_CTestToolchainCfgCtor(self):
        o_tChainCfg = TDDConfig.CTestToolchainCfg()
        self.assertEqual(o_tChainCfg.str_compiler,"gcc")
        self.assertEqual(o_tChainCfg.str_testlib,"cpputest")
        self.assertEqual(o_tChainCfg.str_automock,'cppumockgen')


    def test_CTestConfigCtor(self):
        o_testCfg = TDDConfig.CTestConfig()
        self.assertEqual(o_testCfg.SUT_dict,{})
        self.assertEqual(o_testCfg.OTHER_dict,{})
        self.assertEqual(o_testCfg.AUTOMOCK_dict,{})
        self.assertEqual(o_testCfg.AUTOMOCKCPP_dict,{})
        self.assertEqual(o_testCfg.AUTOMOCKFLDRINC_lst,[])
        self.assertEqual(type(o_testCfg.co_coverage), type(TDDConfig.CCovCfg() ) )
        self.assertEqual(type(o_testCfg.co_staticAnalysis), type(TDDConfig.CStaticAnalysisCfg() ) )
        self.assertEqual(type(o_testCfg.co_guidelineFormat), type(TDDConfig.CFormaterGuidelineCheckerCfg() ) )
        self.assertEqual(type(o_testCfg.co_testToolchain), type(TDDConfig.CTestToolchainCfg() ) )
        self.assertEqual(type(o_testCfg.co_codeStatistics), type(TDDConfig.CCodeStatisticsCfg() ) )

    def test_CTestConfig_checkReadTestFile(self):
        o_testCfg = TDDConfig.CTestConfig()
        o_testCfg.readCfgFile(Path('test') / 'testingData' / 'testWithAutomock.ini')
        self.assertEqual(o_testCfg.AUTOMOCK_dict,{'FOOOO/POOO/ZOO.h': 'SRC_TEMP'})
        self.assertEqual(o_testCfg.AUTOMOCKCPP_dict,{'FOOOO/POOO/ZOOO.hpp': 'SRC_TEMP'})
        self.assertEqual(o_testCfg.AUTOMOCKFLDRINC_lst,['FOOOO/POOO/INCLUDE'])
