@REM -*- coding: windows-1252-dos; mode: bat -*-
@echo off

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

SET PY27=%CDBTOOLS_HOME%\py27

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

powerscript -c "import pip, sys;sys.executable='powerscript.exe';pip.main()" install --install-option="--prefix=%PY27%" %*

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
