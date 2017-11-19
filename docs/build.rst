.. -*- coding: utf-8; mode: rst -*-

.. include:: refs.txt

.. _cdbtools-build:

=================
Bootstrap & Build
=================

Bevor die CDB-Tools genutzt werden können müssen die externen Abhängigkeiten aus
dem Internet geladen werden (im ``cdb-tools.zip`` initial enthalten). Die
Installation (der Build) besteht aus den unten beschriebenen Schritten.  Da in
*restricted areas* nicht immer ein Zugang zum Internet zur Verfügung steht,
wurde der *Build* in eine *online* und eine *offline* Phase aufgeteilt.

Die Schritte können mit einem Doppelklick auf ``winShortcuts\upkeep.bat``
durchgeführt werden.

**online**

Für die beiden ersten Schritte ist ein online Zugangang zum Internet und ein
Python 2.7.9 erforderlich. Das Python 2.7.9 wird aus der CDB-Instanz bezogen,
sofern diese zur Verfügung steht.

- bootstrap

  Der *bootstrap* ist initial einmal erforderlich. Er installiert eine
  minimal erforderliche Umgebung.

- download

  Beim Download werden alle Python-Pakete und Tools aus dem Internet geladen und
  in dem ``dist`` Ordner abgelegt.

**offline**

Für die nun folgenden Schritte ist eine CDB Instanz erforderlich. Ein online
Zugangang zum Internet ist nicht mehr erforderlich.

- install

  Für die Installation ist kein online Zugang mehr erforderlich. Die
  Installation erfolgt aus dem ``dist`` Ordner.

- update launcher

  Die Python Pakete installieren sich z.T. mit absoluten Pfadnamen. Damit die
  CDB-Tools *portable* sind müssen die absoluten Pfadnamen in relative
  *umgebogen* werden.

- ZIP CDB-Tools

  In diesem letzten Schritt wird aus den CDB-Tools ein ``cdb-tools.zip``
  gebaut. Dieser Schritt ist nur erforderlich, wenn Sie sich eine aktuelle
  Version der CDB-Tools als ZIP bereit stellen möchten.
