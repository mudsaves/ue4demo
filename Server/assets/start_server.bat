@echo off
set curpath=%~dp0

cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/Hybrid/

if defined uid (echo UID = %uid%) else set uid=%random%%%32760+1

cd %curpath%
call "kill_server.bat"

echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

start %KBE_BIN_PATH%/machine.exe --cid=172016005031901000 --gus=1
@rem start %KBE_BIN_PATH%/logger.exe --cid=172016005031902000 --gus=2
start %KBE_BIN_PATH%/interfaces.exe --cid=172016005031903000 --gus=3
start %KBE_BIN_PATH%/dbmgr.exe --cid=172016005031904000 --gus=4
start %KBE_BIN_PATH%/baseappmgr.exe --cid=172016005031905000 --gus=5
start %KBE_BIN_PATH%/cellappmgr.exe --cid=172016005031906000 --gus=6
start %KBE_BIN_PATH%/baseapp.exe --cid=172016005031907001 --gus=7
@rem start %KBE_BIN_PATH%/baseapp.exe --cid=172016005031907002 --gus=8
start %KBE_BIN_PATH%/cellapp.exe --cid=172016005031908001 --gus=9
@rem start %KBE_BIN_PATH%/cellapp.exe --cid=172016005031908002  --gus=10
start %KBE_BIN_PATH%/loginapp.exe --cid=172016005031909000 --gus=11
