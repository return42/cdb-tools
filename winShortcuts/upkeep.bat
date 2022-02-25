@REM -*- coding: utf-8; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     upkeep.bat
REM -- Copyright (C) 2022 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------

REM upkeep need some special tests for the environment
SET _CHECK_ENV=N

CALL "%~d0%~p0cdbEnv.bat"

echo ============================================================
echo %~n0 CDB-Tools
echo ============================================================
echo.

IF NOT EXIST "%CADDOK_RUNTIME%" (
  SET _MISSING_CDB=Y
  CALL :WARN "missing CADDOK_RUNTIME at %CADDOK_RUNTIME%"
)

IF NOT EXIST "%CADDOK_BASE%" (
  SET _MISSING_CDB=Y
  CALL :WARN "missing CADDOK_BASE at %CADDOK_BASE%"
)

IF [%_MISSING_CDB%]==[Y] (
  echo.
  echo running upkeep without CDB ^(use this only ^for bootstrap and download purposes^)
) ELSE (
  SET "PATH=%CADDOK_RUNTIME%;%CADDOK_RUNTIME%\Scripts;%PATH%"
  echo   CDBTOOLS_HOME:  %CDBTOOLS_HOME%
  echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
  echo   CADDOK_BASE:    %CADDOK_BASE%
  echo   CADDOK_DEFAULT: %CADDOK_DEFAULT%
  echo.
)

WHERE python.exe >NUL  2>NUL
IF %ERRORLEVEL% EQU 0 goto main

IF EXIST C:\Python27 SET "PATH=C:\Python27;C:\Python27\Scripts;%PATH%"
WHERE python.exe >NUL  2>NUL
IF %ERRORLEVEL% EQU 0 goto main

echo ERROR: ^at least a Python 2.7.9 installation is needed !!!
echo ERROR: first install python 2.7 from https://www.python.org/downloads/
pause
exit 42

:main

  IF x%1 EQU x GOTO runall

  CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"

  IF x%1 EQU xdownload GOTO downloadPackages
  IF x%1 EQU xdist GOTO buildZIP
  echo "-- END --"
  GOTO EXIT_OK

:runall

  REM bootsrap and download (with or without CDB installation)

  echo.
  CALL :askYN "Do you like to download/update the CDB-Tools libraries?"
  IF [%_result%]==[Y] (
    CALL :downloadPackages
  ) ELSE (
    call :INFO "download skiped"
  )

  call :header "bootsrap and download of packages completed"

  IF [%_MISSING_CDB%]==[Y] (
    echo.
    call :INFO "To continue a CDB installation is needed."
    pause
    exit 0
  )

  REM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  REM From here on you have to have an CDB installation
  REM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"

  CALL :askYN "Do you like to (re-) install the CDB-Tools libraries?"
  IF [%_result%]==[Y] (
    CALL :installPackages
  ) ELSE (
    call :INFO "installation skiped"
  )

  CALL :askYN "Do you like to fix the python script launcher?"
  IF [%_result%]==[Y] (
    CALL :fixLauncher
  ) ELSE (
    call :INFO "fix-launcher skiped"
  )

  CALL :askYN "Do you like to built a ZIP from the CDB-Tools?"
  IF [%_result%]==[Y] (
    CALL :buildZIP
  ) ELSE (
    call :INFO "zipping CDB-Tools skiped"
  )

  echo "-- END --"
  GOTO EXIT_OK

:downloadPackages

  CALL :header "bootstrap CDB-Tools"

  START /B /WAIT "bootstrap" "%CDBTOOLS_HOME%\bootstrap\bootstrap.bat"
  IF NOT %ERRORLEVEL% EQU 0 (
     CALL :RAISE_ERROR "bootstrap exit with %ERRORLEVEL%"
  )

  CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat" >NUL 2>NUL

  CALL :header "Download packages"

  python "%CDBTOOLS_HOME%\bootstrap\build.py" get-pypkgs
  IF NOT %ERRORLEVEL% EQU 0 (
     CALL :RAISE_ERROR "download exit with %ERRORLEVEL%"
  )

  python "%CDBTOOLS_HOME%\bootstrap\build.py" get-software
  IF NOT %ERRORLEVEL% EQU 0 (
     CALL :RAISE_ERROR "download exit with %ERRORLEVEL%"
  )

  EXIT /B 0

:installPackages

  CALL :header "install python requirements"
  python "%CDBTOOLS_HOME%\bootstrap\build.py" install-pypkgs
  IF NOT %ERRORLEVEL% EQU 0 (
     CALL :RAISE_ERROR "installation exit with %ERRORLEVEL%"
  )

  CALL :header "install software"
  python "%CDBTOOLS_HOME%\bootstrap\build.py" install-software
  IF NOT %ERRORLEVEL% EQU 0 (
     CALL :RAISE_ERROR "installation exit with %ERRORLEVEL%"
  )
  EXIT /B 0

:fixLauncher

  CALL :header "fix python launcher"
  python "%CDBTOOLS_HOME%\bootstrap\fix_launcher.py"
  IF NOT %ERRORLEVEL% EQU 0 (
    CALL :RAISE_ERROR "fix-launcher exit with %ERRORLEVEL%"
  )
  EXIT /B 0

:buildZIP

  CALL :header "build CDB-Tools ZIP"
  python.exe "%CDBTOOLS_HOME%\bootstrap\build.py" dist
  IF NOT %ERRORLEVEL% EQU 0 (
    CALL :RAISE_ERROR "build CDB-Tools ZIP exit with %ERRORLEVEL%"
  )
  EXIT /B 0


:askYN
  SET _result=Y
  CHOICE /C YN /M %1
  IF %ERRORLEVEL%==2  (
    SET _result=N
  )
  EXIT /B 0

:header
  echo.
  echo %~1
  echo ============================================================
  echo.
  EXIT /B 0

:INFO
  echo INFO: %~1
  EXIT /B 0

:WARN
  echo WARN: %~1
  EXIT /B 0

:RAISE_ERROR
  echo ERROR: %~1
  pause
  exit 42

:EXIT_OK
  pause
  exit 0
