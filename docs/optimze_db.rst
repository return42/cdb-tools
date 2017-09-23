.. -*- coding: utf-8; mode: rst -*-

=============
DB optimieren
=============

.. _MSSQL-Transaction-log: https://docs.microsoft.com/en-us/sql/relational-databases/logs/the-transaction-log-sql-server


MSSQL-Transaction
-----------------

Die Dateigrößen des MSSQL-Transaction-log_ können u.U. stark anwachsen,
insbesondere nach größeren SQL-UPDATE Statements die große Tabellen komplett
ändern oder leeren. Die Dateien zum Transaction-log sind in den Properties der
DB konfiguriert. Dort kann man auch die *Autogrow* Eigenschaften parametrisieren
(in einer Entwickler Installation sollte ein Limit von 2GB genug sein).

Um das Transaction-log und damit die Größe der DB Instanz zu optimieren kann man
im *MS-SQL Server Management Studio* folgendes ausführen::


  Task --> Shrink --> Database
