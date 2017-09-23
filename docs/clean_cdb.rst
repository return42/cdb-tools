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

ACHTUNG:  ES WERDEN DATEN GELÖSCHT!


Löschen der Lizenz-Statistik (lstatistics)
==========================================

Die Lizenstatistik wächst kontinuierlich an. In lang laufenden Systemen mit
vielen Benutzern ist die Statistik oftmals eine der größten Tabellen. Sofern
die Statistik nicht ausgewertet wird, kann sie auch von Zeit zu Zeit mal
gelöscht werden.


Bereinigen der MQ-Anwendungen (mq)
==================================

Es werden alle Message-Queues aufgelistet und Vorschläge zum Reduziern der
Daten gemacht.


Reduzieren der ERP-Log-Einträge
===============================

Das ERP-log wächst bei Fehlern im SAP-Abgleich rasant an. Mit dieser
Operation können die sich wiederholenden ERP Einträge im Log eines Objektes
auf das wesentlich *runter* gekürzt werden.

