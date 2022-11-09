#!/bin/bash

# This script starting test framework in shell


if [ ! -d "./Tools/TestConfigs" ]
then
  echo Creating TestConfigs folder in Tools\/TestConfigs
  mkdir ./Tools/TestConfigs
fi

if [ ! -f "./Tools/TestConfigs/default.tcfg" ]
then
  echo "Copy default test config file.\(default.tcfg\)"
  cp Tools/defaults/default.tcfg Tools/TestConfigs/default.tcfg
fi

if [ ! -f "testSetups.ini" ]
then
  echo "Copy default test ini file.\(testSetups.ini\)"
  cp Tools/defaults/testSetupsTemplate.ini testSetups.ini
fi

if [ ! -f "envPath.ini" ]
then
  echo "Copy default test ini file.\(envPath.ini\)"
  cp Tools/defaults/envPathTemplate.ini envPath.ini
fi

if [ ! -f "bashEnvCfg.sh" ]
then
  echo "Copy default test ini file.\(bashEnvCfg.sh\)"
  cp Tools/defaults/bashEnvCfgTemplate.sh bashEnvCfg.sh
fi

source bashEnvCfg.sh

if ! command -v "${PYTHON3}" &> /dev/null
then
    echo "${PYTHON3} could not be found"
    exit 1
fi


echo Run tests framework.

${PYTHON3} Tools/tdd/src/startTddTool.py

echo "Press any key to continue"
read -n 1

exit 0
