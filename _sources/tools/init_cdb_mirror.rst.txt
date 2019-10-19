.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _init_cdb_mirror:

================================================================================
Initialisieren eines CDB Spiegel-Systems
================================================================================

Für die Initialisierung eines Spiegelsystems (aka Entwicklersystem) eignet sich
das Kommando ``init-cdb-mirror`` der CDB-Tools.  Die Anwendung wird im Abschnitt
":ref:`mirror_init`" beschrieben. ::

   [CDBTools]$ init-cdb-mirror

   =========================================
   Initialisierung eines CDB Spiegel-Systems
   =========================================

   Zum Anlegen eines solchen Spiegels werden ein DB-Export und eine (Clone-)
   Kopie des CADDOK_BASE Ordners benötigt (ohne BlobStore).

   Die Initialisierung einer CDB Instanz ist für Entwickler-Systeme gedacht, die
   aus einem DB-Dump und einem Abzug der Sourcen aufgebaut werden.

   Die Änderungen aus einer solchen Initialisierung sind unumkehrbar und sollten
   nur von Personen durchgeführt werden, die wissen, was sie machen!

   ELEMENTS Version 15.3

   Soll die DB initialisiert werden? [y/N] n

   END

