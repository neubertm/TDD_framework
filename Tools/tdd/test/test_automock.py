from .context import automock as am


import unittest
from unittest.mock import patch, mock_open
from unittest import mock


class TestAutomock(unittest.TestCase):
    
    def test_foo(self):
        self.assertEqual(1,1)
