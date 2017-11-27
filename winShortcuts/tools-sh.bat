@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools-wrapper.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap libraries from CDB-Tools
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   call "%~d0%~p0cdbEnv.bat"
)

IF NOT EXIST "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" goto openCMD
  SET LC_ALL=de_DE.UTF-8

  IF NOT '%1' == 'conemu' (
    START "ConEmu" "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" -reuse -run %0 conemu
    GOTO Exit
  )

REM ----------------------------------------------------------------------------
:openCMD
REM ----------------------------------------------------------------------------

cd /D "%CDBTOOLS_HOME%"

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"
title tools-sh %CADDOK_DBNAME%
cdbsh.exe -v -db "%CADDOK_DEFAULT%"
