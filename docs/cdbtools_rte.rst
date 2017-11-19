.. -*- coding: utf-8; mode: rst -*-

.. include:: refs.txt

.. _cdbtools_rte:

================
Laufzeitumgebung
================

Zur Erweiterung der Laufzeitumgebung von CDB Prozessen nutzen die CDB-Tools die
Umgebungsvariablen:

``PATH``:
  In den Shell-Umgebungen werden zusätzliche Kommandos zur Verfügung gestellt.

``PYTHONUSERBASE``:

  Über die Umgebungsvariabe wird ein User-Scheme (`the user scheme`_)
  aktiviert. Das User-Scheme liegt in den CDB-Tools. Während der Initialisierung
  eines Python Prozess passt es (u.a.) die Liste der Python-Pfade ``sys.path``
  als auch die Umgebung ``PATH`` an.

In der CDB-Tools Umgebung steht ein Paketmanager (:ref:`cdbtools_pckg`) bereit
mit dem Python Pakete in das User-Scheme installiert werden können.

  Über die Installation in das User-Scheme steht die komplette Welt der `PyPi`_
  Pakete von `PyPi`_ in CDB zur Verfügung, ohne das dazu etwas in die CDB
  Instanz installiert werden müsste.

Durch die Installation in bzw. durch die Bereitstellung von Werkzeugen aus den
CDB-Tools wird die CDB Instanz nachhaltig *schlank* gehalten.  In der CDB-Tools
Umgebung kann neben den `PyPi`_ Paketen zusätzliche Software bereit gestellt
werden.  So steht z.B. für Windows eine erweiterte Konsole (`ConEmu`_) zur
Verfügung mit der man wesentlich produktiver ist, als mit der *doch recht
störrischen* ``cmd.exe``.

Die CDB-Tools Umgebung kann über die Skripte

- ``cdbtools-activate`` aktiviert und mit
- ``cdbtools-deactivate`` deaktiviert werden.

I.d.R. wird man meist über ein Doppelklick auf eines der ``tools-<name>.bat``
Skripte in den ``winShortcuts`` eine CDB-Tools Umgebung starten. Für eine
CDB-Shell mit CDB-Tools Umgebung sieht das in etwa so aus:

.. code-block:: dosbatch

    ------------------------------------------------------------
    CDB-Tools environment
    ------------------------------------------------------------

     CADDOK_RUNTIME: C:\share\cdb_sw
     CADDOK_BASE:    C:\share\prod_copy
     CDBTOOLS_HOME:  C:\share\cdb-tools
     HOME:           C:\Users\user

    Using instance prod_copy@:C:\share\prod_copy
    Software in C:\share\cdb_sw
    Microsoft Windows [Version 6.3.9600]
    (c) 2013 Microsoft Corporation. Alle Rechte vorbehalten.

    [cdb_sw:prod_copy] C:\share\cdb-tools
    [CDBTools]$ ...


.. hint::

   Hier in der Anleitung wird der Prompt ``[CDB-Tools]`` genutzt, um anzuzeigen,
   wann ein Kommando **in einer CDB-Tools Umgebung ausgeführt werden muss**.
