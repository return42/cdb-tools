.. -*- coding: utf-8; mode: rst -*-

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
