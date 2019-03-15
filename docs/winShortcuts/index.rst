.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _winShortcuts:

============
winShortcuts
============

In dem Ordner ``winShortcuts`` stehen Skripte und Links bereit, die i.d.R. mit
einem Doppelklick geöffnet werden können. Die Idee dieses Ordner ist es, dem
CDB -Entwickler bzw. -Administrator für seine Arbeit die wichtigsten Umgebungen,
Tools oder aber auch Links auf einfache Weise an einem Ort bereit zu stellen.
Zu unterscheiden sind die Prozesse in ihrer Laufzeitumgebung, die entweder eine
:ref:`gewöhnliche CDB Umgebung <cdb_winShortcuts>` ist oder aber eine
:ref:`erweiterte CDB-Tools Umgebung <cdbtools_winShortcuts>` ist. Als dritte
Gruppe gibt es noch die :ref:`WEB-Links <cdblinks_winShortcuts>` die gar keine
Umgebung benötigen, da sie nur Links auf die Seiten der (CDB) Dienste sind.

- ``cdbEnv.bat`` In dieser Datei werden Variablen der CDB-Tools Umgebung
  eingestellt siehe :ref:`setup_cdbenv`.

.. toctree::

   cdb_winShortcuts
   cdbtools_winShortcuts
   cdblinks_winShortcuts


.. _winShortcuts_tip:

.. tip::

   Kopieren Sie sich den ganzen Ordner :origin:`winShortcuts` in Ihre Instanz
   und versionieren Sie ihn dort.  Dort können Sie dann auch nach belieben die
   Links ändern, Launcher entfernen oder eigene Launcher erstellen.  Nicht
   vergessen, in der Kopie muss in der ``cdbEnv.bat`` dann noch der Verweis auf
   die CDB-Tools korrekt gesetzt sein:

   .. code-block:: dosbatch

      SET "CDBTOOLS_HOME=C:\share\cdb-tools"


Vorlage für eigene Launcher
===========================

.. code-block:: dosbatch

   @REM -*- coding: windows-1252; mode: bat -*-
   @echo off
   IF NOT DEFINED CDBTOOLS_HOME (
      call "%~d0%~p0cdbEnv.bat"
   )

   call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"

   REM hier den Aufruf des Programms, das in der CDB-Tools Umgebung gestartet
   REM werden soll.
   SET
   PAUSE


Wenn das Programm nur über eine Shell mit dem Anwender interagiert, dann kann
man das Programm auch in der etwas komfortableren ConEmu_ aufrufen:

.. code-block:: dosbatch

   @REM -*- coding: windows-1252; mode: bat -*-
   @echo off
   IF NOT DEFINED CDBTOOLS_HOME (
      call "%~d0%~p0cdbEnv.bat"
   )

   IF NOT EXIST "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" goto openCMD
   IF NOT [%1]==[conemu] (
      START "ConEmu" "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" -reuse -run %0 conemu
      GOTO Exit
   )
   :openCMD

   call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"

   REM hier den Aufruf des Programms, das in der CDB-Tools Umgebung gestartet
   REM werden soll.
   SET
   PAUSE

   :Exit


