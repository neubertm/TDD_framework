from .context import automock as am

from pathlib import Path

import unittest
from unittest.mock import patch, mock_open
from unittest import mock


class TestAutomock(unittest.TestCase):

    def test_stripComments_CPP_simple_unixformat(self):
        str_test = 'fooo\n//aa\npooo'
        str_stripped = am.stripCppComments(str_test)
        self.assertEqual('fooo\npooo',str_stripped)

    def test_stripComments_CPP_simple_winformat(self):
        str_test = 'fooo\r\n//aa\r\npooo'
        str_stripped = am.stripCppComments(str_test)
        self.assertEqual('fooo\r\npooo',str_stripped)

    def test_stripComments_CPP_simple(self):
        str_test = 'fooo\n//aa\npooo'
        str_stripped = am.stripCppComments(str_test)
        self.assertEqual('fooo\npooo',str_stripped)

    def test_stripComments_mix_C_CPP_simple(self):
        str_test = 'fooo\n//aa\npooo ///*\n */'
        str_stripped = am.stripCppComments(str_test)
        self.assertEqual('fooo\npooo  */',str_stripped)

    def test_stripComments_mix_C_CPP_advanced(self):
        str_test = 'fooo\n//aa\npooo /*\n\n\n\n\n// */a'
        str_stripped = am.stripCppComments(str_test)
        self.assertEqual('fooo\npooo a',str_stripped)

    def test_removeTabs_default(self):
        N = 4
        str_test = '\tTEST0\t\n\t\tTEST1\n\t\t\tTEST2\n'
        str_result = (N * ' ') + 'TEST0'+ (N * ' ') + '\n' + (2*N * ' ') + 'TEST1' + '\n' + (3*N * ' ') + 'TEST2\n'
        str_remTab = am.removeTabs(str_test)
        self.assertEqual(str_result, str_remTab)

    def test_removeTabs_defaultIsFour(self):
        N = 4
        str_test = '\tTEST0\t\n\t\tTEST1\n\t\t\tTEST2\n'
        str_result = (N * ' ') + 'TEST0'+ (N * ' ') + '\n' + (2*N * ' ') + 'TEST1' + '\n' + (3*N * ' ') + 'TEST2\n'
        str_remTab = am.removeTabs(str_test,4)
        self.assertEqual(str_result, str_remTab)

    def test_removeTabs_2default(self):
        N = 2*4
        str_test = '\tTEST0\t\n\t\tTEST1\n\t\t\tTEST2\n'
        str_result = (N * ' ') + 'TEST0'+ (N * ' ') + '\n' + (2*N * ' ') + 'TEST1' + '\n' + (3*N * ' ') + 'TEST2\n'
        str_remTab = am.removeTabs(str_test,N)
        self.assertEqual(str_result, str_remTab)

    def test_numOfClassesInHeader_simple(self):
        app = am.AutomockPostprocessor(Path(),Path())
        str_test = '\nclass foo{}\nclasspoo{}'
        self.assertEqual(1,app.getNumOfClassesInHeader(str_test))

    def test_numOfClassesInHeader_nestedClasses(self):
        app = am.AutomockPostprocessor(Path(),Path())
        str_test = '\nclass foo{\n    class poo{\n}\n}'
        self.assertEqual(2,app.getNumOfClassesInHeader(str_test))

    def test_numOfClassesInHeader_2NormalClasses(self):
        app = am.AutomockPostprocessor(Path(),Path())
        str_test = '\nclass foo{\n}\nclass poo{\n}\n'
        self.assertEqual(2,app.getNumOfClassesInHeader(str_test))

    def test_getAllClassesInHeader_Normal(self):
        str_test = '\nclass foo{\n}\nclass poo{\n}\n'
        self.assertEqual([(0, 7), (13, 20)],am.getAllClassesInHeader(str_test))

    def test_CppClassInfo_constructorCheck(self):
        str_test = '\nfoo{\n}\nclassd poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(o_classInfo.fullHeader, str_test)
        self.assertEqual(o_classInfo.fullClass, '')
        self.assertEqual(o_classInfo.name, '')
        self.assertEqual(o_classInfo.name_s, 0)
        self.assertEqual(o_classInfo.name_e, 0)
        self.assertEqual(o_classInfo.inheritance, '')
        self.assertEqual(o_classInfo.inheritance_s, 0)
        self.assertEqual(o_classInfo.inheritance_e, 0)
        self.assertEqual(o_classInfo.body, '')
        self.assertEqual(o_classInfo.body_s, 0)
        self.assertEqual(o_classInfo.body_e, 0)
        self.assertEqual(o_classInfo.rest, '')
        self.assertEqual(o_classInfo.int_classLable_s, -1)
        self.assertEqual(o_classInfo.int_classLable_e, -1)
        self.assertEqual(o_classInfo.ctors, [])
        self.assertEqual(o_classInfo.dtors, [])
        self.assertEqual(o_classInfo.innerClassLst, [])


    def test_CppClassInfo_findClassLabel_errorMissingLbl(self):
        str_test = '\nfoo{\n}\nclassd poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(False, o_classInfo.findClassLabel())
        self.assertEqual(o_classInfo.int_classLable_s, -1)
        self.assertEqual(o_classInfo.int_classLable_e, -1)


    def test_CppClassInfo_findClassLabel_oneLabel(self):
        str_test = '\nfoo{\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        self.assertEqual(o_classInfo.int_classLable_s, 7)
        self.assertEqual(o_classInfo.int_classLable_e, 14)


    def test_CppClassInfo_findClassLabel_twoLabelsGetFirst(self):
        str_test = '\nclass foo{\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        self.assertEqual(o_classInfo.int_classLable_s, 0)
        self.assertEqual(o_classInfo.int_classLable_e, 7)


    def test_CppClassInfo_findClassLabel_twoLabelsGetFirstNoCharBefore(self):
        str_test = 'class foo{\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        self.assertEqual(o_classInfo.int_classLable_s, 0)
        self.assertEqual(o_classInfo.int_classLable_e, 6)

    @patch('automock.automock_assert')
    def test_CppClassInfo_findClassName_simple(self,mock_assert):
        str_test = '\nclass foo{\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)

        self.assertEqual(o_classInfo.name, 'foo')

    @patch('automock.automock_assert')
    def test_CppClassInfo_findClassName_simpleWithInheritance(self,mock_assert):
        str_test = '\nclass foo: public poo\n{\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)

        self.assertEqual(o_classInfo.name, 'foo')

    @patch('automock.automock_assert')
    def test_CppClassInfo_findClassName_simpleWithMultipleInheritance(self,mock_assert):
        str_test = '\nclass foo: public poo, private boo\n{\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)

        self.assertEqual(o_classInfo.name, 'foo')


    @patch('automock.automock_assert')
    def test_CppClassInfo_recognizeInheritance_multipleInheritance(self,mock_assert):
        str_test = '\nclass foo: public poo, private boo\n{\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()
        o_classInfo.recognizeInheritanceSection()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(True, mock_assert.call_args_list[2][0][0])
        self.assertEqual('Missing class declaration.', mock_assert.call_args_list[2][0][1])

        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)
        self.assertEqual(o_classInfo.name, 'foo')

        self.assertEqual(10, o_classInfo.inheritance_s)
        self.assertEqual(36, o_classInfo.inheritance_e)
        self.assertEqual(o_classInfo.inheritance, ': public poo, private boo\n')


    @patch('automock.automock_assert')
    def test_CppClassInfo_recognizeInheritance_simpleInheritance(self,mock_assert):
        str_test = '\nclass foo: public poo {\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()
        o_classInfo.recognizeInheritanceSection()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(True, mock_assert.call_args_list[2][0][0])
        self.assertEqual('Missing class declaration.', mock_assert.call_args_list[2][0][1])

        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)
        self.assertEqual(o_classInfo.name, 'foo')

        self.assertEqual(10, o_classInfo.inheritance_s)
        self.assertEqual(23, o_classInfo.inheritance_e)
        self.assertEqual(o_classInfo.inheritance, ': public poo ')


    @patch('automock.automock_assert')
    def test_CppClassInfo_findEndOfClassDeclaration_simple(self,mock_assert):
        str_test = '\nclass foo: public poo {public:\n  calc(int);\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()
        o_classInfo.recognizeInheritanceSection()
        o_classInfo.findEndOfClassDeclaration()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(True, mock_assert.call_args_list[2][0][0])
        self.assertEqual('Missing class declaration.', mock_assert.call_args_list[2][0][1])

        self.assertEqual(True, mock_assert.call_args_list[3][0][0])
        self.assertEqual('Missing class termination.', mock_assert.call_args_list[3][0][1])

        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)
        self.assertEqual(o_classInfo.name, 'foo')

        self.assertEqual(10, o_classInfo.inheritance_s)
        self.assertEqual(23, o_classInfo.inheritance_e)
        self.assertEqual(o_classInfo.inheritance, ': public poo ')

        self.assertEqual(23, o_classInfo.body_s)
        self.assertEqual(45, o_classInfo.body_e)
        self.assertEqual(o_classInfo.body, '{public:\n  calc(int);\n')


    @patch('automock.automock_assert')
    def test_CppClassInfo_findEndOfClassDeclaration_error(self,mock_assert):
        str_test = '\nclass foo: public poo {public:\n  calc(int);\n\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()
        o_classInfo.recognizeInheritanceSection()
        o_classInfo.findEndOfClassDeclaration()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(True, mock_assert.call_args_list[2][0][0])
        self.assertEqual('Missing class declaration.', mock_assert.call_args_list[2][0][1])

        self.assertEqual(False, mock_assert.call_args_list[3][0][0])
        self.assertEqual('Missing class termination.', mock_assert.call_args_list[3][0][1])

        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)
        self.assertEqual(o_classInfo.name, 'foo')

        self.assertEqual(10, o_classInfo.inheritance_s)
        self.assertEqual(23, o_classInfo.inheritance_e)
        self.assertEqual(o_classInfo.inheritance, ': public poo ')

        self.assertEqual(23, o_classInfo.body_s)
        self.assertEqual(-1, o_classInfo.body_e)


    @patch('automock.automock_assert')
    def test_CppClassInfo_fillRestOfStringVars_simple(self,mock_assert):
        str_test = '\nclass foo: public poo {public:\n  calc(int);\n}\nclass poo{\n}\n'
        o_classInfo = am.CppClassInfo(str_test)
        self.assertEqual(True, o_classInfo.findClassLabel())
        o_classInfo.findClassName()
        o_classInfo.recognizeInheritanceSection()
        o_classInfo.findEndOfClassDeclaration()
        o_classInfo.fillRestOfStringVars()

        self.assertEqual(True, mock_assert.call_args_list[0][0][0])
        self.assertEqual('Class name missing.', mock_assert.call_args_list[0][0][1])

        self.assertEqual(True, mock_assert.call_args_list[1][0][0])
        self.assertEqual('Class name is strange.', mock_assert.call_args_list[1][0][1])

        self.assertEqual(True, mock_assert.call_args_list[2][0][0])
        self.assertEqual('Missing class declaration.', mock_assert.call_args_list[2][0][1])

        self.assertEqual(True, mock_assert.call_args_list[3][0][0])
        self.assertEqual('Missing class termination.', mock_assert.call_args_list[3][0][1])

        self.assertEqual(0, o_classInfo.int_classLable_s)
        self.assertEqual(7, o_classInfo.int_classLable_e)


        self.assertEqual(7, o_classInfo.name_s)
        self.assertEqual(10, o_classInfo.name_e)
        self.assertEqual(o_classInfo.name, 'foo')

        self.assertEqual(10, o_classInfo.inheritance_s)
        self.assertEqual(23, o_classInfo.inheritance_e)
        self.assertEqual(o_classInfo.inheritance, ': public poo ')

        self.assertEqual(23, o_classInfo.body_s)
        self.assertEqual(45, o_classInfo.body_e)
        self.assertEqual(o_classInfo.body, '{public:\n  calc(int);\n')

        self.assertEqual(o_classInfo.fullClass,str_test[o_classInfo.int_classLable_s:o_classInfo.body_e])
        self.assertEqual(o_classInfo.rest,str_test[o_classInfo.body_e:])

    @patch('automock.CppClassInfo.findClassLabel', return_value=False)
    def test_cppClassInfo_processClassHeader_findClassLabel_Failed(self,mock_fcl):
        o_classInfo = am.CppClassInfo('fakeString')
        self.assertEqual(False, o_classInfo.processClassHeader())
        self.assertTrue(mock_fcl.called)


    @patch('automock.CppClassInfo.findSubclasses')
    @patch('automock.CppClassInfo.evalAllCtors')
    @patch('automock.CppClassInfo.evalAllDtors')
    @patch('automock.CppClassInfo.fillRestOfStringVars')
    @patch('automock.CppClassInfo.findEndOfClassDeclaration')
    @patch('automock.CppClassInfo.recognizeInheritanceSection')
    @patch('automock.CppClassInfo.findClassName')
    @patch('automock.CppClassInfo.findClassLabel', return_value=True)
    def test_cppClassInfo_processClassHeader_correct(self,mock_fcl, mock_fcn, mock_ris, mock_feocd,mock_frosv, mock_ead,mock_eac, mock_fs):
        o_classInfo = am.CppClassInfo('fakeString')
        self.assertEqual(True, o_classInfo.processClassHeader())

        self.assertTrue(mock_fs.called)
        self.assertTrue(mock_fcl.called)
        self.assertTrue(mock_fcn.called)
        self.assertTrue(mock_ris.called)
        self.assertTrue(mock_feocd.called)
        self.assertTrue(mock_frosv.called)
        self.assertTrue(mock_ead.called)
        self.assertTrue(mock_eac.called)


    @patch('automock.CppClassInfo.findClassLabel', return_value=False)
    def test_cppClassInfo_processClassHeader_labelFailed(self, mock_fcl):
        o_classInfo = am.CppClassInfo('fakeString')
        self.assertEqual(False, o_classInfo.processClassHeader())

        self.assertTrue(mock_fcl.called)


    @patch('automock.CppClassInfo.findCtorDecl')
    @patch('automock.CppClassInfo.findCtorDefinitions')
    def test_cppClassInfo_evalAllCtors(self, mock_def, mock_decl):
        o_cppClassInfo = am.CppClassInfo('fakeString',-1)

        o_cppClassInfo.evalAllCtors()
        self.assertTrue(mock_def.called)
        self.assertTrue(mock_decl.called)


    @patch('automock.CppClassInfo.findDtorDecl')
    @patch('automock.CppClassInfo.findDtorDefinitions')
    def test_cppClassInfo_evalAllDtors(self, mock_def, mock_decl):
        o_cppClassInfo = am.CppClassInfo('fakeString',-1)

        o_cppClassInfo.evalAllDtors()
        self.assertTrue(mock_def)
        self.assertTrue(mock_decl)


    def test_cppClassInfo_findCtorDecl_noCTOR(self):
        o_cppClassInfo = am.CppClassInfo('fakeString',-1)
        o_cppClassInfo.body = 'fooooooooo'
        o_cppClassInfo.name = 'TestClass'

        o_cppClassInfo.findCtorDecl()

        self.assertTrue([] == o_cppClassInfo.ctorNotDefinedLst)

    def test_cppClassInfo_findCtorDecl_1CTOR(self):
        o_cppClassInfo = am.CppClassInfo('fakeString',-1)
        o_cppClassInfo.body = 'explicit TestClass(int foo); explicit TestClass() {} explicit TestClass(const int i32_dta, int* pi32_dta2); '
        o_cppClassInfo.name = 'TestClass'

        o_cppClassInfo.findCtorDecl()

        #print(o_cppClassInfo.ctorNotDefinedLst)
        # self.assertTrue(2 == len(o_cppClassInfo.ctorNotDefinedLst) )
        for classStr in o_cppClassInfo.ctorNotDefinedLst:
            print(o_cppClassInfo.body[classStr[0]:classStr[1]])
        #self.assertTrue((0,17) == o_cppClassInfo.ctorNotDefinedLst[0] )
