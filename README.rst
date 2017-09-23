.. -*- coding: utf-8; mode: rst -*-

================================================================================
cdb-tools
================================================================================

Die CDB-Tools sind eine (kleine) Sammlung von Skripten zur Wartung von CIM
DATABASE (CDB) Installationen.

- Dokumentation: http://return42.github.io/cdb-tools
- Reposetorie:   `github return42/cdb-tools <https://github.com/return42/cdb-tools>`_
- Author e-mail: markus.heiser@darmarit.de


Wichtige Hinweise
=================

- Mit Benutzung der CDB-Tools akzeptieren Sie die Lizenzbedingungen (siehe
  ``LICENSE.txt``).

  Für Schäden wird keine Haftung übernommen, die GPL ist die selbe, wie sie auch
  für den Linux Kernel verwendet wird.

  Testen Sie die Tools sorgfältig in einer Entwickler-Kopie bevor Sie diese auf
  ein produktives System anwenden!!!

  Insbesondere die Tools zur (Datenbank-) Optimierung basieren darauf Daten zu
  reduzieren (löschen). Ob Optimierungen solcher Art für Ihre konkreten
  Anwendungszenarien überhaupt geeignet sind oder ob dabei ggf. noch benötigte
  Daten gelöscht werden kann nicht allgemein beantwortet werden. Das Löschen von
  Daten muss immer gegen die Anwendungszenarien geprüft werden.

- Die CDB-Tools sind für CIM DATABASE ab Version 10.1 (inkl. ELEMENTS)

- Die CDB-Tools sollten nur von erfahrenen CDB Entwicklern genutzt werden, die
  wissen was die Tools machen und einschätzen können ob diese überhaupt geeignet
  sind ihre Anforderungen zu erfüllen.

- Die CDB-Tools sind derzeit noch im Aufbau. Sollten Sie Fehler finden melden
  Sie diese bitte / Danke!

- "CIM DATABASE" & "CONTACT ELEMENTS" sind Markenzeichen der `Contact Software
  GmbH <https://www.contact-software.com>`_. Wir sind NICHT die Contact Software
  GmbH und die CDB-Tools sind auch nicht zertifiziert oder sonst was. Es handelt
  sich lediglich um eine Sammlung von Skripten, die *auf eigene Gefahr* genutzt
  werden können.


Installation
============

Eine Installation im eigentlichen Sinne ist nicht erforderlich. Die CDB-Tools
müssen lediglich einmal *geklont* (download) werden und immer in einer CDB-Shell
(``cdbsh``) ausgeführt werden.::

  $ git clone --recursive https://github.com/return42/cdb-tools
  $ $CADDOK_RUNTIME/cdbsh
  cdb$ cd cdb-tools
  cdb$ powerscript ... # Name des Skripts, das ausgeführt wird
