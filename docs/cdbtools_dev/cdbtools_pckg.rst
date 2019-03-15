.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_pckg:

=============================
Paketmanagement der CDB-Tools
=============================

Die CDB-Tools sind eine Umgebung in der zusätzliche Software in CDB Prozessen
bereit gestellt werden kann.  Einiges wird bereits in der Standard-Installation
der CDB-Tools bereit gestellt, anderes kann individuell nachinstalliert werden.
Die CDB-Tools Umgebung bietet im Kern zwei unterschiedliche Methoden zur
Installation zusätzlicher Software:

1. Zusätzliche Python Pakte: bereitgestellt  über PyPi_ (pip)
2. Zusätzliche Software: bereitgestellt über die CDB-Tools Entwicklung

.. _cdbtools_pip:

Python Pakte der CDB-Tools
==========================

Python Pakete werden mit dem Kommando pip_ installiert.  Es existiert ein
``pip`` in der CDB-Installation und ein weiteres ``pip`` in der CDB-Tools
Umgebung.  In der CDB-Tools Umgebung (z.B. ``winShortcuts/tools-sh.bat``):

.. code-block:: dosbatch

  C:\share\cdb_cust_dev
  [CDBTools]$ pip --version
  pip 19.0.3 from C:\share\cdb-tools\py27\Python27\site-packages\pip (python 2.7)


Die CDB-Tools beziehen bereits diverse Pakete über PyPi_, die in der
:origin:`bootstrap/requirements.txt` Datei aufgelistet sind.  Um die CDB-Instanz
resp. die CDB-Software nicht zu manipulieren muss die Installation der Pakete
immer in das User-Scheme (``PYTHONUSERBASE``) der :ref:`Laufzeitumgebung
<cdbtools_rte>` erfolgen.

.. code-block:: dosbatch

  [CDBTools]$ pip install --user <package-name>

.. hint::

   Bei der Verwendung von ``pip install`` in den CDB-Tools sollte immer die
   Option ``--user`` verwendet werden.  Bei unsachgemäßer Installation von
   Paketen mit pip_ kann es passieren, dass in die CDB-Software installiert
   wird, deshalb immer erst mal in einem *unkritischen* System testen!

In der CDB-Tools Umgebung ist die ``PIP_CONFIG_FILE%`` Variable gesetzt.  Die
`pip.ini` Konfiguration liegt unter :origin:`bootstrap/pip.ini`:

.. code-block:: dosbatch

  [CDBTools]$ echo %PIP_CONFIG_FILE%
  C:\share\cdb-tools\bootstrap\pip.ini


.. _cdb_pip:

Python Pakete in CDB
--------------------

Ab CDB-15 ist auch ein pip in CDB enthalten.  Dieses wird nicht von den
CDB-Tools genutzt, die haben ihr eigenes pip resp. Paketmanagement.  In einer
Standard CDB-Installation (z.B. ``winShortcuts/cdb-sh.bat``):

.. code-block:: dosbatch

  [cdbsrv-11.3.10:cust_dev] C:\share\cdb_cust_dev> pip --version
  pip 9.0.1 from C:\share\contact\cdbsrv-11.3.10\lib\site-packages (python 2.7)


.. warning::

   In dem Plattform Handbuch von CDB wird dieses pip vorgestellt, dort werden
   auch die Einschränkungen erwähnt.  Mit diesem pip wird in die CDB-Software
   resp. in den CDB-Instanz installiert.  Bei dem pip aus CDB muss der Schalter
   ``--target`` mit angegeben werden, sonst werden die Pakete in den
   CDB-Software Ordner installiert.  Werden (neue) Python Pakete damit
   installiert, so kann es sein, dass deren Abhängigkeiten aktuelle Versionen
   von Python Paketen benötigen, die bereits mit der CDB-Software ausgeliefert
   werden.  Diese werden dann ebenfalls im *target* Ordner installiert.  Damit
   wird dann auch die CDB-Software resp. die Standard CDB-Umgebung verändert, da
   nun auch die CDB Module (ungetestet) diese neuen Bibliotheken nutzen.

Die CDB-Tools Umgebung wurde entwickelt um genau das zu vermeiden
(*non-Invasiv*) und um eine klare Trennung zwischen CDB-Standard Umgebung und
einer *erweiterten* Umgebung zu haben.  Deshalb ist es im allgemeinen zu
empfehlen, das pip aus den CDB-Tools zu verwenden, siehe ":ref:`cdbtools_pip`".


.. tip::

   Egal ob CDB oder CDB-Tools, wenn Sie auch bei unsachgemäßer Nutzung sicher
   vermeiden wollen, dass Manipulationen an der CDB-Software sattfinden, dann
   müssen Sie den CDB -Admins bzw. -Entwicklern die Schreibberechtigungen auf
   den ``CADDOK_RUNTIME`` Ordner entziehen.


.. _cdbtools_software:

Softwarepakete der CDB-Tools
============================

.. todo::

   Die Doku zu den Softwarepaketen aus den CDB-Tools muss noch erstellt werden.
