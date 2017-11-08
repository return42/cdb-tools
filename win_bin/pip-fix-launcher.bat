@REM -*- coding: windows-1252-dos; mode: bat -*-
@echo off

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

SET "CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27"
SET "MYPYTHON_EXE=%CADDOK_RUNTIME%\python.exe"

SET PIP_INGNORE_INSTALLED=true

echo fixing script wrapper ...
"%MYPYTHON_EXE%" -c "import dm.cdbtools.bootstrap;dm.cdbtools.bootstrap.replace_exe_with_bat('%CDBTOOLS_PY27%\Scripts')"

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
