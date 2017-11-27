.. -*- coding: utf-8; mode: rst -*-
.. include:: refs.txt

.. _install_cdbtools:

============
Installation
============

Die CDB-Tools sind *non invasiv*, d.h. sie werden nicht in *CIM DATABASE* (CDB)
installiert.  Die Idee der CDB-Tools ist es, eine erweiterte Laufzeitumgebung
für CDB bereit zu stellen ohne das dazu die CDB Installation *verändert* werden
muss.  Mit dieser Eigenschaft können die CDB-Tools komfortabel auf jede
bestehende CDB Instanz *aufgesattelt* werden.

- download ``cdbtools-zip`` `Releases`_

  Die CDB-Tools können als fertiges ZIP *runter geladen* werden (siehe
  ``cdbtools-zip`` in den `Releases`_)

- entpacken ``cdbtools-zip``

  Der Ordner ``cdb-tools`` in der ZIP Datei muss *irgendwo - hin* ausgepackt
  werden (s.a. :ref:`Hinweise <cdbtools_portable>` ).

- CDB in den CDB-Tools bekannt machen

  In der CDB-Tools Umgebung müssen ein paar ``CADDOK_*`` Variablen angepasst
  werden (s.a. :ref:`setup_cdbenv`). Datei ``winShortcuts/cdbEnv.bat``:

  .. code-block:: dosbatch

   SET "CADDOK_DBNAME=prod_copy"
   SET "CADDOK_RUNTIME=C:\share\cdb_sw"
   SET "CADDOK_BASE=C:\share\customer\instance_prod_copy"

- cdbtools-fix-launcher

  Initial sollte noch einmal das Skript:

  .. code-block:: dosbatch

     [CDBTools]$ cdbtools-fix-launcher

  in einer CDB-Tools Shell ausgeführt werden (siehe Hinweise Abschnitt
  :ref:`Portable <cdbtools_portable>`).

Bezüglich Aktualisierung der CDB-Tools siehe :ref:`update_cdbtools`.  Eine
alternative Installation, ist im Abschhnitt :ref:`clone_cdbtools` beschrieben.
Sie basiert auf dem selben git-Reposetorie, welches bereits in dem obigen ZIP
download enthalten ist.
