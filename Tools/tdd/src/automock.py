from pathlib import Path
import subprocess
import re

def createAutomocks(mockDict,incLst,strCppStd = 'c++11', strCStd = 'c99', forcedCpp = False):
    '''
    This function create mock file for whole mock dictionary,
    it has default parameters and call creating function for each specific item.
    '''
    for key in mockDict:
        callAutomockTool(key, mockDict[key], incLst, strCppStd, strCStd, forcedCpp)

def getPathAutomockTool():
    return Path('Tools') / 'programs' / 'CppUMockGen-0.4-win64' / 'bin' / 'CppUMockGen'

def callAutomockTool(headerName, mockName, incList, strCppStd, strCStd, forcedCpp):
    str_PathCppUMockGen = getPathAutomockTool()
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
    pass

class DtorFunction(BasicFunction):
    def __init__(self, name: str):
        BasicFunction.__init__()
        self.name = '~' + name
    pass

class CppClassInfo():
    name: str
    start: int
    end: int
    ctors: [CtorFunction]
    dtors: [DtorFunction]
    # innerClassLst: [CppClassInfo] python does not have forward declaration
    innerClassLst: []
    def __init__(self, name, int_start=0, int_end=0):
        self.name = name
        self.start = int_start
        self.end = int_end
        self.ctors = []
        self.dtors = []
        self.innerClassLst = []

class AutomockPostprocessor():
    pMock: Path
    pHeader: Path
    strMock: str
    strHeader: str
    strPatchedMock: str

    def __init__(self, pathHeader: Path, pathMock: Path):
        self.pMock = pathMock
        self.pHeader = pathHeader
        self.strMock = ''
        self.strHeader = ''
        self.strPatchedMock = ''

    def setHeader(self, pathHeader: Path):
        self.pHeader = pathHeader

    def setHeader(self, pathMock: Path):
        self.pMock = pathMock


    def processCppAutomockedFile(self):
        self.strMock = readFilePathToString(self.pMock)
        self.strHeader = readFilePathToString(self.pHeader)
        self.strPatchedMock = self.patchCppAutomock()
        writeStringToFilePath(self.strPatchedMock,self.pMock)
        pass

    def numOfClassesInHeader(self, strHeader):
        classPatern = '((^|\s)class\s)'
        return len(re.findall(classPatern,strHeader))
        pass

    def patchCppAutomock(self):
        # Extract non implemented ctors and dtors from header
        ## remove comment in code
        header = stripCppComments(self.strHeader)
        header = removeTabs(header)
        ## calculate number of top classes. Class object keep index start end. start 'class', end '}' terminator
        #((^|\s)class\s)
        numOfClass = self.numOfClassesInHeader(header)
        # numOfClass = header.count(' class ')
        if numOfClass > 0 :
            pass
        ### check existence of inner classes. Each class keep list of internal class
        ### for each class find definitions/declarations of ctors dtors, ClassName(foo)=default/0; -> declaration only + attributes, ClassName(foo){} -> definice

        ### i have list of classes, whith list of ctors and which ctors need be implemented i have list of params(in contructors params will be typed to void)
        else:
            pass
        # append non existing ctors and dtor to mock
        ## from structure above append all code in to mockStr
        pass

def readFilePathToString(pathF):
    assert pathF.is_file()
    return pathF.read_text()

def writeStringToFilePath(str_txt, pathF):
    with pathF.open('w') as f:
        f.write_text(str_txt)

def stripCppComments(text):
    return re.sub('//.*?\n|/\*.*?\*/', '', text, flags=re.S)
    #return re.sub('//.*?(\r\n?|\n)|/\*.*?\*/', '', text, flags=re.S)

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
