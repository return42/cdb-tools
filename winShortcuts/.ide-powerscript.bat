@REM -*- coding: utf-8; mode: bat -*-
@echo off

SET _CDBTOOLS_SKIP_INTRO=1

IF NOT DEFINED CDBTOOLS_HOME (
   call "%~d0%~p0cdbEnv.bat" >NUL  2>NUL
)
call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat" >NUL  2>NUL
"%CADDOK_RUNTIME%\powerscript.exe" %*
exit
