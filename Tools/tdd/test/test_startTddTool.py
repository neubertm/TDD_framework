from .context import startTddTool


import unittest
from unittest.mock import patch

import sys
import os


class TestStartTddTool(unittest.TestCase):

    def test_main_emptyArgs(self):
        test_sriptFldrPath = os.path.dirname(__file__)
        test_envIniFilePath = os.path.abspath(os.path.join(test_sriptFldrPath, 'ini_files', 'envPath.ini'))
        testargs = ['prog', test_envIniFilePath]
        with patch.object(sys, 'argv', testargs):
            startTddTool.main()
        pass


if __name__ == '__main__':
    unittest.main()
