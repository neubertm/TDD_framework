from pathlib import Path
import subprocess
import re

import clang.cindex

def setPathToCLang(str_CLangPath):
    '''
    Set path to clang lib in libclang(python-module)
    '''
    clang.cindex.Config.set_library_path(str_CLangPath)

def getListOfUndefinedCtors(cursor, ctorLst):
    if ( ( cursor.kind == clang.cindex.CursorKind.CONSTRUCTOR ) and
         ( not cursor.is_definition() ) and
         ( None == cursor.get_definition() ) and
         ( not cursor.is_default_method() ) ):
         ctorLst.append(cursor)

    for iCursor in cursor.get_children():
        getListOfUndefinedCtors(iCursor,ctorLst)

def parseCode(str_FileName,args=['-std=c++11']):
    index = clang.cindex.Index.create()
    tr_unit = index.parse(str_FileName,args)
    return tr_unit


def getAllClassesInHeader(strHeader):
    '''
    Function returns list of class keywords in source code.
    Valid code and removed comments are necessary.
    Unit tested (indirectly)
    '''
    classPatern = '((^|\s)class\s)'
    return [ (m.start(0), m.end(0)) for m in re.finditer(classPatern, strHeader)]

def automock_assert(condition, str_text):
    '''
    Local assertion function for mocking purpose
    '''
    assert condition, str_text

def createAutomocks(mockDict,incLst,strCppStd = 'c++11', strCStd = 'c99', forcedCpp = False):
    '''
    This function create mock file for whole mock dictionary,
    it has default parameters and call creating function for each specific item.
    '''
    for key in mockDict:
        callAutomockTool(key, mockDict[key], incLst, strCppStd, strCStd, forcedCpp)

# def getPathAutomockTool():
#     '''
#     Function returning path to CppUMockGen, but in future will not be hardcoded but store as other tool in configuration file
#     '''
#     return Path('Tools') / 'programs' / 'CppUMockGen-0.4-win64' / 'bin' / 'CppUMockGen'

def callAutomockTool(headerName, mockName, incList, strCppStd, strCStd, forcedCpp):
    '''
    Function call automock tool for generating basic(not patched mock)
    '''
    #str_PathCppUMockGen = getPathAutomockTool()
    str_PathCppUMockGen = "CppUMockGen"
    op_lst = [str(str_PathCppUMockGen)]

    # i is input
    op_lst.append('--input')
    op_lst.append(headerName)

    # m is mocked file
    op_lst.append('--mock-output')
    op_lst.append(mockName)

    # forced cpp
    if True == forcedCpp:
        op_lst.append('--cpp')
        op_lst.append('--std')
        op_lst.append(strCppStd)
    else:
        op_lst.append('--std')
        op_lst.append(strCStd)

    for incPath in incList:
        op_lst.append('--include-path')
        op_lst.append(incPath)

    # print(op_lst)
    subprocess.call(op_lst, shell=True)


def processMockDictionary(dict, subsDict, fnc_suffix):
    '''
        This function accept input dictionary where key is header file and
        create/get position of header file location and create mock for header.
    '''
    # 'source location' of header file
    srcLst = []
    # 'destination location' of header file
    dstLst = []
    # dictionary contains as key source location and mocked file
    mockDict = {}
    #for each header file do
    for key in dict:
        procKey = patchStrByDict(key, subsDict)
        procVal = patchStrByDict(dict[key], subsDict)
        pathSrc = Path(procKey)
        str_SrcFileName = pathSrc.name
        str_SrcSuffix = pathSrc.suffix
        str_SrcStripName = str_SrcFileName.replace(pathSrc.suffix, '')
        pathDst = Path(procVal)
        dstFileName = ''
        if '' != pathDst.suffix:
            #extract file name
            dstFileName = pathDst.name
            #remove filename from path
            pathDst = pathDst.parents[0]

        pathHeaderDst = pathDst / str_SrcFileName
        pathMockDst = pathDst / (str_SrcStripName + '_MOCK.' + fnc_suffix(str_SrcSuffix))

        srcLst.append(procKey)
        dstLst.append(str(pathHeaderDst))
        mockDict[procKey] = str(pathMockDst)

    return srcLst, dstLst, mockDict

class BasicFunction():
    name: str
    namespace: str
    retType: str
    argsList: [(str,str)]
    declPreAtrib: str
    def __init__(self):
        self.name = ''
        self.namespace = ''
        self.retType = ''
        self.argsList = []
        self.declPostAtrib = ''
        self.declPreAtrib = ''

class CtorFunction(BasicFunction):
    def __init__(self, name: str):
        BasicFunction.__init__()
        self.name = name
        self.retType = None
    pass

class DtorFunction(BasicFunction):
    def __init__(self, name: str):
        BasicFunction.__init__()
        self.name = '~' + name
        self.retType = None
    pass

class CppClassInfo():
    fullHeader: str
    fullClass: str
    name: str
    name_s: int
    name_e: int
    inheritance: str
    inheritance_s: int
    inheritance_e: int
    body: str
    body_s: int
    body_e: int
    rest: str
    int_classLable_s: int
    int_classLable_e: int
    ctors: [CtorFunction]
    dtors: [DtorFunction]
    # innerClassLst: [CppClassInfo] python does not have forward declaration
    innerClassLst: []

    def __init__(self, str_fullHeader: str, classLbl_s=-1):
        self.fullHeader = str_fullHeader
        self.fullClass = ''
        self.name = ''
        self.name_s = 0
        self.name_e = 0
        self.inheritance = ''
        self.inheritance_s = 0
        self.inheritance_e = 0
        self.body = ''
        self.body_s = 0
        self.body_e = 0
        self.rest = ''
        self.int_classLable_s = classLbl_s
        self.int_classLable_e = classLbl_s
        self.ctors = []
        self.dtors = []
        self.innerClassLst = []
        self.ctorNotDefinedLst = []

    def findClassLabel(self):
        '''
        Function find start index of class lbl based on defined classLbl_s. if its -1 it start from zero.
        Unit tested: ok
        '''
        b_retval = True
        startIndex = 0
        if self.int_classLable_s > 0:
            startIndex = self.int_classLable_s

        fnc_list = getAllClassesInHeader(self.fullHeader[startIndex:])
        if len(fnc_list) > 0:
            self.int_classLable_s = fnc_list[0][0]
            self.int_classLable_e = fnc_list[0][1]
            pass
        else:
            self.int_classLable_s = -1
            self.int_classLable_e = -1
            b_retval = False
            pass
        return b_retval

    def findClassName(self):
        '''
        Function find separate class name
        UT: ok
        '''
        self.name_s = -1
        for indexCH, CH in enumerate(self.fullHeader[self.int_classLable_e:]):
            if CH != ' ':
                self.name_s = indexCH + self.int_classLable_e
                break
        automock_assert(self.name_s != -1, 'Class name missing.')

        self.name_e = -1
        for indexCH, CH in enumerate(self.fullHeader[self.name_s:]):
            if ( CH == ' ' ) or ( CH == ':' ) or ( CH == '{'):
                self.name_e = indexCH + self.name_s
                break
        automock_assert(self.name_e - self.name_s > 0, 'Class name is strange.')

        self.name = self.fullHeader[self.name_s:self.name_e]
        pass

    def recognizeInheritanceSection(self):
        '''
        Function is finding start beginning of class body. When reach : expect inheritance section.
        UT: ok
        '''
        self.inheritance_s = -1
        self.body_s = -1
        for indexCH, CH in enumerate(self.fullHeader[self.name_e:]):
            if CH == ':':
                self.inheritance_s = indexCH + self.name_e
            if CH == '{':
                self.body_s = indexCH + self.name_e
                break

        automock_assert(self.body_s != 1, 'Missing class declaration.')

        # 2) find all inheritance classes
        self.inheritance = ''
        if self.inheritance_s != -1:
            self.inheritance_e = self.body_s
            self.inheritance = self.fullHeader[self.inheritance_s:self.inheritance_e]


    def findEndOfClassDeclaration(self):
        '''
        Function jump to start of class declaration, we are looking for termination brackets.
        NOTE: here could be problem when we will have some construction with brackets. This is naive implementation.
        UT: ok
        '''
        self.body_e = -1
        bracketCnt = 0
        for indexCH, CH in enumerate(self.fullHeader[self.body_s:]):
            if CH == '{':
                bracketCnt += 1
            if CH == '}':
                bracketCnt -= 1
            if bracketCnt == 0:
                # 4) find termination bracket } index of it
                self.body_e = indexCH + self.body_s
                break
        automock_assert(self.body_e != -1, 'Missing class termination.')

        self.body = self.fullHeader[self.body_s:self.body_e]
        pass

    def fillRestOfStringVars(self):
        '''
        Assign rest of variables.
        UT: ok
        '''
        self.fullClass = self.fullHeader[self.int_classLable_s:self.body_e]
        self.rest = self.fullHeader[self.body_e:]
        pass

    def findSubclasses(self):
        '''
        This function do similar thing as find processClassHeader,
        but declaration is only in body of upper class.
        '''
        pass

    def processClassHeader(self):
        '''
        Function process input string.
        Output is list of missing ctors and dtors.
        UT: ok
        '''
        if not self.findClassLabel():
            return False
        # 1) find name
        self.findClassName()

        self.recognizeInheritanceSection()

        # 3) find start bracket {  index of it
        self.findEndOfClassDeclaration()

        self.fillRestOfStringVars()

        self.evalAllCtors()
        self.evalAllDtors()

        self.findSubclasses()
        return True

    def evalAllCtors(self):
        '''
        Function has this functionality:
            1) find all pure declaration of ctors
            2) find all implementation of ctors (inplace in declaration or outside of declaration CName::CName() )
            3) Create list of this ctors with notes which have to created
        UT: ok
        '''
        self.findCtorDecl()
        self.findCtorDefinitions()
        pass

    def evalAllDtors(self):
        '''
        Function has this functionality:
            1) find pure declaration of dtor for founded class
            2) find implementation of dtor (inplace in declaration or outside of declaration CName::~CName() )
            3) Create list of this ctors with notes which have to created
        UT: ok
        '''
        self.findDtorDecl()
        self.findDtorDefinitions()
        pass

    def findCtorDecl(self):
        '''
        Function is looking for Ctor for pure declarations, store attributes
        (pure mean without direct definition)
        '''
        # Cases which we can exclude
        #   1) definition with declaration CName (list of args) {}
        #   2) definition with =0; =default; =deleted;
        #                    '(\s*explicit)?\s' + self.name + '\s?\(.*\);'

        #CtorPaternPureDecl = '(\;|\s|(\sexplicit\s))' + self.name + '\s*\(((\s*\w*)*\,?)*\)'
        #CtorPaternPureDecl = '(^|\;|\s|(\^?\;?\s*explicit\s))' + self.name + '\s*\(((\s*\w*)*\,?)*\)'
        CtorPaternPureDecl = '(^|\;|\s|(\^?\;?\s*explicit\s))' + self.name + '\s*'

        #CtorPaternPureDecl = '(^|\;|\s|(\^?\;?\s*explicit\s))' + self.name + '\s*\(((\s*\w+)*\,?)*\)'


        #CtorPaternPureDecl = '\s*\((((\s*\w+)*\,?))?\)'


        # CtorPaternPureDecl = '(\s*explicit)?\s*' + self.name + '(\s*)?\(.*\)\s*;' # only declaration
        #print(CtorPaternPureDecl)
        #print(self.body)
        self.ctorNotDefinedLst =  [ (m.start(0), m.end(0)) for m in re.finditer(CtorPaternPureDecl, self.body)]
        #print(self.ctorNotDefinedLst)


    def findCtorDefinitions():
        '''
        Function is looking for Ctor definitions outside of class declaration body
        '''
        for ctor in self.ctorNotDefinedLst:

            strCtor = self.body[ctor[0]:ctor[1]] # extract ctor declaration string
            strCtor = re.sub(r'\s+',' ',strCtor) # subtitute one or more white chars to one space char
            argsList = re.search('\(.*\)',strCtor).replace('(','').replace(')','').split(',') # get arg list
            for ARG in argsList:
                #remove default arg value
                ARG = ARG.split('=')[0] if '=' in ARG else ARG

            #o_ctor = CtorFunction(self.name)
            # Declaration ctor pattern
            ## CTOR name
            ctorDefPattern = self.name + '\:\:' + self.name
            # CTOR opening arg bracket
            ctorDefPattern += '\s*\('

            #TODO from args list generate correct pattern
            # CTOR closing arg bracket and implementation
            ctorDefPattern += '\)\s*\{.*\}'

    def findDtorDecl():
        '''
        Function is looking for Dtor declarations, store attributes, and definition
        '''
        DtorPaternPureDecl = '(\s)+(explicit)?(\s)+\~' + self.name + '\s*\(.*\)\s*;' # only declaration
        pass


    def findDtorDefinitions():
        '''
        Function is looking for Dtor definition outside of class declaration body
        '''
        pass

class AutomockPostprocessor():
    pMock: Path
    pHeader: Path
    strMock: str
    strHeader: str
    strPatchedMock: str
    lstCppClassInfo: [CppClassInfo]

    def __init__(self, pathHeader: Path, pathMock: Path):
        '''
        Init function set default value.
        '''
        self.pMock = pathMock
        self.pHeader = pathHeader
        self.strMock = ''
        self.strHeader = ''
        self.strPatchedMock = ''
        self.lstCppClassInfo = []


    def setHeader(self, pathHeader: Path):
        '''
        Header setter
        '''
        self.pHeader = pathHeader


    def setMock(self, pathMock: Path):
        '''
        Mock setter
        '''
        self.pMock = pathMock


    def processCppAutomockedFile(self):
        '''
        Process cpp automocked file:
        1   Load mock and header files to string.
        2   Aply patch to mock string.
        3   Write mock string to file.
        '''
        self.strMock = readFilePathToString(self.pMock)
        self.strHeader = readFilePathToString(self.pHeader)
        self.patchCppAutomock()
        writeStringToFilePath(self.strPatchedMock,self.pMock)
        pass


    def getNumOfClassesInHeader(self, strHeader):
        '''
        Function return number of class keyword in string header.
        '''
        classPatern = '((^|\s)class\s)'
        return len(re.findall(classPatern,strHeader))


#    def getClassStructure(self, int_start, str_header):
#
#        pass
    def processHeader(self, strPureHeader):
        '''
        It creates list of CppClassInfo even with subclasses.
        Go through code and identify all ctors and dtors declaration and definition.
        Keep all none defined ctors and dtors.
        '''
        startIndex = 0
        while True:
            o_classInfo = CppClassInfo(header,startIndex)
            if o_classInfo.processClassHeader():
                self.lstCppClassInfo.append(o_classInfo)
                startIndex = o_classInfo.body_e
            else:
                # process class header failed. -> EOF or seriouse error.
                break

        pass
        ### for each class find definitions/declarations of ctors dtors, ClassName(foo)=default/0; -> declaration only + attributes, ClassName(foo){} -> definice

        ### i have list of classes, whith list of ctors and which ctors need be implemented i have list of params(in contructors params will be typed to void)


    def patchCppAutomock(self):
        '''
        Patch automock expects valid code and generated mock code.
        It consists of these steps:
        1   strip comments
        2   remove tabs and other multiple white char
        3   get number of classes
        3a  if number of classes is zero -> nothing to do
        3b  if number of classes is non zero -> find all not implemented ctors and dtor
        4   Process class header. This
        '''
        # Extract non implemented ctors and dtors from header
        ## remove comment in code
        header = stripCppComments(self.strHeader)
        header = removeTabs(header)
        ## calculate number of top classes. Class object keep index start end. start 'class', end '}' terminator
        #((^|\s)class\s)
        numOfClass = self.getNumOfClassesInHeader(header)
        # numOfClass = header.count(' class ')
        if numOfClass > 0 :
            self.processHeader(header)

        else:
            # nothing to add in to mock string
            self.strPatchedMock = self.strMock
        # append non existing ctors and dtor to mock
        ## from structure above append all code in to mockStr


def readFilePathToString(pathF):
    assert pathF.is_file()
    return pathF.read_text()

def writeStringToFilePath(str_txt, pathF):
    with pathF.open('w') as f:
        f.write_text(str_txt)

def stripCppComments(text):
    #return re.sub('//.*?\n|/\*.*?\*/', '', text, flags=re.S)
    return re.sub('//.*?(\r\n?|\n)|/\*.*?\*/', '', text, flags=re.S)


def removeTabs(text, numOfSpace = 4):
    return text.replace('\t', numOfSpace * ' ')

def patchStrByDict(strPath, subsDict):
    strArg = strPath
    for key in subsDict:
        strArg = strArg.replace(key,subsDict[key])

    return strArg


def getRightSourceSuffixFromHeader(hSuf):
    suffixDict = {'h': 'c', 'H': 'C', 'hpp': 'cpp', 'HPP': 'CPP'}
    stripSuff = hSuf.replace('.','')
    assert stripSuff in suffixDict, 'Unexisting header suffix(%s)!' % (stripSuff)
    return suffixDict[stripSuff]

def getCppSuffix(hSuf):
    return 'cpp'
