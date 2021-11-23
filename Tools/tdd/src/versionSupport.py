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

from pathlib import Path

RelVerNums = [0, 1, 0]

def readWholeTextFileAsStrlist(filePath: Path):
    Lines = []
    with open(str(filePath), "r") as file:
        Lines = file.read().splitlines()
        #Lines = file.readlines()
    return Lines

class VersionRelease:
    def __init__(self):
        self.int_HighNum = RelVerNums[0]
        self.int_MidNum = RelVerNums[1]
        self.int_LowNum = RelVerNums[2]

    def getHigh(self):
        return self.int_HighNum

    def getMid(self):
        return self.int_MidNum

    def getLow(self):
        return self.int_LowNum

    def getStrReleaseVersion(self):
        return "V%i.%i.%i" % (self.int_HighNum, self.int_MidNum, self.int_LowNum)

class VersionDevelopment:
    def __init__(self):
        self.areValuesReaded = False
        self.Time_UTC = ""
        self.Branch = ""
        self.DevName = ""
        self.DevEmail = ""
        self.HASH = ""

    def readVersionFile(self, verFile: Path):
        bRetVal = False
        if verFile.is_file() :
            lines = readWholeTextFileAsStrlist(verFile)
            for line in lines:
                listSplit = line.split(": ",1)
                if "Time_UTC" in listSplit[0]:
                    self.Time_UTC = listSplit[1]
                if "Branch" in listSplit[0]:
                    self.Branch = listSplit[1]
                if "Name" in listSplit[0]:
                    self.DevName = listSplit[1]
                if "Email" in listSplit[0]:
                    self.DevEmail = listSplit[1]
                if "HASH" in listSplit[0]:
                    self.HASH = listSplit[1]
                    bRetVal = True
            self.areValuesReaded = True
            pass
        return bRetVal

    def getHash(self):
        return self.HASH

    def getShortedHash(self,num=5):
        if num < ( len(self.HASH) - 2 ):
            return self.HASH[:num] + "..." + self.HASH[-num:]
        return self.getHash

#class VersionFull:
