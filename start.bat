@ECHO OFF

REM ##################################################################################
REM # Copyright (c) 2021, Milan Neubert (milan.neuber@gmail.com)
REM # All rights reserved.
REM #
REM # Redistribution and use in source and binary forms, with or without modification,
REM # are permitted provided that the following conditions are met:
REM #
REM # 1. Redistributions of source code must retain the above copyright notice,
REM #    this list of conditions and the following disclaimer.
REM #
REM # 2. Redistributions in binary form must reproduce the above copyright notice,
REM #    this list of conditions and the following disclaimer in the documentation
REM #    and/or other materials provided with the distribution.
REM #
REM # 3. Neither the name of the copyright holder nor the names of its contributors
REM #    may be used to endorse or promote products derived from this software without
REM #    specific prior written permission.
REM #
REM # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
REM # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
REM # WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
REM # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
REM # ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
REM # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
REM # LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
REM # ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
REM # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
REM # SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
REM ##################################################################################

REM ##################################################################################
REM EDIT HERE PLEASE
REM ##################################################################################
REM If you do not have python3 in path uncomment and fill correctly next two lines
REM PATH=%PATH%;ABSOLUT_PATH_TO_PYTHON3\
REM PATH=%PATH%;ABSOLUT_PATH_TO_PYTHON3\Scripts
REM ##################################################################################
REM ##################################################################################


where /q python
IF ERRORLEVEL 1 (
    ECHO The python is missing in path. Ensure it is installed and placed in your PATH.
    ECHO If you know where is your python installed but you do not want to update your PATH:
    ECHO Please open this start.bat and edit line two and fill correct position for python.exe
    pause
    EXIT /B
) ELSE (
    ECHO Python exists. Let's go!
)

cd %~dp0 && python startTddTool.py

pause
