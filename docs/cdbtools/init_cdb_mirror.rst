.. -*- coding: utf-8; mode: rst -*-

.. _FQDN: https://en.wikipedia.org/wiki/Fully_qualified_domain_name

================================================================================
Initialisierung eines CDB Spiegel-Systems
================================================================================

Eine CDB Installation wird i.d.R. wie im Handbuch beschrieben aufgebaut
(Software + Pakete installieren). In der Praxis, wenn z.B. die Nutzdaten in
einem System gebraucht werden wird man jedoch eher einen *Spiegel* einer
bestehenden Instanz aufbauen wollen.  Zum Anlegen eines solchen Spiegels werden
ein DB-Export und eine (Clone-) Kopie des ``CADDOK_BASE`` Ordners benötigt
(i.d.R. ohne BLOB storage).


CDB Software
============

Die Software (Server) muss auf dem Host bereit gestellt werden (der
``CADDOK_RUNTIME`` Ordner).

Die Installer von Microsoft installieren Software Pakete meist irgendwo unter::

  "C:\Program Files (x86)"

Nachteil an diesem Pfadnamen ist, dass er Leerzeichen enthält. Leerzeichen,
besondere Zeichen wie '-' (Minus) oder '\*' (Sternchen) sind nicht selten
Ursache von Fehlern. CDB als auch die CDBTools sollten damit umgehen können,
sobald man aber andere Tools benutzt oder eigen Skripte schreibt kann man mit
solchen Zeichen in Pfadnamen schnell Probleme bekommen. Es wird daher empfohlen
die gesammte Installation (CDB Software & Instanz) unter Pfaden abzulegen, die
keine solche Zeichen enthalten. Gern genutzt wird z.B. ``opt``::

  C:\opt\cdbsrv
  C:\opt\instance_prod_copy
  C:\opt\cdb-tools

Einige (älter) Versionen von CDB haben Probleme mit der Apache Konfiguration
wenn das Instanz Verzeichnis Leerzeichen beinhaltet. Auch wenn solche BUGs
i.d.R. gefixet werden, man sollte auf Leer- und Sonderzeichen als auch Umlaute
in Pfadnamen immer verzichten.


DB Export einspielen
====================

Der DB-Export muss mit dem DB-Management System eingespielt werden.  Dazu muss
man sich der nativen Werkzeuge des jeweiligen DB-Management System bedienen
(wird hier nicht weiter drauf eingegangen).


DB Connect einrichten
=====================

Die CDB-Instanz ist eine (Clone-) Kopie des ``CADDOK_BASE`` Ordners in der noch
in der Konfigurationsdatei ``etc/dbtab`` der DB-Connect zum oben eingespielten
DB-Spiegel eingerichtet werden muss.::

  edit $CADDOK_BASE/etc/dbtab

Für einen MS-SQL Connect ``prod_copy`` gegen eine DB Instanz mit dem Namen
``ProdCopy`` (auf dem ``localhost``) könnte der Eintrag in etwa so aussehen::

  prod_copy  mssql localhost  x SSPI/SSPI ProdCopy     - Latin1_General_CS_AS mssql

Alle anderen Einträge sollte man aus-kommentieren.  Prinzipiell müsste es danach
möglich sein eine ``cdbsh`` bzw. ein ``cdbsql`` zu starten, dass in der
CDB-Instanz läuft und gegen die ``prod_copy`` verbindet.


CDB Tools installieren
======================

Die Tools zum Initialisieren eines Spiegels werden in den CDB-Tools bereit
gestellt, deshalb müssen diese nun eingerichtet werden, sofern das nicht eh
bereits geschehen ist. Wie die CDB-Tools installiert werden ist detailliert im
Kapitel :ref:`install_cdbtools` beschrieben.


Spiegel konfigurieren
=====================

Um den Spiegel in Betrieb zu nehmen müsste man normalerweise jetzt die Dienste
für den FQDN_ des lokalen Hosts einrichten. Da noch keine CDB Instanz läuft kann
man das eigentlich nur, indem man diese Dienste via SQL Statements direkt in der
DB einrichtet. Das kann sehr mühsam sein, Erleichterung verschafft das Skript
``init-cdb-mirror`` (das in einer CDB-Tools Umgebung aufgerufen werden kann):

.. code-block:: dosbatch

  [CDB-Tools] C:\> init-cdb-mirror --help

Mit dem Skript werden die minimal erforderlichen CDB-Dienste eingerichtet um CDB
starten zu können. Alle weiteren Dienste können danach in einer CDB Sitzung
interaktiv eingerichtet werden. Die Dienste werden eingerichtet, indem die
Konfiguration eines Application Servers des *original* Systems für den lokalen
Host *übernommen* und als *default* Site eingerichtet werden.

Mit ``init-cdb-mirror`` können auch gleichzeitig die Passwörter zurück gesetzt
werden und für die Dienste werden einfache Logins (``caddok/welcome``)
eingerichtet. Diese Einstellungen sind nur für *Entwickler-Systeme* geeignet.

.. hint::

   Mit ``init-cdb-mirror`` wird ein minimales Entwickler-System eingerichtet.
   Das Tool darf niemals in einer produktiven Umgebung ausgeführt werden.

Nachdem der Spiegel mit dem ``init-cdb-mirror`` eingerichtet wurde, müsste es
möglich sein den CDB-Server mit ``CDBSVCD-START`` (s. :ref:`cdb_shortcuts`) zu
starten. Die weiteren Dienste kann man dann nach Bedarf in einer CDB-Client
Sitzung einrichten.

Will man *nutzlose* Daten aus dem Entwickler System entfernen so kann dafür das
Skript :ref:`clean-cdb <clean_cdb>` genutzt werden.
