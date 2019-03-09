.. -*- coding: utf-8; mode: rst -*-

================================================================================
CDB Tools
================================================================================

Die CDB-Tools sind eine Laufzeitumgebung die komfortabel auf jede bestehende CIM
DATABASE (CDB) Instanz *aufgesattelt* werden kann, ohne dass die CDB Instanz
dazu angepasst werden muss (*non invasiv*).  Die Umgebung stellt Erweiterungen
in CDB Prozessen bereit und über das Paketmanagement der CDB-Tools steht die
Welt der `PyPi`_ Pakete in CDB zur Verfügung ohne diese in die CDB Instanz
installieren zu müssen.  Die CDB-Tools richten sich an erfahrene CDB -Entwickler
und -Administratoren.  Vor Benutzung bitte die *wichtigen Hinweise* lesen.

- Dokumentation: http://return42.github.io/cdb-tools
- Reposetorie:   `github return42/cdb-tools <https://github.com/return42/cdb-tools>`_
- Author e-mail: markus.heiser@darmarit.de

Bitte beachten:

- wichtige Hinweise: https://return42.github.io/cdb-tools/hints.html
- Installation:      https://return42.github.io/cdb-tools/install.html


.. hint::

   Die CDB-Tools verfügen über git Submodule.  Zum Clonen sollte::

     git clone --recursive https://github.com/return42/cdb-tools

   verwendet werden.  Falls man das vergessen hat, kann man das mit::

     git submodule init
     git submodule update

   nachholen.
