@REM -*- coding: windows-1252; mode: bat -*-
@echo off
IF NOT DEFINED CDBTOOLS_HOME (
   call "%~d0%~p0cdbEnv.bat"
)

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"
pylint %*

