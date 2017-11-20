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

Startet eine gewöhnliche ``cdbsh``. Zu erkennen auch an dem Prompt
``[cdb:prod_copy]`` (oder ähnlich) und nicht zu verwechseln mit einer
``[CDBTools]`` Umgebung (s.a. :ref:`rte_prompt`).


.. _cdb_pc_bat:

``cdb-pc.bat``
==============

Startet einen gewöhnlichen CDB-Client, mit Anmeldedialog.

.. _cdb_studio_bat:

``cdb-studio.bat``
==================

Startet das CDB Powerscript Studio (aka. eclipse)

.. _cdb_localhost_START_bat:

``cdb-localhost-START.bat``
===========================

Startet den *lokalen* CDB Server und die für *diesen* Host konfigurierten
Dienste. Eignet sich für Entwickler Instanzen, bei denen man den Application
Server nicht in den Diensten des Betriebssystems einrichten möchte. Der
CDB-Server läuft in einer gewöhnlichen CDB Umgebung.
