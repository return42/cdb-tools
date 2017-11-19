.. -*- coding: utf-8; mode: rst -*-

.. include:: refs.txt

.. _cdbtools_pckg:

Paketmanagement der CDB-Tools
=============================

Die CDB-Tools bringen ihr eigenes Paket-Managment (pip) mit, dass wenige bis
keine Abhängigkeiten zu CDB hat, also unabhängig von CDB genutzt werden kann (in
CDB 10 gibt es beispielsweise kein pip).

Die Installation der Pakete muss immer in das User-Scheme (``PYTHONUSERBASE``)
der :ref:`Laufzeitumgebung <cdbtools_rte>` erfolgen um die CDB Instanz nicht zu
manipulieren (Option ``--user``). ::

  [CDBTools]$ pip install --user <package-name>

Die pip Konfiguration liegt unter::

  %CDBTOOLS_HOME%\bootstrap\pip.ini

Die CDB-Tools beziehen bereits diverse Pakete die in der Datei::

  bootstrap/requirements.txt

gelistet sind.

.. hint::

   Bei unsachgemäßer Installation von Paketen mit pip kann die CDB-Software
   u.U. beschädigt werden, deshalb immer erst mal in einem *unkritischen* System
   testen!

   Setzt man den Schalter ``--user`` nicht, dann besteht immer die Gefahr, dass
   das pip versucht ein Paket aus der CDB-Software zu deinstallieren und durch
   ein neueres unter zu ersetzen. Damit wäre die CDB-Software manipuliert, was
   unbedingt vermieden werden muss (Stichwort: *non invasive Installation*).
