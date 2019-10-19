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

1. Die CDB-Tools können als fertiges ZIP *runter geladen* werden.  Siehe aktuelle
   ``cdb-tools.zip`` in den `Releases`_.

2. Der Ordner ``cdb-tools`` in der ZIP Datei muss *irgendwo - hin* ausgepackt
   werden (s.a. :ref:`Hinweise <cdbtools_portable>` ).

3. CDB in den CDB-Tools bekannt machen.  In der CDB-Tools Umgebung müssen ein
   paar ``CADDOK_*`` Variablen angepasst werden (s.a. :ref:`setup_cdbenv`).

.. code-block:: dosbatch

   REM Datei winShortcuts/cdbEnv.bat

   SET "CADDOK_BASE=C:\share\cdb_cust_dev"
   SET "CADDOK_DBNAME=cust_dev"

   SET "CADDOK_RUNTIME=C:\share\contact\cdbsrv-11.3.10"
   SET "CADDOK_CLIENT_HOME=C:\share\contact\cdbpc-11.3.0.10"

Damit ist die Installation bereits abgeschlossen.

.. tip::

   Wenn die CDB-Tools in mehreren Instanzen genutzt werden sollen, dann kopiert
   man am besten den :origin:`winShortcuts` Ordner in die CDB-Instanzen und
   passt zusätzlich noch ``CDBTOOLS_HOME`` an.

   .. code-block:: dosbatch

      SET "CDBTOOLS_HOME=C:\share\cdb-tools"


Hinweise
========

Ab Version 11.3 verwendet CDB ELEMENTS die 64bit Bibliotheken (``win_amd64`` ist
der Default in den CDB-Tools), weshalb für ältere Versionen noch die Variable
``PIP_PY_PLATFORM`` gesetzt (*aus-kommentiert*) werden muss:

.. code-block:: dosbatch

     SET PIP_PY_PLATFORM=win32

Initial sollte noch einmal das folgende Skript in einer CDB-Tools Shell
ausgeführt werden (siehe Hinweise Abschnitt :ref:`Portable
<cdbtools_portable>`):

.. code-block:: dosbatch

   [CDBTools]$ cdbtools-fix-launcher

Bezüglich Aktualisierung der CDB-Tools siehe :ref:`update_cdbtools`.  Eine
alternative Installation, ist im Abschhnitt ":ref:`cdbtools_repo`" beschrieben.
Sie basiert auf dem selben git-Reposetorie, welches bereits in dem obigen ZIP
download enthalten ist.
