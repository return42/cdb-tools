@REM -*- coding: windows-1252-dos; mode: bat -*-
@echo off

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

SET "CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27"
SET "MYPYTHON_EXE=%CADDOK_RUNTIME%\python.exe"

REM This is a small hackisch injection to get *portable* shebangs for the .exe
REM starter installed in /Scripts::
REM
REM   sys.executable='powerscript.exe'
REM
REM In sense of beeing *portable* we need a shebang without absolute pathnames.
REM With above, we get::
REM
REM   #!python.exe
REM

SET PIP_INGNORE_INSTALLED=true

"%MYPYTHON_EXE%" -c "import pip, sys;sys.executable='python.exe';pip.main()" install --ignore-installed --install-option="--prefix=%CDBTOOLS_PY27%" %*

call "%CDBTOOLS_HOME%\win_bin\pip-fix-launcher.bat" 2> NUL

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
