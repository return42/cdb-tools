.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_repo:

=========================
Build aus dem Reposetorie
=========================

Die Entwicklung der CDB-Tools findet in dem Reposetorie `cdb-tools@github
<https://github.com/return42/cdb-tools>`_ statt. Will man die CDB-Tools selber
bauen oder ein Update durchführen so muss man zunächst über einen Klon dieses
Reposetories verfügen.

.. _clone_cdbtools:

git-clone
=========

Das Reposetorie der CDB-Tools wird mit ``git clone`` *geklont*.::

  $ git clone --recursive https://github.com/return42/cdb-tools

Wichtig ist der Schalter ``--recursive`` der sicherstellt, dass auch die
Submodule der CDB-Tools *geklont* werden.  Spätere Aktualisierungen können
mittels ``git pull`` erfolgen (:ref:`update_cdbtools`).  Die nächsten Schritte
sind im Abschnitt :ref:`cdbtools_build` beschrieben.

.. hint::

   In dem ZIP ``cdb-tools.zip`` ist das Reposetorie bereits enthalten / kein
   git-clone mehr erforderlich.


.. _cdbtools_build:

Bootstrap & Build
=================

Bevor die CDB-Tools genutzt werden können müssen zunächst die externen
Abhängigkeiten aus dem Internet geladen werden (im ``cdb-tools.zip`` initial
enthalten). Der Build besteht aus den unten beschriebenen Schritten.  Da in
*restricted areas* nicht immer ein Zugang zum Internet zur Verfügung steht,
wurde der *Build* in eine *online* und eine *offline* Phase aufgeteilt.

.. tip::

   Die Schritte können komfortabel mit einem Doppelklick auf :ref:`upkeep_bat`
   durchgeführt werden.

**online**

Für die beiden ersten Schritte ist ein online Zugangang zum Internet und ein
Python 2.7.9 erforderlich. Sofern eine CDB-Instanz zur Verfügung steht wird der
Python Interpreter aus der CDB-Instanz bezogen (ansonsten muss man ein Python
2.7.9 auf dem *online* Host installieren).

1. bootstrap

  Der *bootstrap* ist initial einmal erforderlich. Er installiert eine minimal
  erforderliche Umgebung mit der die weiteren Schritte wie 'download' oder
  'install' erst möglich sind.

2. download

  Beim Download werden alle Python-Pakete und *Tools* aus dem Internet geladen
  und in dem ``dist`` Ordner abgelegt. Die Tools wie :ref:`cdbtools_ConEmu`
  werden dabei aus dem Download bereich der CDB-Tools bezogen.

  - Quelle der Python Pakete: PyPi_ (`requirements.txt`_)
  - Quelle der *Tools*: https://github.com/return42/cdb-tools/releases/

**offline**

Für die folgenden Schritte ist eine CDB Instanz erforderlich. Ein online
Zugangang zum Internet ist nicht mehr erforderlich.

3. install

  Für die Installation ist kein online Zugang mehr erforderlich. Die
  Installation erfolgt aus dem ``dist`` Ordner.

4. update launcher

  Die Python Pakete installieren sich z.T. mit absoluten Pfadnamen. Damit die
  CDB-Tools *portable* sind müssen die absoluten Pfadnamen in relative
  *umgebogen* werden.

5. ZIP CDB-Tools

  In diesem letzten Schritt wird aus den CDB-Tools ein ``cdb-tools.zip``
  gebaut. Dieser Schritt ist nur erforderlich, wenn Sie sich eine aktuelle
  Version der CDB-Tools als ZIP bereit stellen möchten.

.. _update_cdbtools:

Update
======

Die Aktualisierung der CDB-Tools erfolgt über das Reposetorie. Für das Update
muss ``git`` und ein online Zugang zur Verfügung stehen::

   $ git pull
   $ git submodule update --recursive

Das Update, respektive der neue Build erfolgt dann durch die in
:ref:`cdbtools_build` beschriebenen Schritte (z.B. mit :ref:`upkeep_bat`):

2. download (nur online möglich)
3. install
4. update launcher
