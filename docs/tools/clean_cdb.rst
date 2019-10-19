.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _clean_cdb:

=========================
Bereinigung der Datenbank
=========================

.. sidebar::  ES WERDEN DATEN GELÖSCHT!

   Das Löschen von Daten muss immer gegen die eigenen Anwendungsszenarien
   geprüft werden!  Die Bereinigung der DB sollte an einem Spiegel-System (DUMP)
   getestet werden, bevor diese auf ein produktives System angewendet wird.

In CDB sammeln sich z.T. Daten an, die u.U. nicht länger benötigt werden.  Gute
Beispiele sind *uralt* Einträge in der Lizenzstatistik, abgeschlossene Jobs in
den MQ-Anwendungen oder ein überbordendes ERP-Log.  In *unaufgeräumten*
Installationen die seit Jahren im Betrieb sind, können 30% bis 60% der
DB-Resourcen auf solche obsoleten Objekte entfallen.  Ob Optimierungen solcher
Art für Ihre konkreten Anwendungsszenarien überhaupt geeignet sind oder ob dabei
ggf. noch benötigte Daten gelöscht werden kann nicht allgemein beantwortet
werden.  Beim Erstellen von Spiegel-System für die Entwicklung ist eine
Optimierung i.d.R. zu empfehlen.

Kommando clean-cdb
==================

.. sidebar:: Massen-Änderung

   Die gelöschten Daten selbst einzelner Relationen können gewaltig sein und
   u.U. das Transaktions-LOG des DB Systems sprengen.  Die Optionen
   ``--truncate`` und ``--days`` können ggf. helfen.

Für die Bereinigung steht das Tool ``clean-cdb`` zur Verfügung::

  [CDBTools]$ clean-cdb --help

Mit dem Tool können die unten beschriebenen Anwendungen aufgeräumt werden.
Mit dem Parameter ``all`` werden alle Aktionen nacheinander ausgeführt. ::

  [CDBTools]$ clean-cdb all

``--day`` (default 30 Tage)
  Wenn in Installationen die seit Jahren im Betrieb sind zum ersten Mal
  aufgeräumt wird, können die Transaktionen zum Löschen gewaltig sein.  Um das
  Transaktions LOG nicht zum Bersten zu bringen kann es sinnvoll sein, zuerst
  die ganz alten Einträge zu löschen und sich sukzessive zum gewünschten
  Erhalt-Datum nach vorne zu arbeiten.

``--truncate`` (default False)
  Wenn die Inhalte der zu bereinigenden DB-Tabellen komplett gelöscht werden
  können, dann kann das über diese Option erreicht werden.  Die DB Tabellen
  werden mit dem SQL-TRUNCATE Statement geleert, welches kein Transaktions-LOG
  erstellt.  Nach dem TRUNCATE wird noch eine Bereinigung des Object-Dictionary
  (``cdb_objects``) durchgeführt.

  Diese Option ist oftmals für Spiegel-Systeme geeignet, die man auf einfache
  weise *schlank* halten will (z.B. ``clean-cdb all --truncate``).


Bereinigen des Object-Dictionary
================================

Bereinigung des Object-Dictionary (cdb_object).  Kann nach SQL Update-Skripten,
insbesondere nach einem SQL-TRUNCATE sinnvoll sein. Wird automatisch auf die
bereinigten Relationen angewendet, die mit der Option ``clean-cdb --truncate``
aufgerufen wurden.


Löschen der Lizenz-Statistik (lstatistics)
==========================================

Die Lizenzstatistik wächst kontinuierlich an. In *lang laufenden* Systemen mit
vielen Benutzern ist die Statistik oftmals eine der größten Tabellen.  Sofern
die Statistik nicht ausgewertet wird, kann sie auch von Zeit zu Zeit mal
gelöscht werden.::

  [CDBTools]$ clean-cdb lstatistics --help


Bereinigen der MQ-Anwendungen (mq)
==================================

Es werden alle Message-Queues aufgelistet und Vorschläge zum Reduzieren der
MQ-Daten gemacht (inklusieve dem Löschen der Langtexte).::

  [CDBTools]$ clean-cdb mq --help


Reduzieren der ERP-Log-Einträge
===============================

Das Kontext bezogene ERP-Log (Reiter ERP-Log im Info Dialog) wird über die
CAD-Konfig-Schalter gesteuert:

- "ERP Logging" bzw. "SAP Logging": ``AN`` oder ``AUS``
- "SAP Logmode" bzw. "SAP Logmode:<klasse>" [Messages|Calls|Params|Results]

In einem produktiven System sollte der "SAP Logmode" auf ``Results`` stehen, zu
Diagnosezwecken empfiehlt es sich den Wert kurzfristig auf z.B. ``Results,
Messages`` zu setzen (Details bitte dem Handbuch entnehmen).  In jedem Fall
sollten solche Diagnose Einstellungen aber nicht dauerhaft im produktiven System
aktiviert sein, da das ERP Log die DB aufbläht.  Zum Löschen alter Meldungen
eignet sich das Kommando::

    [CDBTools]$ clean-cdb erplog --help

``--sap-system SAP_SYSTEM`` (default: all)
  SAP-System dessen Logs bereinigt werden sollen.

``--drop-result`` (default: False)
  Die ``Results`` Meldungen des SAP-GW sollen auch gelöscht werden.

Auch wenn das Logging nur auf ``Results`` steht, kann es passieren, dass das
ERP-Log extrem anwächst, wenn z.B. SAP Abgleichvorgänge über lange Zeiträume
fehlschlagen, diese aber permanent wiederholt werden.  Folgendes SQL Statement
kann einen Eindruck darüber vermitteln ob es angebracht ist das ERP-Log mal zu
bereinigen.

.. code-block:: sql

  SELECT obj_id, COUNT(obj_id) 'Einträge'
    FROM erp_log
   GROUP BY obj_id
   ORDER BY count(obj_id) DESC;

Wenn das Statement viele Objekte mit mehr als 100 Einträgen auflistet, kann sich
eine Bereinigung des Logs lohnen.

.. code-block:: sql

   SELECT COUNT(*) FROM erp_log;

Sollte das letzte Statement mehr als 200.000 Einträge zählen, kann man auch mal
überlegen aufzuräumen.

Historie der Kennzahlen in CDB
==============================

Für die Bereinigung der Relation ``CDBQC_HISTORY`` bieten die CDB-Tools aktuell
keine Lösung.  Jedoch sollte der CDB-Admin diese genau im Auge behalten, denn
auch sie wird oftmals nicht benötigt.


DB-Management System
====================

Räumt man eine DB nach langer Zeit zum ersten mal auf, so können die gelöschten
Datenmengen z.T. sehr groß sein und es kann Sinn machen die Datenbank-Files zu
*shrinken* und auch das Transaction Log zu löschen und/oder nach Bedarf zu
konfigurieren (s.a. :ref:`optimze_db`).

