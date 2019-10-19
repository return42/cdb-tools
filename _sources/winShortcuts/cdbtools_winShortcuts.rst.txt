.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_winShortcuts:

=============================
Erweiterte CDB-Tools Umgebung
=============================

.. _upkeep_bat:

``upkeep.bat``
==============

Ein Skript für den :ref:`Build <cdbtools_repo>` & :ref:`Update
<update_cdbtools>` der CDB-Tools, das nacheinander die folgenden Operationen
anbietet:

1. bootstrap       :ref:`(nur online möglich) <cdbtools_bootstrap>`
2. download        :ref:`(nur online möglich) <cdbtools_bootstrap>`
3. install         :ref:`(auch offline möglich) <cdbtools_build>`
4. update launcher :ref:`(auch offline möglich) <cdbtools_build>`
5. ZIP CDB-Tools   :ref:`(auch offline möglich) <cdbtools_build>`


.. _tools_sh_bat:

``tools-sh.bat``
================

Startet eine Shell mit der erweiterten Laufzeitumgebung der CDB-Tools.  Auch zu
erkennen an dem Prompt ``[CDBTools]`` und nicht zu verwechseln mit einer
gewöhnlichen CDB Umgebung mit dem Prompt ``[cdbsrv-11.3.10:cust_dev]`` (oder
ähnlich, s.a. :ref:`rte_prompt`).

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

Startet den Python-Interpreter von CDB in der CDB-Tools Umgebung. Als REPL_
kommt ptpython_ zum Einsatz.  Hier ein Beispiel, bei dem zu erkennen ist, dass
das ``lxml`` Paket aus der CDB-Tools Umgebung bezogen wird:

.. code-block:: none

   ------------------------------------------------------------
   CDB-Tools environment
   ------------------------------------------------------------

     CADDOK_RUNTIME: C:\share\contact\cdbsrv-11.3.10
     CADDOK_BASE:    C:\share\cdb_cust_dev
     CADDOK_DEFAULT: cust_dev@C:\share\cdb_cust_dev
     HOME:           C:\Users\user

   >>> import lxml
   >>> lxml
   <module 'lxml' from 'C:\share\cdb-tools\py27\Python27\site-packages\lxml\__init__.pyc'>

   >>> import cust.plm
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ImportError: No module named cust.plm

   No module named cust.plm

.. hint::

   Der Python Interpreter (``python.exe``) baut kein CDB RTE auf, es stehen nur
   die Python Pakete aus CDB (als auch aus den CDB-Tools) zur Verfügung.  Python
   Programme, die im Kontext der CDB-Instanz arbeiten müssen immer mit dem
   ``powerscript.exe`` Interpreter gestartet werden.


``tools-studio.bat``
====================

Startet das CDB PowerScript Studio (aka. eclipse) von CDB in der CDB-Tools
Umgebung.


.. _tools_powerscript_bat:

``tools-powerscript.bat``
=========================

Startet den PowerScript Interpreter von CDB in der CDB-Tools Umgebung. Als REPL_
kommt ptpython_ zum Einsatz.  Hier ein Beispiel, bei dem zu erkennen ist, dass
das ``lxml`` Paket aus der CDB-Tools Umgebung bezogen wird.  Da es sich im
PowerScript handelt können auch die Pakete aus der CDB-Instanz importiert
werden:

.. code-block:: none

   ------------------------------------------------------------
   CDB-Tools environment
   ------------------------------------------------------------

     CADDOK_RUNTIME: C:\share\contact\cdbsrv-11.3.10
     CADDOK_BASE:    C:\share\cdb_cust_dev
     CADDOK_DEFAULT: cust_dev@C:\share\cdb_cust_dev
     HOME:           C:\Users\user

   >>> import lxml
   >>> lxml
   <module 'lxml' from 'C:\share\cdb-tools\py27\Python27\site-packages\lxml\__init__.pyc'>

   >>> import cust.plm
   >>> cust.plm
   <module 'cust.plm' from 'c:\share\cdb_cust_dev\cust.plm\cust\plm\__init__.pyc'>



.. _tools_localhost_START_bat:

``tools-localhost-START.bat``
=============================

Eignet sich für remote Debug-Zwecke in einer Entwickler Installation (eine
einfache Alternative zum `PyDev Remote Debugger`_).  Es wird der *lokale* CDB
Server und die für den *localhost* konfigurierten Dienste in einer CDB-Tools
Umgebung gestartet (vergleiche :ref:`cdb_localhost_START_bat`).  Gleichzeitig
startet in der Konsole ein *Listener*, der auf Breakpoints lauscht.  Einen
Breakpoint setzt man wie folgt:

.. code-block:: python

   from dm.cdbtools import BP
   BP()

Wird der Breakpoint erreicht, so öffnet der Listener eine Py-Debugger Sitzung
(siehe pdb_).  Setzt man einen neuen Breakpoint in den Sourcen, so muss nicht
immer der ``CDBSVCD`` Prozess neu gestartet werden.  So reicht es beispielsweise
aus, den PC-Client neu zu starten wenn man lediglich die Sourcen eines
``cdbsrv`` Prozess debuggen will (klassische UserExit Programmierung wie im
PowerScript Studio).

Vorteil des remote Debugging ist, dass man hiermit jeden Server-Prozess debuggen
kann und das auch alle Dienste laufen.  Im Powerscript-Studio läuft
normalerweise nur der cdbsrv Prozess im Debug Modus und man vermisst
evtl. Services die beispielsweise die eLink Anwendungen bereit stellen.

Die Kommunikation zwischen dem Debugger-Client und dem Breakpoint erfolgt über
IP sockets, weshalb man das auch remote Debugging nennen kann.  Prinzipell ist
es auch möglich Server Prozesse auf entfernten Hosts zu debuggen, jedoch sollte
man in einer verteilten Umgebung darauf achten, dass die Breakpoints nicht von
anderen Benutzern oder Prozessen erreicht werden (können). In der Regel wird man
diese Art des Debugging nur in *lokalen* Entwickler Umgebungen nutzen.  Dort
kann es dann aber u.U. auch eine große Hilfe sein, wo man bisher nur die
Möglichkeit hatte Logfiles zu lesen.

.. _cdbtools-activate_bat:

``cdbtools-activate.bat``
=========================

Mit dem Scripten:

- ``win_bin/cdbtools-activate.bat`` und
- ``win_bin/cdbtools-deactivate.bat``

kann die CDB-Tools Umgebung aktiviert resp. deaktiviert werden.  Will man nur
ein Kommando aus den CDB-Tools ausführen, nicht aber die ganze Umgebung in der
Shell aktiveren, so kann man das Skript auch als Wrapper nutzen.  Hier ein
Beispiel für den Aufruf von Pylint::

  C:\share\cdb-tools\win_bin\cdbtools-activate.bat pylint
