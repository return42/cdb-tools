.. -*- coding: utf-8; mode: rst -*-

.. _optimze_db::

=============
DB optimieren
=============

Oracle
======

comming soon ...


MSSQL
=====

.. _MSSQL-Transaction-log: https://docs.microsoft.com/en-us/sql/relational-databases/logs/the-transaction-log-sql-server


MSSQL-Transaction
-----------------

Die Dateigrößen des MSSQL-Transaction-log_ können u.U. stark anwachsen,
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
