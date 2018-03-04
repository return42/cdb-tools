@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbEnv.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     general CDB setup
REM ----------------------------------------------------------------------------

REM color 0E

REM CDB setup
REM ---------------

SET "CADDOK_DBNAME=prod_copy"
SET "CADDOK_RUNTIME=C:\share\cdb10_1_sl48"
SET "CADDOK_BASE=C:\share\customer\instance_prod_copy"

SET "CADDOK_INSTALLDIR=%CADDOK_RUNTIME%"
SET "CADDOK_LOGDIR=%CADDOK_BASE%\tmp"
SET "CADDOK_DEFAULT=%CADDOK_DBNAME%@%CADDOK_BASE%"
SET "CADDOK_CLIENT_HOME=%CADDOK_RUNTIME%"

REM CDB-Tools setup
REM ---------------

SET HOME=%HOMEDRIVE%%HOMEPATH%

for %%A IN ("%~dp0\..") DO SET "CDBTOOLS_HOME=%%~fA"
IF %CDBTOOLS_HOME:~-1%==\ SET CDBTOOLS_HOME=%CDBTOOLS_HOME:~0,-1%

REM SET "CDBTOOLS_HOME=C:\share\cdb-tools"

SET "CDBTOOLS_DEBUG_ADDR=127.0.0.1"
SET "CDBTOOLS_DEBUG_PORT=4444"


goto checkEnv

:errorEnv
echo.
echo CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo CADDOK_BASE:    %CADDOK_BASE%
echo CADDOK_DEFAULT: %CADDOK_DEFAULT%
echo.
ECHO ERROR: Die Umgebungsvariablen in der Datei::
ECHO ERROR:   %~d0%~p0cdbEnv.bat
ECHO ERROR: Sind (noch) nicht richtig konfiguriert!
pause
START notepad %~d0%~p0cdbEnv.bat
exit

:checkEnv

IF NOT EXIST %CADDOK_RUNTIME% goto errorEnv
IF NOT EXIST %CADDOK_BASE% goto errorEnv
