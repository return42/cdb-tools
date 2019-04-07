@REM -*- coding: utf-8; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     start CDB-Client
REM ----------------------------------------------------------------------------

call "%~d0%~p0cdbEnv.bat"

REM start "CDB-Client" "%CADDOK_CLIENT_HOME%\cdbpc.exe" --url https://localhost --user caddok --password "welcome" --autologon
start "CDB-Client" "%CADDOK_CLIENT_HOME%\cdbpc.exe"

REM ==============================================================================
:Exit
REM ==============================================================================
