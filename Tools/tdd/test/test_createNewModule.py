from .context import createNewModule

import unittest
from unittest.mock import patch

import sys
import os


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
        newModule = createNewModule.CreateNewModule()
        self.assertEqual(newModule.str_SRC_FOLDER,"")
        self.assertEqual(newModule.str_HEADER_FOLDER,"")
        self.assertEqual(newModule.str_FRAMEWORK,"cpputest")
        self.assertEqual(newModule.str_TOOLCHAIN,"mingw")
        self.assertEqual(newModule.str_LANGUAGE,"c++")
        self.assertEqual(newModule.str_COMPONENT_NAME,"")
        self.assertEqual(newModule.str_SRC_TYPE,"")

    def test_createNewModule_setSourceCodeType(self):
        
        pass
