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
  Über die Umgebungsvariable wird ein User-Scheme (`the user scheme`_)
  aktiviert.  Das User-Scheme liegt in den CDB-Tools.  Während der
  Initialisierung eines Python Prozess passt es (u.a.) die Liste der
  Python-Pfade ``sys.path`` als auch die Umgebung ``PATH`` an.

In der CDB-Tools Umgebung steht ein Paketmanager bereit mit dem Python Pakete in
das User-Scheme installiert werden (siehe ":ref:`cdbtools_pip`").  Durch die
Installation *in* bzw. durch die Bereitstellung von Werkzeugen *aus* den
CDB-Tools wird die CDB-Instanz selbst nachhaltig *schlank* gehalten.

In der CDB-Tools Umgebung kann neben den `PyPi`_ Paketen auch zusätzliche
Software bereit gestellt werden (:ref:`cdbtools_software`).

Die CDB-Tools Umgebung kann in einer Shell über die Skripte

- ``cdbtools-activate``   aktiviert und mit
- ``cdbtools-deactivate`` deaktiviert werden.

I.d.R. wird man unter Windows meist über ein Doppelklick auf eine der ``.bat``
Dateien in den :ref:`winShortcuts` die Umgebung starten.  Für eine Shell mit
CDB-Tools Umgebung sieht das in etwa so aus (:ref:`tools_sh_bat`):

.. code-block:: dosbatch

   ------------------------------------------------------------
   CDB-Tools environment
   ------------------------------------------------------------

     CADDOK_RUNTIME: C:\share\contact\cdbsrv-11.3.10
     CADDOK_BASE:    C:\share\cdb_cust_dev
     CADDOK_DEFAULT: cust_dev@C:\share\cdb_cust_dev
     HOME:           C:\Users\user
   ...

   C:\share\cdb_cust_dev
   [CDBTools]$


.. _rte_prompt:

Konsolen Prompt der Umgebungen
==============================

``[CDBTools]``
  Hier in der Anleitung wird der Prompt ``[CDBTools]`` genutzt, um anzuzeigen,
  das ein Kommando **in einer CDB-Tools Umgebung ausgeführt werden muss**.

``[cdbsrv-11.3.10:cust_dev]``
   Hier in der Anleitung wird der Prompt ``[cdb:prod_copy]`` genutzt, um
   anzuzeigen, das ein Kommando **in einer Standard CDB-Installation ageführt
   werden muss**.

.. _setup_cdbenv:

Setup cdbEnv
============

Damit die CDB-Tools und die CDB Installation *zueinander finden* müssen in der
Datei ``winShortcuts/cdbEnv.bat`` folgende Umgebungen angepasst werden.

.. code-block:: dosbatch

   SET "CADDOK_BASE=C:\share\cdb_cust_dev"
   SET "CADDOK_DBNAME=cust_dev"

   SET "CADDOK_RUNTIME=C:\share\contact\cdbsrv-11.3.10"
   SET "CADDOK_CLIENT_HOME=C:\share\contact\cdbpc-11.3.0.10"

Nachdem die Umgebung korrekt gesetzt wurde, ist es möglich mit
``winShortcuts/cdb-sh.bat`` eine CDB-Shell zu starten:

.. code-block:: dosbatch

  $ C:\share\cdb-tools\winShortcuts\cdb-sh.bat
  ...
  [cdbsrv-11.3.10:cust_dev] C:\share\cdb_cust_dev> ...

Den Prompt ``[cdbsrv-11.3.10:cust_dev]`` setzt die CDB-Shell, er wird in der
*eigenen* Instanz vermutlich etwas anders aussehen (s.a. :ref:`rte_prompt`).  Um
zu überprüfen ob die Umgebung korrekt gesetzt ist sollte man sich die
``CADDOK_*`` Variablen anschauen:

.. code-block:: dosbatch

  [cdbsrv-11.3.10:cust_dev] C:\> SET CADDOK
  ...
  CADDOK_RUNTIME=C:\share\contact\cdbsrv-11.3.10
  CADDOK_BASE=C:\share\cdb_cust_dev
  CADDOK_DEFAULT=cust_dev@C:\share\cdb_cust_dev
  ...

Stimmen nicht alle Einstellungen, so muss man ggf. noch die ``etc/site.conf``
oder eine der anderen ``etc/*.conf`` Dateien anpassen (normale CDB
Konfiguration).


.. _cdbtools_portable:

Portable
========

.. _`portable Software`: https://de.wikipedia.org/wiki/Portable_Software

Die einfachste Form Software zu installieren ist, sie nicht zu installieren /
einfach nur den ZIP-Ordner mit den CDB-Tools auspacken.  In diesem Sinne sind
die CDB-Tools `portable Software`_.  Da jedoch nicht alle Module der CDB-Tools
(insbesondere Python Pakete) *per se* in diesem Sinne *portabel* sind, muss nach
dem *Verschieben* der CDB-Tools an einen anderen Ort einmal das Skript:

.. code-block:: dosbatch

   [CDBTools]$ cdbtools-fix-launcher

in einer CDB-Tools Shell ausgeführt werden.

.. hint::

   Wir haben z.T. Probleme mit CDB festgestellt, wenn unter Windows die
   CDB-Tools in einen anderen Laufwerksbuchstaben als CDB installiert werden.
   Am besten liegen CDB-Instanz, CDB-Software und die CDB-Tools auf dem gleichen
   Laufwerksbuchstaben.
