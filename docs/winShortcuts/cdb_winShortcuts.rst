.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdb_winShortcuts:

========================
gewöhnliche CDB Umgebung
========================

Die *normalen* CDB Prozesse laufen in der *normalen* Laufzeitumgebung von CDB,
sie sollen keinen Zugriff auf die Erweiterungen aus den CDB-Tools haben. So
gesehen sind die, in diesem Abschnitt vorgestellten *Shortcuts* ganz normale CDB
Anwendungen.

.. _cdb_sh_bat:

``cdb-sh.bat``
==============

Startet eine ``cdbsh`` in einer Standard CDB-Umgebung (ohne CDB-Tools
Erweiterungen).  Zu erkennen auch an dem Prompt ``[cdbsrv-11.3.10:cust_dev]``
(oder ähnlich) und nicht zu verwechseln mit einer ``[CDBTools]`` Umgebung
(s.a. :ref:`rte_prompt`).

.. code-block:: none

   ============================================================
   cdb-sh (cust_dev@C:\share\cdb_cust_dev)
   ============================================================

     CADDOK_RUNTIME: C:\share\contact\cdbsrv-11.3.10
     CADDOK_BASE:    C:\share\cdb_cust_dev
     CADDOK_DEFAULT: cust_dev@C:\share\cdb_cust_dev

   ============================================================
   ...
   Microsoft Windows [Version 6.3.9600]
   (c) 2013 Microsoft Corporation. Alle Rechte vorbehalten.

   [cdbsrv-11.3.10:cust_dev] C:\share\cdb_cust_dev>


.. _cdb_pc_bat:

``cdb-pc.bat``
==============

Startet einen gewöhnlichen CDB-Client, mit Anmeldedialog.

.. _cdb_studio_bat:

``cdb-studio.bat``
==================

Startet das CDB Powerscript Studio (aka. eclipse) in einer Standard
CDB-Umgebung.

.. _cdb_localhost_START_bat:

``cdb-localhost-START.bat``
===========================

Startet den *lokalen* CDB Server und die für *diesen* Host konfigurierten
Dienste in einer Standard CDB-Umgebung.  Eignet sich für Entwickler Instanzen,
bei denen man den Application Server nicht in den Diensten des Betriebssystems
einrichten möchte.
