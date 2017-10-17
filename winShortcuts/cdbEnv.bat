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

color 0E

REM CDB setup
REM ---------------

SET "CADDOK_DBNAME=prod_copy"
SET "CADDOK_RUNTIME=C:\share\cdb10_1_sl48"
SET "CADDOK_BASE=C:\share\customer\instance_prod_copy"

SET "CADDOK_LOGDIR=%CADDOK_BASE%\tmp"
SET "CADDOK_DEFAULT=%CADDOK_DBNAME%@%CADDOK_BASE%"
SET "CADDOK_CLIENT_HOME=%CADDOK_RUNTIME%"

REM CDB-Tools setup
REM ---------------

SET HOME=%HOMEDRIVE%%HOMEPATH%

for %%A IN ("%~dp0\..") DO SET "CDBTOOLS_HOME=%%~fA"
IF %CDBTOOLS_HOME:~-1%==\ SET CDBTOOLS_HOME=%CDBTOOLS_HOME:~0,-1%

REM SET "CDBTOOLS_HOME=C:\share\cdb-tools"
