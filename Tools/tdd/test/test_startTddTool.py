from .context import startTddTool
from .context import mainMenu


import unittest
from unittest.mock import patch

import sys
import os


class TestStartTddTool(unittest.TestCase):

    def test_main_emptyArgs(self):
        test_sriptFldrPath = os.path.dirname(__file__)
        test_envIniFilePath = os.path.abspath(os.path.join(test_sriptFldrPath, 'ini_files', 'envPath.ini'))
        test_testSetupFilePath = os.path.abspath(os.path.join(test_sriptFldrPath, 'ini_files', 'testSetups.ini'))
        testargs = ['prog', test_envIniFilePath, test_testSetupFilePath]
        with patch.object(sys, 'argv', testargs):
            with patch("mainMenu.MainMenu.createAndShow") as mock_createAndShow:
                startTddTool.main()
        pass


if __name__ == '__main__':
    unittest.main()
