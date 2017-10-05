.. -*- coding: utf-8; mode: rst -*-

.. _install_cdbtools:

============
Installation
============

Laufzeitumgebungen
==================

Die CDB-Tools sind *non invasiv*, d.h. sie werden nicht in CDB installiert.  Die
Idee der CDB-Tools ist es, eine erweiterte Laufzeitumgebung bereit zu stellen in
der Wartungs- und Diagnose- Werkzeuge in CDB ausgeführt werden können, ohne das
dazu die CDB Installation *verändert* werden müsste.

Zur Erweiterung der Laufzeitumgebungen von CDB Prozessen nutzen die CDB-Tools
die Umgebungsvariablen ``PATH`` und ``PYTHONPATH`` und in Python Prozessen wird
die Liste der Python-Pfade ``sys.path`` angepasst.

Das Paketmanagement der CDB-Tools (:ref:`cdbtools_pckg`) ist unabhängig von CDB.
Auf diese Weise müssen Werkzeuge für die Wartung und Diagnose nicht mehr in CDB
installiert werden, was die CDB Instanz zusätzlich *schlank* hält.


Download (git clone)
====================

Anstatt eines klassischen Downloads sollten die CDB-Tools mit ``git clone``
*gedownloaded* werden, so kann man später mittels ``git pull`` die CDB-Tools
auch einfach *updaten*.::

  $ git clone --recursive https://github.com/return42/cdb-tools

Wichtig ist der Schalter ``--recursive`` der sicherstellt, dass auch die
Submodule der CDB-Tools *geklont* werden.


.. _setup_cdbenv:

Setup cdbEnv
============

Damit die CDB-Tools und die CDB Installation *zueinander finden* müssen in der
Datei ``winShortcuts/cdbEnv.bat`` folgende Umgebungen angepasst werden.

.. code-block:: dosbatch

   SET CADDOK_DBNAME=prod_copy
   SET CADDOK_RUNTIME=C:\share\cdb_sw
   SET CADDOK_BASE=C:\share\customer\instance_prod_copy
   ...
   SET CDBTOOLS_HOME=C:\share\cdb-tools

Der letzte Wert ``CDBTOOLS_HOME`` muss nur gesetzt werden, wenn man sich den
winShortcuts Ordner an eine andere Stelle (z.B. in die CDB-Instanz) kopiert hat.
Verbleibt der Ordner unterhalb ``./cdb-tools`` passt der Wert, der da schon
automatisch ermittelt wird.

Nachdem die Umgebung richtig gesetzt ist, müsste es möglich sein durch einen
Doppelklick auf ``winShortcuts/cdbSHELL.bat`` eine CDB-Shell zu starten:

.. code-block:: dosbatch

  C:\> C:\share\cdb-tools\winShortcuts\cdbSHELL.bat
  ...
  [cdb:prod_copy] C:\> echo Die CDB-Tools liegen hier: %CDBTOOLS_HOME%
  Die CDB-Tools liegen hier: C:\share\cdb-tools
  [cdb:prod_copy] C:\>

Der Prompt ``[cdb:prod_copy]`` ist der Prompt, den die cdb-Shell setzt, er wird
in der eigenen Instanz vermutlich etwas anders aussehen.

.. hint::

   Hier in der Anleitung wird der Prompt ``[cdb:prod_copy]`` genutzt, um
   anzuzeigen, wann ein Kommando **in einer cdb-Shell** ausgeführt werden muss.


.. _bootstrap_cdbtools:

bootstrap
=========

Bevor die CDB-Tools genutzt werden können müssen ihre externen Abhängigkeiten
einmal installiert werden.:

.. code-block:: dosbatch

  [cdb:prod_copy] C:\> cdb-tools\bootstrap\install.bat

Mit diesem Kommando wird das ``pip`` Paketmanagement für die CDB-Tools
eingerichtet und es werden die externen Abhängigkeiten (Python Pakete) in den
Ordner ``cdb-tools/py27`` installiert. Die Kommandos aus diesen Paketen stehen
danach in einer :ref:`CDB-Tools Umgebung <cdbtools_env>` bereit.

.. hint::

   Für den Download/Update der externen Abgängigkeiten (Python Pakete) ist ein
   online Zugangang erforderlich. In *restricted areas* ist das nicht immer
   gegeben, weshalb dieser Vorgang auch auf einem Host durchgeführt werden kann
   der online ist. Anschließend muss nur der ganze cdb-tools Ordner auf den
   *offline* Host kopiert werden.


.. _cdbtools_env:

CDB-Tools Umgebung
==================

Die CDB-Tools Umgebung wird über das Skript ``winShortcuts/cdbtools.bat`` bereit
gestellt. I.d.R. wird man durch einen Doppelklick darauf eine Shell öffnen, man
kann das Skript aber auch in einer Kommandozeile aufrufen.

.. code-block:: dosbatch

   C:\> cdb-tools\winShortcuts\cdbtools.bat

   Executing Script: C:\share\cdb_sw\cdb\etc\std.conf
   Executing Script: C:\share\instance\etc\site.conf
   Using instance prod_copy@:C:\share\instance
   Software in C:\share\cdb_sw
   ------------------------------------------------------------
   CDB-Tools environment
   ------------------------------------------------------------

   CDBTOOLS_HOME: c:\share\yyy\cdb-tools
   HOME:          C:\Users\user

   [CDB-Tools] C:\
   $ ...

.. hint::

   Hier in der Anleitung wird der Prompt ``[CDB-Tools]`` weiter genutzt, um
   anzuzeigen, wann ein Kommando **in einer CDB-Tools Umgebung** ausgeführt
   werden muss.

.. _cdbtools_pckg:

Paketmanagement der CDB-Tools
=============================

Die CDB-Tools bringen ihr eigenes Paket-Managment (pip + setuptools) mit, dass
wenige bis keine Abhängigkeiten zu CDB hat, also unabhängig von CDB genutzt
werden kann (in CDB 10 gibt es beispielsweise kein pip).

Die Python Pakete werden in dem Ordner::

  %CDBTOOLS_HOME%\py27

angelegt, dort werden auch die Launcher im Ordner ``py27/Scripts`` eingerichtet
und von den CDB-Tools so angepasst, dass sie in der CDB-Tools Umgebung laufen.
In der Datei::

  bootstrap/requirements.txt

sind die zu installierenden (s. :ref:`bootstrap_cdbtools`) Pakete aufgelistet.
Um die CDB-Software *unberührt* zu lassen müssen Installationen in die CDB-Tools
Umgebung mit pip immer über folgende Schalter verfügen::


  pip install --ignore-installed \
              --install-option="--prefix=%CDBTOOLS_HOME%\py27" 

.. hint::

   Bei unsachgemäßer Installation von Paketen mit pip kann die CDB-Software
   u.U. beschädigt werden, deshalb immer erst mal in einem *unkritischen* System
   testen!

   Setzt man den Schalter ``--ignore-installed`` nicht, dann besteht immer die
   Gefahr, dass das pip versucht ein Paket aus der CDB-Software zu
   deinstallieren und durch ein neueres unter ``--prefix=%CDBTOOLS_HOME%\py27``
   zu ersetzen. Damit wäre die CDB-Software manipuliert und nicht mehr
   lauffähig.

   
