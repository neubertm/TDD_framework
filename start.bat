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

REM Usage: start.bat                 interactive menu
REM        start.bat <Package_Tpkg>  run one package, exit 0 = unit tests pass, 1 = fail
REM        start.bat -a              run all packages, print failed ones, exit = number of failed

setlocal
cd /d "%~dp0"
set "TDD_ARG=%~1"

if not exist winEnvCfg.bat (
  echo First run:
  echo     Creating winEnvCfg.bat file. Probably you have to fill it.
  echo.
  copy Tools\defaults\winEnvCfgTemplate.bat winEnvCfg.bat
)
call winEnvCfg.bat

rem Check if TestConfigs folder exists, if not create it.
if not exist Tools\TestConfigs\ (
  mkdir Tools\TestConfigs
)

if not exist Tools\TestConfigs\default.tcfg (
  copy Tools\defaults\default.tcfg Tools\TestConfigs\default.tcfg
)

if not exist testSetups.ini (
  copy Tools\defaults\testSetupsTemplate.ini testSetups.ini
)

where /q python
IF ERRORLEVEL 1 (
    ECHO The python is missing in path. Ensure it is installed and placed in your PATH.
    ECHO If you know where is your python installed but you do not want to update your PATH:
    ECHO Please open this winEnvCfg.bat and edit two lines and fill correct position for python3.exe
    IF NOT DEFINED TDD_ARG pause
    EXIT /B 1
)

IF NOT DEFINED TDD_ARG GOTO interactive
python -u Tools/tdd/src/autoTest.py "%TDD_ARG%"
EXIT /B %ERRORLEVEL%

:interactive
ECHO Python exists. Let's go!

title eTDD framework

python Tools/tdd/src/startTddTool.py

REM pause
