##########################################################################
# Copyright (c) 2021, Milan Neubert (milan.neuber@gmail.com)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##########################################################################

from tabulate import tabulate
from colorama import Fore, Style


class CodeStatistics:
    def __init__(self, srcFileName):
        self.loadNewFile(srcFileName)

    def loadNewFile(self, srcFileName):
        pass

    def getTableComplete(self):
        pass

    def getTableViolation(self, params):
        pass


def readLIZARDoutfile(lizardFileName):
    with open(lizardFileName, "r") as File:
        data = File.read()

    lines = data.split("\n")
    lines = [line for line in lines if line]
    array = []
    for line in lines:
        dtaLine = line.split(",")
        array.append([*dtaLine[0:5], dtaLine[6].split("\\")[-1], *dtaLine[7:]])

    return(array)


def interpretLIZARDoutfile(lizardFileName, int_complex, int_parCnt, int_fncLen):
    resArray = readLIZARDoutfile(lizardFileName)
    errArray = []
    for dtaLine in resArray:
        if (int(dtaLine[1]) >= int_complex) or (
                int(dtaLine[3]) >= int_parCnt) or (int(dtaLine[4]) >= int_fncLen):
            errArray.append(dtaLine)
    return(errArray)


def printLIZARDerrArray(errArray, int_complex, int_parCnt, int_fncLen):
    header = [
        'NLOC',
        'CCN[<%s]' % int_complex,
        'tokens',
        'arg num[<%s]' % int_parCnt,
        'length[<%s]' % int_fncLen,
        'file name',
        'fnc name',
        'fnc full name',
        'start',
        'end']
    print(tabulate(errArray, header, tablefmt="pretty"))

def chckCondAndRetColored(str_intVal, intLevel):
    colorChar = []
    if int(str_intVal) >= intLevel:
        colorChar = Fore.RED
    else:
        colorChar = Fore.GREEN

    return (colorChar + str_intVal + Style.RESET_ALL)


def printLIZARDerrArrayShortAndColor(errArray, int_complex, int_parCnt, int_fncLen):
    header = [
        'CCN[<%s]' % int_complex,
        'argn[<%s]' % int_parCnt,
        'flen[<%s]' % int_fncLen,
        'fnc name',
        's',
        'e']
    printArray = []
    for errLine in errArray:
        line = []

        line.append(chckCondAndRetColored(errLine[1],int_complex))

        line.append(chckCondAndRetColored(errLine[3],int_parCnt))

        line.append(chckCondAndRetColored(errLine[4],int_fncLen))

        # fnc name
        line.append(errLine[6])

        # fnc start end
        line.append(errLine[8])
        line.append(errLine[9])

        printArray.append(line)

    print(tabulate(printArray, header, tablefmt="pretty"))
