@REM -*- coding: windows-1252-dos; mode: bat -*-
@echo off

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

SET "PY27=%CDBTOOLS_HOME%\py27"

SET __PYVENV_LAUNCHER__=powerscript.exe
SET PIP_INGNORE_INSTALLED=true

echo.
echo fixing script wrapper
echo =====================
echo.
powerscript -c "import dm.cdbtools; dm.cdbtools.replace_exe_with_bat('%PY27%\Scripts')"

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
