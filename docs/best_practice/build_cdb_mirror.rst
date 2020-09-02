.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _build_cdb_mirror:

================================================================================
Aufbau eines CDB Spiegel-Systems
================================================================================

.. sidebar:: Info

   Der Aufbau eines Spiegels ist mit einem DUMP schneller möglich und die
   Qualitätssicherung einer Änderung lässt sich gegen die *echten* Nutzdaten
   testen.

Eine CDB Installation wird i.d.R. wie im Handbuch beschrieben aufgebaut:
*"Software + Pakete inkl. Kundenpaket installieren"*.  Diese Vorgehensweise hat
den Vorteil, dass sich die zu transportierenden Änderungen auf die geänderten
Module (i.d.R. das Kundenmodul ``cust.plm``) beschränken.  Theoretisch lässt
sich damit eine vollständige aber immer noch relativ *schlanke* Anbindung des
Lieferanten abbilden.

In der Praxis kann diese Vorgehensweise aber auch erhebliche Nachteile
resp. Einschränkungen mit sich bringen.  So verfügt der Lieferant mit dem
Kundenpaket beispielsweise noch nicht über Nutzdaten, wie sie typischer Weise im
produktiven Betrieb aufgebaut werden (mit all ihren *Eigentümlichkeiten*).

Folgend wird alternativ ein Vorgehen beschrieben, bei dem ein **Spiegel** der
ganzen CDB-Instanz erstellt wird.  Um dieses Verfahren zu etablieren, werden
keine CDB-Tools benötigt.  Die CDB-Tools können aber den Aufbau des Spiegels
erheblich erleichtern (:ref:`mirror_init`).  Der Spiegel wird aus folgenden
Komponenten aufgebaut:

.. sidebar:: CADDOK_BASE versionieren

   Es empfiehlt sich den ganzen CADDOK_BASE Ordner in die Versionsverwaltung
   (git_) mit aufzunehmen

DUMP
  Ein Export der Datenbank.

CADDOK_BASE
  Kopie des Instanzordners

BLOBS
  Die BLOBs der Anwendung sind in CDB-Modulen (:ref:`mirror_importblobs`).
  Optional kann auch der Vault in den Spiegel übernommen werden
  (:ref:`mirror_vault`).

.. _mirror_DBDump:

DB Dump
=======

.. sidebar:: Export am Branch-Point

   Bevor der DB Export erstellt wird (oder unmittelbar danach) sollte ein
   :ref:`Dump der Konfiguration <rm_dump_into_scm>` erfolgen.

Die DB Exporte können sehr groß sein, meist empfiehlt es sich die DB vorher zu
bereinigen, s.a. :ref:`clean_cdb`.  Der DB-Export muss mit dem DB-Management
System eingespielt werden.  Dazu muss man sich der nativen Werkzeuge des
jeweiligen DB-Management Systems bedienen (wird hier nicht weiter erläutert).

.. _mirror_CADDOK_BASE:

CADDOK_BASE
===========

Der CADDOK_BASE Ordner kann ein ZIP sein, besser ist es aber ``CADDOK_BASE`` zu
versionieren, s.a. `einheitliche Ordnerstrukturen`_.  Alle Änderungen zum
Betrieb einer Instanz werden so versioniert und Änderungen sind damit
*reproduzierbar*.  Als *ignore list* für git_ eignet sich
:ref:`caddok_base_gitignore`. ::

  git clone <URL des gemeinsamen Repository>
  git checkout <branch-point>


.. _mirror_dbconnect:

DB Connect einrichten
=====================

Wurde die Clone-Kopie der CDB-Instanz lokal angelegt und der :ref:`DB Import
<mirror_DBDump>` durchgeführt, wird als Nächstes der DB-Connect eingerichtet.
In der Konfigurationsdatei ``etc/dbtab`` werden die DB-Connect eingetragen.  Für
einen MS-SQL Connect ``cust_dev`` gegen eine DB Instanz mit dem Namen
``cust_dev`` (auf dem ``localhost``) könnte der Eintrag in etwa so aussehen::

  # NAME   RDBMS NET       DEFAULT LOGIN     DBMS-HOME DBMS-ID DBMS-LANG            DBMS_DRIVER
  cust_dev mssql localhost x       SSPI/SSPI cust_dev  -       Latin1_General_CS_AS mssql

Ein anderes Beispiel für eine Oracle Datenbank auf dem Host 'dbhost' im eigenen
Subnetz::

  # NAME   RDBMS  NET                   DEFAULT LOGIN             DBMS-HOME DBMS-ID DBMS-LANG               DBMS_DRIVER
  cust_dev oracle //dbhost:1521/orclpdb x       cust_dev/cust_dev -         -       german_germany.AL32UTF8 oracle

Alle anderen Einträge sollte man aus-kommentieren.  Prinzipiell müsste es danach
möglich sein eine ``cdbsh`` bzw. ein ``cdbsql`` zu starten, dass in der
CDB-Instanz läuft und gegen die ``cust_dev`` Datenbank verbindet.::

  DOS> cdbsql.exe -v
  Executing Script: C:\share\cust\etc\site.conf
  Encoding IN cp850 OUT cp850
  SQL>


.. _mirror_cdbtools:

CDB Tools einrichten
====================

Die Tools zum Initialisieren eines Spiegels werden in den CDB-Tools bereit
gestellt, deshalb müssen diese nun eingerichtet werden, sofern das nicht eh
bereits geschehen ist.  Wie die CDB-Tools installiert werden ist detailliert im
Kapitel :ref:`install_cdbtools` beschrieben.


.. _mirror_init:

Spiegelsystem initialisieren
============================

.. sidebar:: Tipp

   Um *nutzlose* Daten aus dem Entwickler System zu entfernenen eignet sich das
   Skript :ref:`clean-cdb <clean_cdb>`.

Um den Spiegel in Betrieb zu nehmen müsste man normalerweise jetzt die Dienste
für den FQDN_ des lokalen Hosts einrichten.  Da noch keine CDB Instanz läuft
kann man das eigentlich nur, indem man diese Dienste via SQL Statements direkt
in der DB einrichtet.  Das kann sehr mühsam sein, Erleichterung verschafft das
Skript ``init-cdb-mirror``, das in einer CDB-Tools Umgebung aufgerufen werden
kann.

.. caution::

   Das Tool ``init-cdb-mirror`` darf niemals in einer produktiven Umgebung
   ausgeführt werden!

.. code-block:: dosbatch

  [CDBTools]$ init-cdb-mirror

Mit dem Skript werden die minimal erforderlichen CDB-Dienste eingerichtet um CDB
starten zu können.  Alle weiteren Dienste können danach in einer CDB Sitzung
interaktiv eingerichtet werden.

Die Dienste werden eingerichtet, indem die Konfiguration eines Application
Servers des *original* Systems für den lokalen Host *übernommen* und als
*default* Site eingerichtet werden.  Mit ``init-cdb-mirror`` können auch
gleichzeitig die Passwörter zurück gesetzt werden und für die Dienste werden
einfache Logins (``caddok/welcome``) eingerichtet.  Diese Einstellungen sind nur
für *Entwickler-Systeme* geeignet.


.. _mirror_importblobs:

BLOBs einspielen
================

Nachdem der Spiegel mit dem ``init-cdb-mirror`` eingerichtet wurde, müsste es
möglich sein, den CDB-Server z.B. mit :ref:`cdb_localhost_START_bat` zu starten.
Die weiteren Dienste kann man dann nach Bedarf in einer CDB-Client Sitzung
einrichten.  Zum Einspielen der BLOBs aus den Modulen muss der Service-Daemon
gestartet werden, da die Instanz noch nicht voll aufgebaut ist, wird er für
*Update* gestartet.::

  $ cdbsvcd -d --for_update

Der BlobStore Dienst sollte dann soweit laufen und es können die BLOBs aus den
Modulen in den BlobStore importiert werden::

  $ cdbpkg import_blobs
  Imported 42 missing blob(s)


.. _mirror_vault:

Vault übernehmen
================

.. sidebar:: optional

   Die Vaults aus dem PROD System in das Entwickler System zu übernehmen ist
   eher selten erforderlich, aber auch solche Szenarien kann es geben.

Um den Speicher eines BlobStore Servers komplett zu übernehmen müssen Kopien der
Ordner ``base_path`` und ``vault_path`` angelegt werden (siehe CDB
Administration Konfiguration des BlobStore Dienstes).  In den meisten Setups ist
der ``vault_path`` bereits im ``base_path`` enthalten.  Im ``base_path``
befinden sich die SQLite Datenbank ``filestore.db`` in welcher der BlobStore
Server seine Hash-Value Objekte verwaltet.  Siehe auch im CDB Plattform Handbuch
im Abschnitt *"Die BLOB-Storage-DB"*:

.. code:: bat

   cd /D %CADDOK_BASE%\storage\blobstore
   sqlite3 filestore.db

.. code:: sql

   sqlite> .tables
   -- backup    blobs     metadata  vaults
   sqlite> .schema vaults
   --   CREATE TABLE vaults (
   --          vault_id INTEGER PRIMARY KEY,
   --          path     TEXT NOT NULL);
   -- ...
   sqlite> .schema blobs
   --   CREATE TABLE blobs (
   --          id          TEXT PRIMARY KEY,
   --          vault_id    INTEGER,
   --          filename    TEXT NOT NULL,
   --          size        INTEGER,
   --          created_at  TIMESTAMP);
   -- ...
   sqlite> select vault_id, count(*) from blobs group by vault_id;
   -- 1|nnnn
   -- 2|mmmm
   sqlite> select * from vaults;
   -- 1|z:\blobstore\vault\
   -- 2|c:\share\cdb_cust_dev\storage\blobstore\vault\


  sqlite> select vault_id, count(*) from blobs group by vault_id;
  ...

Mit einem *Distinct* auf die Vault-ID kann man nachschauen, welche Vaults
genutzt werden.  In der Relation ``vaults`` kann man sehen, wo diese Vaults
lokalisiert sind:

.. code-block:: sql

  sqlite> select distinct vault_id from blobs;
  sqlite> select * from vaults;

.. code-block:: none

  1|c:\share\cdb_cust_dev\storage\blobstore\vault\

Der ``vault.path`` Wert muss entsprechend dem Spiegel neu gesetzt werden:

.. code-block:: sql

  sqlite> update vaults set path='X:\to\my\blobstore\vault\'
     ...> where vault_id = 1;


.. hint::

   Bevor Änderungen an der ``filestore.db`` vorgenommen werden, sollte
   sichergestellt sein, dass die DB nicht zeitgleich von einem BlobStore Server
   benutzt wird (BlobStore Dienst ggf. stoppen).


Einheitliche Ordnerstrukturen
=============================

.. sidebar:: Leerzeichen in Pfadnamen vermeiden

   Alte Versionen von CDB haben beispielsweise Probleme mit der Apache
   Konfiguration, wenn das Instanz Verzeichnis Leerzeichen beinhaltet.  Auch
   wenn solche BUGs i.d.R. gefixet werden, man sollte auf Leer- und
   Sonderzeichen als auch Umlaute in Pfadnamen immer verzichten.


.. _Deployment: https://de.wikipedia.org/wiki/Softwareverteilung

CDB Instanzen erstrecken sich über homogene Systemlandschaften und weltweite
Standorte hinweg.  Um das Deployment_ dafür nicht weiter zu verkomplizieren
empfiehlt es sich eine einheitliche Ordnerstruktur unternehmensweit zu
etablieren.  Die Software (Server) muss auf dem Host bereit gestellt werden (der
``CADDOK_RUNTIME`` Ordner).  Die *Installer* von Microsoft installieren Software
Pakete meist irgendwo unter::

  "C:\Program Files (x86)"

Nachteil an diesem Pfadnamen ist, dass er Leerzeichen enthält. Leerzeichen,
besondere Zeichen wie ``-`` (Minus) oder ``*`` (Sternchen) sind nicht selten
Ursache von Fehlern. CDB als auch die CDB-Tools sollten damit umgehen können,
sobald man aber andere Tools benutzt oder eigene Skripte schreibt kann man mit
solchen Zeichen in Pfadnamen schnell Probleme bekommen.  Es wird daher empfohlen
die gesamte Installation (CDB Software & Instanz) unter Pfaden abzulegen, die
keine solche Zeichen enthalten. Gern genutzt wird z.B. ``opt`` oder wie hier in
den CDB-Tools oft auch ``share``::

  C:\share\contact\cdbsrv-11.3.10    <-- CDB Software
  C:\share\cdb_cust_dev              <-- CDB Instanz
  C:\share\cdb-tools                 <-- CDB-Tools

.. _caddok_base_gitignore:

``CADDOK_BASE/.gitignore``
--------------------------

.. _`.gitignore`: https://git-scm.com/docs/gitignore

Um den ``CADDOK_BASE`` Ordner im git_ zu versionieren eignet sich die folgende,
exemplarische `.gitignore`_ , die ggf. in Teilen noch angepasst werden muss:

.. code-block:: none

   *.pyc
   *.pyo
   *~
   *.swp
   */#*#
   .#*
   .DS_Store
   .cvsignore
   .svn
   #~$*[.docx|.xlsx]
   #~*[.doc|.xls]

   # Das Systemverzeichnis instance/app_conf wird von cdbpkg verwaltet und darf
   # nicht versioniert resp. distributiert werden.
   /app_conf/

   # Directory for dynamic configuration.  This is used by various services to
   # store temporary configuration items.  It can be excluded from backups.
   /etcd/

   # TEMP-Daten und der Package Ordner werden nicht versioniert
   /tmp/
   /CDBAPPS

   # Der Storage hat sein eigenes Backup Konzept.  Unter dem storage-Ordner liegt
   # allerdings auch die Konfiguration des Index Servers, die muss mit in die
   # Versionsverwaltung.

   /storage/*
   !/storage/index
   /storage/index/*
   !/storage/index/search
   /storage/index/search/*
   !/storage/index/search/conf

   # Das 3D Connect Release 15.5.1.2 neigt dazu Änderungen an Dateien im
   # site-package vorzunehmen. Wir behandeln die AdobeFnt11.lst Dateien, wie auch
   # schon die *.pyc Dateien.
   # site-packages/cs.threed-15.5*.egg/win64/release/img/resource/CMap/AdobeFnt11.lst
   # site-packages/cs.threed-15.5*.egg/win64/release/img/resource/Font/AdobeFnt11.lst

