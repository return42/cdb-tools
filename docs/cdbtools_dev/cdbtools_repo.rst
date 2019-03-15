.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_repo:

=========================
Build aus dem Reposetorie
=========================

Die Entwicklung der CDB-Tools findet in dem Reposetorie `cdb-tools@github
<https://github.com/return42/cdb-tools>`_ statt.  Will man die CDB-Tools selber
bauen oder ein Update durchführen so muss man zunächst über einen Klon dieses
Reposetories verfügen (``cdb-tools.zip`` in den `Releases`_ ist bereits ein
git-Clone).

.. _clone_cdbtools:

git-clone
=========

Das Repository der CDB-Tools wird mit ``git clone`` *geklont*.::

  $ git clone --recursive https://github.com/return42/cdb-tools

Wichtig ist der Schalter ``--recursive`` der sicherstellt, dass auch die
Submodule der CDB-Tools *geklont* werden.  Es kann aber auch später nachgeholt
werden::

  $ git submodule init
  $ git submodule update

Als nächstes müssen die ``CADDOK_*`` Variablen angepasst werden
(:ref:`install_cdbtools`).

Der Build besteht aus den unten beschriebenen Schritten.  Da in *restricted
areas* nicht immer ein Zugang zum Internet zur Verfügung steht, wurde der
*Build* in eine *online* und eine *offline* Phase aufgeteilt.


.. _cdbtools_bootstrap:

Bootstrap & Download (online)
=============================

Bevor die CDB-Tools genutzt werden können müssen zunächst die externen
Abhängigkeiten aus dem Internet geladen werden (im ``cdb-tools.zip`` initial
enthalten).

.. tip::

   Die Schritte können komfortabel mit einem Doppelklick auf :ref:`upkeep_bat`
   durchgeführt werden.

Für die beiden ersten Schritte (Bootstrap & Download) ist ein online Zugang zum
Internet und ein Python 2.7.9 erforderlich.  Sofern eine CDB-Instanz zur
Verfügung steht wird der Python Interpreter aus der CDB-Instanz bezogen
(ansonsten muss man ein Python 2.7.9 auf dem *online* Host installieren).

bootstrap
  Der *bootstrap* ist initial einmal erforderlich.  Er installiert eine minimal
  erforderliche Umgebung mit der die weiteren Schritte wie 'download' oder
  'install' erst möglich sind.

download
  Beim Download werden alle Python-Pakete und *Tools* aus dem Internet geladen
  und in dem ``dist`` Ordner abgelegt.  Die Tools wie :ref:`cdbtools_ConEmu`
  werden dabei aus dem Download bereich der CDB-Tools bezogen.

  - Quelle der Python Pakete: PyPi_ (:origin:`bootstrap/requirements.txt`)
  - Quelle der *Tools*: https://github.com/return42/cdb-tools/releases/


.. _cdbtools_build:

Build der CDB-Tools (offline)
=============================

Für die folgenden Schritte ist eine CDB Instanz erforderlich. Ein online Zugang
zum Internet ist nicht mehr erforderlich, da die erforderlichen Pakete bereits
aus dem Internet geladen wurden.

install
  Für die Installation ist kein online Zugang mehr erforderlich. Die
  Installation erfolgt aus dem ``dist`` Ordner.

update launcher
  Die Python Pakete installieren sich z.T. mit absoluten Pfadnamen. Damit die
  CDB-Tools *portable* sind müssen die absoluten Pfadnamen in relative
  *umgebogen* werden.

ZIP CDB-Tools
  In diesem letzten Schritt wird aus den CDB-Tools ein ``cdb-tools.zip`` gebaut.
  Dieser Schritt ist nur erforderlich, wenn Sie sich eine aktuelle Version der
  CDB-Tools als ZIP bereit stellen möchten (ein eigenes Release).

.. _update_cdbtools:

Update
======

Die Aktualisierung der CDB-Tools erfolgt über das Reposetorie.  Für das Update
muss ``git`` und ein online Zugang zur Verfügung stehen::

   $ git pull
   $ git submodule update --recursive

Die CDB-Tools müssen dann neu gebaut werden:

- :ref:`cdbtools_bootstrap`
- :ref:`cdbtools_build`

