.. -*- coding: utf-8; mode: rst -*-

================================================================================
Initialsierung eines CDB Spiegel-Systems
================================================================================

Zum Anlegen eines solchen Spiegels werden ein DB-Export und eine (Clone-) Kopie
des CADDOK_BASE Ordners benötigt (ohne BLOB storage).

Die Initialisierung einer CDB Instanz ist für Entwickler-Systeme gedacht,
die aus einem DB-Dump und einem Abzug der Sourcen aufgebaut werden.

Die Änderungen aus einer solchen Initialisierung sind unumkehrbar und
sollten nur von Personen durchgeführt werden, die wissen, was sie machen!


DB Export einspielen
====================

- Mit den DB-Tools das Backup der DB einspielen.
- Ggf. Transaction Log löschen und/oder nach bedarf konfigurieren

CDB Umgebung einrichten
-----------------------

- CDB Binaries (Software) installieren
- In der Kopie der Instanz die DB in ``$CADDOK_BASE/etc/dbtab`` konfigurieren.

.. todo::

   Doku zum Ausbau von Spiegelsysteme ergänzen
