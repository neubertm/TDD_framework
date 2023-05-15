cd %~dp0

PATH=%CMAKE_BIN_PATH%;%PATH%
PATH=%MINGW_BIN_PATH%;%PATH%

cmake -G "MinGW Makefiles" .

mingw32-make