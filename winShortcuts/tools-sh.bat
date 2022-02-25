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

cd /d %CADDOK_BASE%

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"
title tools-sh %CADDOK_DBNAME%

REM Der Aufruf der cdbsh bewirkt, dass die PATH Variable sich so ändert, dass
REM die CDB-Tools hinter den CDB .exe stehen (Es wird die RTE des CDB
REM verwendet).  Wenn man hingegen nur eine CMD startet oder in einer CMD das
REM cdbtools-activate.bat aufgerufen wird, hat man das RTE der cdb-tools.

REM "%CADDOK_RUNTIME%\cdbsh.exe" -v -db "%CADDOK_DEFAULT%"
%COMSPEC%
