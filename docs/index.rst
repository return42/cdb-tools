.. -*- coding: utf-8; mode: rst -*-
.. include:: refs.txt

================================================================================
CDB Tools
================================================================================

.. sidebar:: Good to know ..

   - `Get git started <http://return42.github.io/handsOn/slides/git/#/>`__
   - `CDB Entwicklung <slides/cdb_comp/index.html>`__

Die CDB-Tools sind eine :ref:`Laufzeitumgebung <cdbtools_rte>` die komfortabel
auf jede bestehende CIM DATABASE (CDB) Instanz *auf-gesattelt* werden kann, ohne
dass die CDB Instanz dazu angepasst werden muss (*non invasiv*).

Die Umgebung stellt Erweiterungen in CDB Prozessen bereit und über das
:ref:`Paketmanagement der CDB-Tools <cdbtools_pckg>` steht die Welt der `PyPi`_
Pakete in CDB zur Verfügung, ohne diese in die CDB Instanz installieren zu
müssen.  Die CDB-Tools richten sich an erfahrene CDB -Entwickler und
-Administratoren.  Vor Benutzung bitte die :ref:`wichtigen Hinweise
<cdbtools_hint>` lesen.


.. toctree::
   :maxdepth: 2

   install
   winShortcuts/index
   cdbtools_dev/index
   tools/index
   best_practice/index
   hints
   LICENSE


.. sidebar:: Projekt

   - `Sources <https://github.com/return42/cdb-tools>`_
   - :ref:`todo-list`
   - markus.heiser@darmarIT.de

Aktuell wurden die CDB-Tools lediglich auf Windows getestet, grundsätzlich sind
sie aber auch unter Linux lauffähig. Im weiteren Verlauf werden die CDB-Tools
noch auf Linux getestet und ständig erweitert. Ihre Mitarbeit wird benötigt und
ist willkommen, sei es in Form von `Fehlermeldungen
<https://github.com/return42/cdb-tools/issues>`_ , Anregungen oder aber
Pull-Requests (PR). Möchten Sie uns Ihre CDB Umgebung zur Verfügung stellen um
darin die CDB-Tools zu testen, so nehmen Sie bitte Kontakt zu uns auf
(markus.heiser@darmarit.de).  Danke!

