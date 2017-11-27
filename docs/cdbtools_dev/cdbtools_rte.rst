.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_rte:

================
Laufzeitumgebung
================

Zur Erweiterung der Laufzeitumgebung von CDB Prozessen nutzen die CDB-Tools die
Umgebungsvariablen:

``PATH``
  In den Shell-Umgebungen werden zusätzliche Kommandos zur Verfügung gestellt.

``PYTHONUSERBASE``
  Über die Umgebungsvariabe wird ein User-Scheme (`the user scheme`_)
  aktiviert. Das User-Scheme liegt in den CDB-Tools. Während der Initialisierung
  eines Python Prozess passt es (u.a.) die Liste der Python-Pfade ``sys.path``
  als auch die Umgebung ``PATH`` an.

In der CDB-Tools Umgebung steht ein Paketmanager bereit mit dem Python Pakete in
das User-Scheme installiert werden (:ref:`cdbtools_pckg`).  Durch die
Installation *in* bzw. durch die Bereitstellung von Werkzeugen *aus* den
CDB-Tools wird die CDB Instanz nachhaltig *schlank* gehalten.  In der CDB-Tools
Umgebung kann neben den `PyPi`_ Paketen zusätzliche Software bereit gestellt
werden.  So steht z.B. eine erweiterte Konsole (:ref:`cdbtools_console`) zur
Verfügung mit der man wesentlich produktiver ist, als mit den herkömmlichen
Konsolen.

Die CDB-Tools Umgebung kann in einer Shell über die Skripte

- ``cdbtools-activate``   aktiviert und mit
- ``cdbtools-deactivate`` deaktiviert werden.

I.d.R. wird man unter Windows meist über ein Doppelklick auf eines der ``.bat``
Skripte in den :ref:`winShortcuts` die Umgebung starten.  Für eine CDB-Shell mit
CDB-Tools Umgebung sieht das in etwa so aus:

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


.. _rte_prompt:

Konsolen Prompt der Umgebungen
==============================

``[CDBTools]``
  Hier in der Anleitung wird der Prompt ``[CDBTools]`` genutzt, um anzuzeigen,
  wann ein Kommando **in einer CDB-Tools Umgebung ausgeführt werden muss**.

``[cdb:prod_copy]``
   Hier in der Anleitung wird der Prompt ``[cdb:prod_copy]`` genutzt, um
   anzuzeigen, das ein Kommando **in einer cdb-Shell ausgeführt werden muss**.

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


.. _cdbtools_portable:

Portable
========

Die einfachste Form Software zu installieren ist, sie nicht zu installieren /
einfach nur den ZIP-Ordner mit den CDB-Tools auspacken. In diesem Sinne sind die
CDB-Tools `portable Software <https://de.wikipedia.org/wiki/Portable_Software>`_.

Da jedoch nicht alle Module der CDB-Tools (insbesondere Python Pakete) *per se*
in diesem Sinne *portabel* sind, muss nach dem *Verschieben* der CDB-Tools an
einen anderen Ort einmal das Skript:

.. code-block:: dosbatch

   [CDBTools]$ cdbtools-fix-launcher

in einer CDB-Tools Shell ausgeführt werden.

.. hint::

   Wir haben z.T. Probleme mit CDB festgestellt, wenn unter Windows die
   CDB-Toools in einen anderen Laufwerksbuchstaben als CDB installiert werden.
   Am besten liegen CDB-Instanz, CDB-Software und die CDB-Tools auf dem gleichen
   Laufwerksbuchstaben.
