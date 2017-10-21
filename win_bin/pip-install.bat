@REM -*- coding: windows-1252-dos; mode: bat -*-
@echo off

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

SET "PY27=%CDBTOOLS_HOME%\py27"

REM This is a small hackisch injection to get *portable* shebangs for the .exe
REM starter installed in /Scripts::
REM
REM   sys.executable='powerscript.exe'
REM
REM In sense of beeing *portable* we need a shebang without absolute pathnames.
REM With above, we get::
REM
REM   #!powerscript.exe
REM

SET __PYVENV_LAUNCHER__=powerscript.exe
SET PIP_INGNORE_INSTALLED=true

powerscript -c "import pip, sys;sys.executable='powerscript.exe';pip.main()" install --ignore-installed --install-option="--prefix=%PY27%" %*

REM .bat wrapper
REM ------------

echo.
echo fixing script wrapper
echo =====================
echo.
powerscript -c "import dm.cdbtools.bootstrap;dm.cdbtools.bootstrap.replace_exe_with_bat('%PY27%\Scripts')"

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
