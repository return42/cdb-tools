@REM -*- coding: windows-1252-dos; mode: bat -*-
@echo off

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

REM SET "CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27"
REM SET "MYPYTHON_EXE=%CADDOK_RUNTIME%\python.exe"

REM SET PIP_INGNORE_INSTALLED=true

echo fix script wrappers in: "%CDBTOOLS_PY27%\Scripts"
"%MYPYTHON_EXE%" -c "import dm.cdbtools.bootstrap;dm.cdbtools.bootstrap.fix_win_launcher('%CDBTOOLS_PY27%\Scripts')"

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
