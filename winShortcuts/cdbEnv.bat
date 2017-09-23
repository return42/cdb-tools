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

SET CADDOK_DBNAME=prod_copy
SET CADDOK_RUNTIME=C:\share\cdb10_1_sl48
SET CADDOK_BASE=C:\share\customer\instance_prod_copy
REM SET DEVELOPER_SITE_CONF=%~d0%~p0..\templates\etc\site.conf

SET "CADDOK_LOGDIR=%CADDOK_BASE%\tmp"
SET "CDB_INSTANCE=%CADDOK_DBNAME%@%CADDOK_BASE%"
SET "CADDOK_CLIENT_HOME=%CADDOK_RUNTIME%"
