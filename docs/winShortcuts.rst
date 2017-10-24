.. -*- coding: utf-8; mode: rst -*-

.. _pdb: https://docs.python.org/3/library/pdb.html#debugger-commands
.. _`PyDev Remote Debugger`: http://www.pydev.org/manual_adv_remote_debugger.html   
.. _shortcuts:

============
winShortcuts
============

In dem Ordner ``winShortcuts`` stehen Skripte und Links bereit, die i.d.R. mit
einem Doppelklick geöffnet werden können. Die Idee dieses Ordner ist es, dem
CDB-Entwickler bzw. Administrator für seine Arbeit die wichtigsten Umgebungen,
Tools oder aber auch Links auf einfache Weise an einem Ort bereit zu stellen.
Zu unterscheiden sind die Prozesse in ihrer Laufzeitumgebung, die entweder eine
:ref:`gewöhnliche CDB Umgebung <cdb_shortcuts>` ist oder eine :ref:`erweiterte
CDB-Tools Umgebung <cdbtools_shortcuts>` ist.


cdbEnv
======

In dieser Datei werden die Umgebungsvariablen eingestellt, die erforderlich sind
um die CDB-Tools mit der CDB Instanz zusammenzubringen. Die Beschreibung hierzu
findet sich in der Installationsanleitung im Kapitel :ref:`setup_cdbenv`.


.. _cdb_shortcuts:
  
gewöhnliche CDB Umgebung
========================

Die *normalen* CDB Prozesse laufen in der *normalen* Laufzeitumgebung von CDB,
sie sollen keinen Zugriff auf die Erweiterungen aus den CDB-Tools haben. so
gesehen sind die in diesem Abschnitt gelisteten *Shortcuts* ganz normale CDB
Anwendungen.

- ``cdbPC.bat``:

  Startet einen gewöhnlichen CDB-Client, mit Anmeldedialog.

- ``cdbSHELL.bat``:

  Startet eine gewöhnliche ``cdbsh``. Zu erkennen auch an dem Prompt
  ``[cdb:prod_copy]`` (oder ähnlich) und nicht zu verwechseln mit einer
  ``[CDB-Tools]`` Umgebung.

  .. hint::

     Hier in der Anleitung wird der Prompt ``[cdb:prod_copy]`` genutzt, um
     anzuzeigen, wann ein Kommando **in einer cdb-Shell** ausgeführt werden
     muss.

- ``cdbStudio.bat``:

  Startet das CDB Powerscript Studio (aka. eclipse)

- ``CDBSVCD-START.bat``:

  Startet den *lokalen* CDB Server und die für *diesen* Host konfigurierten
  Dienste. Eignet sich für Entwickler Instanzen, bei denen man den Application
  Server nicht in den Diensten des Betriebssystems einrichten möchte. Der
  CDB-Server läuft in einer gewöhnlichen CDB Umgebung.


.. _cdblinks_shortcuts:

WEB-Links
=========

Die CDB-Links verweisen auf Seiten eines CDB Servers, wie er z.B. mittels
``CDBSVCD-START.bat`` gestartet werden kann (alles *localhost*).

- ``cdbPortal-localhost.url``:   http://localhost:81/
- ``cdbDoc-localhost.url``:      http://localhost:81/doc
- ``cdbServices-localhost.url``: http://localhost:55550/services


.. _cdbtools_shortcuts:

erweiterete CDB-Tools Umgebung
==============================

- ``cdbtools.bat``: 

  Startet eine ``cdbsh`` mit der erweiterten Laufzeitumgebung der CDB-Tools. Zu
  erkennen auch an dem Prompt ``[CDB-Tools]`` und nicht zu verwechseln mit einer
  gewöhnlichen CDB Umgebung (``[cdb:prod_copy]`` oder ähnlich).

  .. hint::

     Hier in der Anleitung wird der Prompt ``[CDB-Tools]`` weiter genutzt, um
     anzuzeigen, wann ein Kommando **in einer CDB-Tools Umgebung** ausgeführt
     werden muss (s.a. :ref:`cdbtools_env`).

- ``CDBSVCD-START-debug.bat``:

  Eignet sich für remote Debug-Zwecke in einer Entwickler Installation (eine
  einfache Alternative zum `PyDev Remote Debugger`_).

  Es wird der *lokale* CDB Server und die für *diesen* Host konfigurierten
  Dienste gestartet. Gleichzeitig startet in der Konsole ein *Listener*, der auf
  Breakpoints lauscht. Einen Breakpoint setzt man wie folgt:

  .. code-block:: python

     from dm.cdbtools import BP
     BP()

  Wird der Breakpoint erreicht, so öffnet der Listener eine Py-Debugger Sitzung
  (siehe pdb_).  Setzt man einen neuen Breakpoint in den Sourcen, so muss nicht
  immer der ``CDBSVCD`` Prozess neu gestartet werden. So reicht es
  beispielsweise aus, den PC-Client neu zu starten, wenn man lediglich die
  Sourcen eines ``cdbsrv`` Prozess debuggen will (klassische UserExit
  Programmierung wie im PowerScript Studio).

  Vorteil des remote Debugging ist, dass man hiermit jeden Server-Prozess
  debuggen kann und das auch alle Dienste laufen. Im Powerscript-Studio läuft
  normalerweise nur der cdbsrv Prozess im Debug Modus und man vermisst
  evtl. Services die beispielsweise die eLink Anwendungen bereit stellen.

  Die Kommunikation zwischen dem Debugger-Client und dem Breakpoint erfolgt über
  IP sockets, weshalb man das auch remote Debugging nennen kann. Prinzipell ist
  es auch möglich Server Prozesse auf entfernten Hosts zu debuggen, jedoch
  sollte man in einer verteilten Umgebung darauf achten, dass die Breakpoints
  nicht von anderen Benutzern oder Prozessen erreicht werden (können). In der
  Regel wird man diese Art des Debugging nur in *lokalen* Entwickler Umgebungen
  nutzen. Dort kann es dann aber auch eine große Hilfe sein, wo man bisher nur
  die Möglichkeit hatte Logfiles zu lesen.
