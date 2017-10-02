.. -*- coding: utf-8; mode: rst -*-

=========================
Bereinigung der Datenbank
=========================

In CDB sammeln sich z.T. Daten an, die u.U. nicht länger benötigt werden.  Gute
Beispiele sind *uralt* Einträge in der Lizenzstatistik, abgeschlossene Jobs in
den MQ-Anwendungen oder ein überbordendes ERP-Log. Es kann sich lohnen solche
Einträge von Zeit zu Zeit mal aufzuräumen, resp. nicht änger benötigte Daten zu
löschen. In *unaufgeräumten* Installationen die seit Jahren laufen können schon
mal bis zu 30% oder 50% der DB-Resourcen auf solche obsoleten Objekte entfallen.

Ob Optimierungen solcher Art für Ihre konkreten Anwendungsszenarien überhaupt
geeignet sind oder ob dabei ggf. noch benötigte Daten gelöscht werden kann
nicht allgemein beantwortet werden.

  Das Löschen von Daten muss immer gegen die eigenen Anwendungsszenarien geprüft
  werden! Testen Sie die Tools sorgfältig in einer Entwickler-Kopie bevor Sie
  diese auf ein produktives System anwenden!

Für die Bereinigung steht das Tool ``clean_cdb`` zur Verfügung::

  [CDB-Tools] $ clean-cdb --help

.. caution::

   ACHTUNG:  ES WERDEN DATEN GELÖSCHT!

Kommando clean_cdb
==================

Wenn in einem System, das schon lange läuft zum Ersten mal aufgeräumt wird,
können die Transaktionen zum Löschen gewaltig sein. Um das Transaktions-Log
nicht zum bersten zu bringen kann es sinnvoll sein, zuerst die ganz alten
Einträge (meist gibt es eine Option ``--days`` ) zu löschen und sich sukzessive
zum gewünschten Erhalt-Datum nach vorne zu arbeiten.

Wenn die Inhalte der zu bereinigenden DB-Tabellen komplett gelöscht werden
können, dann kann das i.d.R. über die Option ``--truncate`` erreicht werden.
Die DB Tabellen werden dan mit dem SQL ``TRUNCATE`` Statement geleert, welches
kein Trnsaction-Log erstellt. Diese Option ist oftmals für Spiegel-Systeme
geeignet, die man auf einfache weise *schlank* halten will (z.B. ``clean_cdb all
--truncate``).


Löschen der Lizenz-Statistik (lstatistics)
==========================================

Die Lizenzstatistik wächst kontinuierlich an. In lang laufenden Systemen mit
vielen Benutzern ist die Statistik oftmals eine der größten Tabellen. Sofern
die Statistik nicht ausgewertet wird, kann sie auch von Zeit zu Zeit mal
gelöscht werden.::

  [CDB-Tools] $ clean-cdb lstatistics --help


Bereinigen der MQ-Anwendungen (mq)
==================================

Es werden alle Message-Queues aufgelistet und Vorschläge zum Reduzieren der
MQ-Daten gemacht (inklusieve dem Löschen der Langtexte).::

  [CDB-Tools] $ clean-cdb mq --help


Reduzieren der ERP-Log-Einträge
===============================

Das Kontext bezogene ERP-Log (Reiter ERP-Log im Info Dialog) wird über über die
CAD-Konfig-Schalter gesteuert:

- "ERP Logging" bzw. "SAP Logging": ``AN`` oder ``AUS``
- "SAP Logmode" bzw. "SAP Logmode:<klasse>" [Messages|Calls|Params|Results]

In einem produktiven System sollte der "SAP Logmode" auf ``Results`` stehen, zu
Diagnosezwecken empfiehlt es sich den Wert kurzfristig auf z.B. ``Results,
Messages`` zu setzen (Details bitte dem Handbuch entnehmen).  In jedem Fall
sollten solche Diagnose Einstellungen aber nicht dauerhaft im produktiven System
aktiviert sein, da das ERP Log die DB aufbläht.  Zum Löschen alter Meldungen
eignet sich das Kommando::

    [CDB-Tools] $ clean-cdb erplog --help

Auch wenn das Logging nur auf 'Results' steht, kann es passieren, dass das Log
extrem anwächst, wenn z.B. SAP Abgleichvorgänge fehlschlagen, diese aber
permanent wiederholt werden.

Folgendes SQL Statement kann einen Eindruck vermitteln ob es angebracht ist das
Log mal zu bereinigen.

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
