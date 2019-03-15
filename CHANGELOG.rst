2019-03-15 Release 2.0

  Im Major-Release 2.0 wurde die CDB-Tools Umgebung entschlackt, die Bootsrap &
  Build Workflow wurde vereinfacht und robuster ausgelegt.  Die Dokumentation
  wurde komplett überarbeitet.

  * 202e60e origin/master fspath: git-submodule auf 'master' aktualisiert
  * 64e38e3 ptpdb: git-submodule gelöscht
  * b9f54ff ptpdb: gelöscht / Unterstützung für python-prompt-toolkit 2.0 fehlt
  * 945ab2d doc: Überarbeitung verschiedener Kapitel
  * 8f56141 doc: Überarbeitung verschiedener Kapitel
  * cfb37bf doc: Überarbeitung "Installation", "Bootsrap & Download" und Build
  * 493f81c doc: Spiegelsysteme nach "best practice" verschieben
  * 1a14de9 doc: Überarbeitung "Einrichten eines Spiegelsystem"
  * 12c6c1d cdbEnv.bat: Normalisierung auf einfache Defaults
  * 0d1066a ptpython: Konfiguration für Version >= 2.0
  * 7090067 cdb-sh.bat: fix C&P typo
  * 612d2f3 bootstrap & install: komplette Überarbeitung (WIP)
  * e11ac17 boilerplate: update
  * cdbc289 bootstrap & install: komplette Überarbeitung (WIP)
  * 5a53bb0 bootstrap & install: komplette Überarbeitung (WIP)
  * e5a77b6 init_cdb_mirror.py: Kommentare ergänzt
  * 26b2972 init_cdb_mirror: Setzen der Methode zur Authentifizierung
  * 6cd2bb2 init_cdb_mirror: Behandlung falls ein Dienst nicht exisitiert
  * bfd32b2 init_cdb_mirror: richtiges Setup für ELEMENTS 15.1 verwenden
  * 40eeeea clean-cdb bugifx: SQL-DATE Felder mit SQLdbms_date formatieren
  * d5716f7 boilerplate update git://github.com/return42/boilerplate 9ea6451
  * d6a1587 CHANGELOG: fixed typo
  * fb07836 Kapitel "Merge mit git und cdbpkg Tools" überarbeitet
  * 75475fd init_cdb_mirror: Anpassungen für ELEMENTS 15.2
  * b4536ad tinker: Einsammeln der CDB Dokumentation im PDF Format
  * 4fe8b2e doc: Installationsanleitung Hinweis auf winShorcuts Kopie
  * ee12b64 make: targets für bootstrap, download und dist angelegt
  * 6b4b5eb pip-download: Ordner wird als ZIP distibutiert

2018-03-04 Release 1.1 <markus.heiser@darmarit.de>

  * slides: cdbpkg & SCM / big picture als SVG erstellt
  * doc: Artikel 'Releasemanagement und CONTACT Elements'
  * SVG: die SVG Dateien etwas aufgeräumt und begradigt
  * sphinx-autobuild: Autobuild HTML documentation while editing.
  * shortcuts: BugFix - tools-localhost-START
  * kleinere Korrekturen Foliensammlung CDB-Komponentenarchitektur
  * ConEmu: Alpha Transparenz auf RDPs sehr langsamm.
  * CDB15: CADDOK_INSTALLDIR ist in CDB-15 erforderlich
  * init_cdb_mirror: Prüfung des vault_path Arguments (BLOB-Storage)

2017-11-27 Release 1.0.1 <markus.heiser@darmarit.de>

  * build: dist (ZIP) unter Einbeziehung des ./templates Ordners
  * build: bugfix der download URL
  * docs: Intsalaltionsprozess etwas vereinfacht beschrieben

2017-11-21 Release 1.0 <markus.heiser@darmarit.de>

  * inital
