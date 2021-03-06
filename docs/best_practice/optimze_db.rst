.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _optimze_db:

=============
DB optimieren
=============


MSSQL
=====

TOP 10
------

Auflistung der zehn größten Tabellen.

.. code-block:: sql

   SELECT TOP 10 OBJECT_NAME(OBJECT_ID) TableName, st.row_count
     FROM sys.dm_db_partition_stats st
    WHERE index_id < 2
    ORDER BY st.row_count DESC



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
ändern oder leeren.  In einem Entwickler-System sollte es ausreichen, das
`Wiederherstellungsmodell "Einfach"
<https://docs.microsoft.com/de-de/sql/relational-databases/backup-restore/recovery-models-sql-server?view=sql-server-2017>`_
zu wählen.

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

Siehe http://return42.github.io/handsOn/oracle/
