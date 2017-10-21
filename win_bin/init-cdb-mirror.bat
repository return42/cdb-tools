@REM -*- coding: windows-1252-dos; mode: bat -*-
@echo off

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

SET "PY27=%CDBTOOLS_HOME%\py27"

powerscript -c "import dm.cdbtools.init_cdb_mirror;dm.cdbtools.init_cdb_mirror.main()"  %*

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
