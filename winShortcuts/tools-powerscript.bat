@REM -*- coding: utf-8; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools-wrapper.bat
REM -- Copyright (C) 2022 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap libraries from CDB-Tools
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   call "%~d0%~p0cdbEnv.bat"
)

IF NOT EXIST "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" goto openCMD
  IF NOT [%1]==[conemu] (
    START "ConEmu" "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" -reuse -run %0 conemu
    GOTO Exit
  )

REM ----------------------------------------------------------------------------
:openCMD
REM ----------------------------------------------------------------------------

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"
title tools-powerscript %CADDOK_DBNAME%
"%CADDOK_RUNTIME%\powerscript.exe" -db "%CADDOK_DEFAULT%" -m dm.cdbtools.run_ptpython

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
