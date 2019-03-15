.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_winShortcuts:

==============================
erweiterete CDB-Tools Umgebung
==============================

.. _upkeep_bat:

``upkeep.bat``
==============

Ein Skript für :ref:`cdbtools_build`, das nacheinander die folgenden Operationen
anbietet:

1. bootstrap (nur online möglich)
2. download (nur online möglich)
3. install
4. update launcher
5. ZIP CDB-Tools


.. _tools_sh_bat:

``tools-sh.bat``
================

Startet eine Shaell mit der erweiterten Laufzeitumgebung der CDB-Tools.  Zu
erkennen auch an dem Prompt ``[CDBTools]`` und nicht zu verwechseln mit einer
gewöhnlichen CDB Umgebung ``[cdbsrv-11.3.10:cust_dev]`` oder ähnlich
(s.a. :ref:`rte_prompt`).

.. code-block:: none

   ------------------------------------------------------------
   CDB-Tools environment
   ------------------------------------------------------------

   CADDOK_RUNTIME: C:\share\contact\cdbsrv-11.3.10
   CADDOK_BASE:    C:\share\cdb_cust_dev
   CADDOK_DEFAULT: cust_dev@C:\share\cdb_cust_dev
   HOME:           C:\Users\user

   Microsoft Windows [Version 6.3.9600]
   (c) 2013 Microsoft Corporation. Alle Rechte vorbehalten.
   Clink v0.4.8 [git:d565ad] Copyright (c) 2012-2016 Martin Ridgers
   http://mridgers.github.io/clink

   C:\share\cdb_cust_dev
   [CDBTools]$


.. _tools_python_bat:

``tools-python.bat``
====================

Startet den Python-Interpreter von CDB in der CDB-Tools Umgebung. Als REPL
kommt ptpython_ zum Einsatz.


.. _tools_powerscript_bat:

``tools-powerscript.bat``
=========================

Startet den Powerscript-Interpreter von CDB in der CDB-Tools Umgebung. Als
REPL kommt ptpython_ zum Einsatz.


.. _tools_localhost_START_bat:

``tools-localhost-START.bat``
=============================

Eignet sich für remote Debug-Zwecke in einer Entwickler Installation (eine
einfache Alternative zum `PyDev Remote Debugger`_).

Es wird der *lokale* CDB Server und die für den *local* Host konfigurierten
Dienste in einer CDB-Tools Umgebung gestartet. Gleichzeitig startet in der
Konsole ein *Listener*, der auf Breakpoints lauscht. Einen Breakpoint setzt
man wie folgt:

.. code-block:: python

   from dm.cdbtools import BP
   BP()

..
   Wird der Breakpoint erreicht, so öffnet der Listener eine Py-Debugger Sitzung
   (siehe pdb_).  Setzt man einen neuen Breakpoint in den Sourcen, so muss nicht
   immer der ``CDBSVCD`` Prozess neu gestartet werden. So reicht es
   beispielsweise aus, den PC-Client neu zu starten, wenn man lediglich die
   Sourcen eines ``cdbsrv`` Prozess debuggen will (klassische UserExit
   Programmierung wie im PowerScript Studio).

   Vorteil des remote Debugging ist, dass man hiermit jeden Server-Prozess
   debuggen kann und das auch alle Dienste laufen. Im Powerscript-Studio läuft
   normalerweise nur der cdbsrv Prozess im Debug Modus und man vermisst
   evtl. Services die beispielsweise die eLink Anwendungen bereit stellen.

   Die Kommunikation zwischen dem Debugger-Client und dem Breakpoint erfolgt über
   IP sockets, weshalb man das auch remote Debugging nennen kann. Prinzipell ist
   es auch möglich Server Prozesse auf entfernten Hosts zu debuggen, jedoch
   sollte man in einer verteilten Umgebung darauf achten, dass die Breakpoints
   nicht von anderen Benutzern oder Prozessen erreicht werden (können). In der
   Regel wird man diese Art des Debugging nur in *lokalen* Entwickler Umgebungen
   nutzen. Dort kann es dann aber auch eine große Hilfe sein, wo man bisher nur
   die Möglichkeit hatte Logfiles zu lesen.
