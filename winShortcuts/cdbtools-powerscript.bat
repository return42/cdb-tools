@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap libraries from CDB-Tools
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   call "%~d0%~p0cdbEnv.bat"
)

REM if NOT '%1' == 'conemu' (
REM   START "ConEmu" "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" -reuse -run %0 conemu
REM  GOTO Exit
REM )

REM ----------------------------------------------------------------------------
:openCMD
REM ----------------------------------------------------------------------------

chcp 65001 >NUL
SET LC_ALL=de_DE.UTF-8

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"
call ptpython

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
