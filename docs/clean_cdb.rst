.. -*- coding: utf-8; mode: rst -*-

=========================
Bereinigung der Datenbank
=========================

In CDB sammeln sich z.T. DB Einträge z.B. aus Message-Queue Anwendungen oder
dem ERP-Log die nicht alle immer benötigt werden. Nicht benötigte Einträge
sollten von Zeit zu Zeit aufgeräumt werden um die DB *schlank* und damit
performant zu halten.

Das Aufräumen dieser Einträge lohnt sich insbesondere in schon lang laufenden
Systemen die bisher nicht aufgeräumt wurden. In solchen Systemen werden z.T.
bis zu 60% der DB Resourcen auf *unnütze* Einträge verschwendet (z.B. eine
über mehrere Jahre angesammelte Lizenzstatistik).

Ob Optimierungen solcher Art für Ihre konkreten Anwendungszenarien überhaupt
geeignet sind oder ob dabei ggf. noch benötigte Daten gelöscht werden kann
nicht allgemein beantwortet werden. Das Löschen von Daten muss immer gegen
die eigenen Anwendungszenarien geprüft werden! Testen Sie die Tools sorgfältig
in einer Entwickler-Kopie bevor Sie diese auf ein produktives System anwenden!

Für die Bereinigung steht das Tool ``clean_cdb`` zur Verfügung::

  powerscript cdb-tools/clean_cdb.py --help

.. caution::

   ACHTUNG:  ES WERDEN DATEN GELÖSCHT!

Wenn in einem System, das schon lange läuft zum Ersten mal aufgeräumt wird,
können die Transaktionen zum Löschen gewaltig sein. Um das Transaktions-Log
nicht zum bersten zu bringen kann es sinnvoll sein, zuerst die ganz alten
Einträge (meist gibt es eine Option ``--days`` ) zu löschen und sich sukzessieve
zum gewünschten Erhalt-Datum nach vorne zu arbeiten.

Wenn die Inhalte der zu bereinigenden DB-Tabellen komplett gelöscht werden
können, dann kann das i.d.R. über die Option ``--truncate`` erreicht werden.
Die DB Tabellen werden dan mit dem SQL ``TRUNCATE`` Statement geleert, welches
kein Trnsaction-Log erstellt. Diese Option ist oftmals für Spiegel-Systeme
geignet, die man auf einfache weise *schlank* halten will (z.B. ``clean_cdb all
--truncate``).


Löschen der Lizenz-Statistik (lstatistics)
==========================================

Die Lizenstatistik wächst kontinuierlich an. In lang laufenden Systemen mit
vielen Benutzern ist die Statistik oftmals eine der größten Tabellen. Sofern
die Statistik nicht ausgewertet wird, kann sie auch von Zeit zu Zeit mal
gelöscht werden.::

  powerscript cdb-tools/clean_cdb.py lstatistics --help


Bereinigen der MQ-Anwendungen (mq)
==================================

Es werden alle Message-Queues aufgelistet und Vorschläge zum Reduzieren der
MQ-Daten gemacht (inklusieve dem Löschen der Langtexte).::

  powerscript cdb-tools/clean_cdb.py mq --help


Reduzieren der ERP-Log-Einträge
===============================

Das Kontext bezogene ERP-Log (Reiter ERP-Log im Info Dialog) wird über über die
CAD-Konfig-Schalter gesteuert:

- "ERP Logging" bzw. "SAP Logging": ``AN`` oder ``AUS``
- "SAP Logmode" bzw. "SAP Logmode:<klasse>" [Messages|Calls|Params|Results]

In einem produktiven System sollte der "SAP Logmode" auf ``Results`` stehen, zu
Diagnosezwecken empfiehlt es sich den Wert kurzfristig auf z.B. ``Results,
Messages`` zu setzen (Details bitte dem Handbuch entnehmen). In jedem Fall
sollten solche Diagnose Einstellungen aber nicht dauerhaft im produktieven
System aktiviert sein, da das ERP Log die DB aufbläht.

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

Sollte das letzte Statement mehr als 200.000 Einträge zählen kann man auch
mal überlegen aufzuräumen::

  powerscript cdb-tools/clean_cdb.py erplog --help

