@REM -*- coding: utf-8; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     start CDB-Client am Edge Knoten
REM ----------------------------------------------------------------------------

call "%~d0%~p0cdbEnv.bat"

start "CDB-Client" "%CADDOK_CLIENT_HOME%\cdbpc.exe" --url "%ENV_EDGE_URL%" --user xxx

REM ==============================================================================
:Exit
REM ==============================================================================
