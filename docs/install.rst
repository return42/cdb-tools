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
bestehende CDB Instanz *aufgesattelt* werden. Die CDB-Tools können als ZIP
*runter geladen* werden (siehe ``cdbtools-zip`` in den `Releases`_)

Der Ordner ``cdb-tools`` in der ZIP Datei muss *irgendwo - hin* ausgepackt
werden.  Danach müssen nur noch ein paar ``CADDOK_*`` Variablen in der CDB-Tools
Umgebung gesetzt werden (:ref:`setup_cdbenv`). Initial sollte noch einmal das
Skript:

.. code-block:: dosbatch

   [CDBTools]$ cdbtools-fix-launcher

in einer CDB-Tools Shell ausgeführt werden (siehe Hinweise Abschnitt
:ref:`Portable <cdbtools_portable>`).  Bezüglich Aktualisierung der CDB-Tools
siehe :ref:`update_cdbtools`.  Eine alternative Installation, ist im Abschhnitt
:ref:`clone_cdbtools` beschrieben.  Sie basiert auf dem selben git-Reposetorie,
welches bereits in dem obigen ZIP download enthalten ist.

.. _setup_cdbenv:

Setup cdbEnv
============

Damit die CDB-Tools und die CDB Installation *zueinander finden* müssen in der
Datei ``winShortcuts/cdbEnv.bat`` folgende Umgebungen angepasst werden.

.. code-block:: dosbatch

   SET "CADDOK_DBNAME=prod_copy"
   SET "CADDOK_RUNTIME=C:\share\cdb_sw"
   SET "CADDOK_BASE=C:\share\customer\instance_prod_copy"

Nachdem die Umgebung korrekt gesetzt wurde, ist es möglich mit
``winShortcuts/cdb-sh.bat`` eine CDB-Shell zu starten:

.. code-block:: dosbatch

  $ C:\share\cdb-tools\winShortcuts\cdb-sh.bat
  ...
  [cdb:prod_copy] ...

Den Prompt ``[cdb:prod_copy]`` setzt die CDB-Shell, er wird in der eigenen
Instanz vermutlich etwas anders aussehen (s.a. :ref:`rte_prompt`).

Um zu überprüfen ob die Umgebung korrekt gesetzt ist sollte man sich die
``CADDOK_*`` Variablen anschauen::

  [cdb:prod_copy] C:\> SET CADDOK
  CADDOK_DEFAULT=prod_copy@:C:\share\customer\instance_prod_copy
  CADDOK_TMPDIR=C:\share\customer\instance_prod_copy\tmp
  CADDOK_LOGDIR=C:\share\customer\instance_prod_copy\tmp
  ...

Stimmen nicht alle Einstellungen, so muss man ggf. noch die ``etc/site.conf``
oder eine der anderen ``etc/*.conf`` Dateien anpassen (normale CDB
Konfiguration).

