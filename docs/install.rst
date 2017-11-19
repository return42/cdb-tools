.. -*- coding: utf-8; mode: rst -*-

.. include:: refs.txt

.. _install_cdbtools:

=====================
Installation & Update
=====================

Die CDB-Tools sind *non invasiv*, d.h. sie werden nicht in *CIM DATABASE* (CDB)
installiert.  Die Idee der CDB-Tools ist es, eine erweiterte Laufzeitumgebung
für CDB bereit zu stellen ohne das dazu die CDB Installation *verändert* werden
muss.  Mit dieser Eigenschaft können die CDB-Tools komfortabel auf jede
bestehende CDB Instanz *aufgesattelt* werden.

cdb-tools.zip
=============

Die CDBT-Tools können als ZIP *runter geladen* werden:

- download :download:`cdb-tools.zip <../dist/cdb-tools.zip>`

Der Ordner 'cdb-tools' in der ZIP Datei muss *irgendwo - hin* ausgepackt werden.

.. hint::

   Wir haben z.T. Probleme festgestellt, wenn unter Windows die CDB-Toools in
   einen anderen Laufwerksbuchstaben als CDB installiert werden. Am besten
   liegen CDB-Instanz, CDB-Software und die CDB-Tools auf dem gleichen
   Laufwerksbuchstaben.

Danach müssen nur noch ein paar ``CADDOK_*`` Variablen in der zentralen *Setup
Datei* der CDB-Tools gesetzt werden (:ref:`setup_cdbenv`) und in einer
:ref:`CDB-Tools Umgebung <cdbtools_rte>` muss noch folgendes Kommando ausgeführt
werden:

.. code-block:: dosbatch

   [CDB-Tools]$ cdbtools-fix-launcher

Eine alternative Installation, ist im Abschhnitt :ref:`clone_cdbtools`
beschrieben.  Sie basiert auf dem selben git-Reposetorie, welches bereits in dem
obigen ZIP download enthalten ist.


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
Instanz vermutlich etwas anders aussehen.

.. hint::

   Hier in der Anleitung wird der Prompt ``[cdb:prod_copy]`` genutzt, um
   anzuzeigen, das ein Kommando **in einer cdb-Shell ausgeführt werden muss**.

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


.. _clone_cdbtools:

git-clone
=========

Das Reposetorie der CDB-Tools wird mit ``git clone`` *geklont*.::

  $ git clone --recursive https://github.com/return42/cdb-tools

Wichtig ist der Schalter ``--recursive`` der sicherstellt, dass auch die
Submodule der CDB-Tools *geklont* werden. Spätere Aktualisierungen können
mittels ``git pull`` erfolgen (:ref:`update_cdbtools`).

Die nächsten Schritte sind:

- :ref:`setup_cdbenv`
- FIXME ....

.. _update_cdbtools:

Update
======

Die Aktualisierung der CDB-Tools erfolgt mittels ``git``::

   $ git pull
   $ git submodule update --recursive

In einer CDB-Tools Umgebung muss der eigentliche Update der Umegbung
durchgeführt werden.

.. code-block:: dosbatch

  [CDBTools]$ bootstrap\install-all
  ...
  [CDBTools]$ cdbtools-fix-launcher
  ...

Alternativ können die beiden Schritte (Install & fix) über das Skript
``winShortcuts/upkeep.bat`` durchgeführt werden.
