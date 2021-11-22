###############################################################################
# Copyright (c) 2021, Milan Neubert (milan.neuber@gmail.com)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

from TDDConfig import CTestConfig

def printout(text):
    print(text)

def get_input(text):
    return input(text)

def questionYesNo(QuestionOfText):
    bRetVal = False
    while(1):
        answer = get_input(QuestionOfText + " [yes(y)|no(n)]:")
        if answer == "yes" or answer == 'y':
            bRetVal = True
            break
        elif answer == "no" or answer == 'n':
            break
        else:
            printout("Incorrect input value.")
    return (bRetVal)


def questionWithList(QuestionOfText,list,default):
    str_RetVal = default

    str_choises = '|'.join(list)
    while(1):
        answer = get_input(QuestionOfText + " ( %s ) default[%s]:" % (str_choises, str_RetVal))
        if answer == "":
            printout('Using default value.')
            break
        elif answer in list:
            str_RetVal = answer
            break
        else:
            printout("Incorrect input value.")
    return (str_RetVal)

class CreateNewModule():
    str_SRC_FOLDER: str
    str_HEADER_FOLDER: str
    str_FRAMEWORK: str
    str_TOOLCHAIN: str
    str_LANGUAGE: str
    str_COMPONENT_NAME: str
    str_SRC_TYPE: str

    def __init__(self):
        self.str_SRC_FOLDER = ''
        self.str_HEADER_FOLDER = ''
        self.str_FRAMEWORK = "cpputest"
        self.str_TOOLCHAIN = "mingw"
        self.str_LANGUAGE = 'c++'
        self.str_COMPONENT_NAME = ''
        self.str_SRC_TYPE = ''
        pass

    def setModuleConfiguration(self, tConfig):
        '''
        This function create configuration for creating new module.
        Result will be definition of files, type of source code.
        Complete test configuration
        '''
        # define src folder
        ## question if user wants to create C or C++
        moduleType = questionWithList("What type of code will the new module be?", ['c++','c'], 'c++')

        resLst = defineFileConfiguration(moduleType, tConfig)

        

        pass

    def createNewModule(self):
        setModuleConfiguration()
        pass

    def defineFileConfiguration(moduleType, tConfig):
        fileLst = defineFileNames(moduleType)

        folderLst = defineFolders()

        return [fileLst, folderLst]
        pass

    def defineFileNames(moduleType):
        pass

    def defineFolders():
        pass

    def copyFilesToCorrectPositions(resLst):
        pass
