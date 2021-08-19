@REM -*- coding: utf-8; mode: bat -*-
@echo off

call "%~d0%~p0cdbEnv.bat"

explorer "%ENV_EDGE_URL%:64064/admin"
