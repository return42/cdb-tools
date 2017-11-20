.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _optimze_db:

=============
DB optimieren
=============

MSSQL
=====

Datenbank-Files
---------------

Datenbank Management-Systeme geben i.d.R. einmal allozierten Platz in den
DB-Files nicht von alleine frei (`MS-SQL DB-Files`_). Nach größeren Änderungen
an den DB-Inhalten (Aufräum-Aktionen), kann es Sinn machen die DB-Files auch zu
*shrinken* (s. `MS-SQL shrink DB`_) damit der überschüssig allozierte
Plattenplatz wieder frei gegeben wird und dem System zur Verfügung steht.


MSSQL-Transaction
-----------------

Die Dateigrößen des `MS-SQL Transaction-log`_ können u.U. stark anwachsen,
insbesondere nach größeren SQL-UPDATE Statements die große Tabellen komplett
ändern oder leeren.

Um das Transaction-log und damit die Größe der DB Instanz zu optimieren kann man
im *MS-SQL Server Management Studio* folgendes ausführen::

  Task --> Shrink --> Database

Die Dateien zum Transaction-log sind in den Properties der DB konfiguriert. Dort
kann man auch die *Autogrow* Eigenschaften parametrisieren::

  Database-Properties / Files / File Type = Log

In der Spalte 'Autogrowth / Maxsize' können die Einstellungen vorgenommen
werden. In einer Entwickler Installation sollte ein Limit von 2GB genug sein.

Oracle
======

comming soon ...

