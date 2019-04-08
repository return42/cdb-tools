.. -*- coding: utf-8; mode: rst -*-

.. include:: ../refs.txt

.. _cdbtools_eclipse:
.. _powerscript_studio:

============================
Eclipse & PowerScript Studio
============================

Das PowerScript Studio ist eine Eclipse_ Installation mit vorinstalliertem
Plugins wie PyDev_ und einem Dropin von Contact, in dem der Projekt-Wizzard für
CDB Installationen enthalten ist (siehe ``$CADDOK_BASE\eclipse\dropins``).
Alternativ zum PowerScript Studio kann auch eine aktuelle Eclipse Version mit
PyDev genutzt werden, in der das Dropin installiert wird, worauf aber hier nicht
weiter eingegangen werden soll.

.. hint::

   Eclipse ist für die Python Entwicklung nur bedingt geeignet.

Die Eclipse Versionen in CDB sind i.d.R. hoffnungslos veraltet, so wird mit CDB
15.3 das Eclipse Version 3.8 aus dem Jahre 2012 ausgeliefert.  Das PyDev Modul
liegt in der Version 4.3 aus dem Jahre 2015 vor und selbst das PowerScript
Dropin ist aus dem Jahre 2012.  Neuere Versionen von Eclipse & Co. können etwas
Linderung verschaffen, wer aber mal genau auf die PyDev Entwicklung schaut
`[ref] <https://www.brainwy.com/tracker/PyDev/>`_ wird merken, dass die
Workflows dort etwas an dem vorbei gehen, was man evtl. aus modernen
Entwicklungen kennt.

In gewachsenen Umgebungen mag es sein, dass Eclipse & Co. nur schwer zu ersetzen
sind.  Wer das aber nicht hat sollte sich gleich überlegen ob das mit dem
Eclipse in CDB überhaupt noch Sinn macht oder ob man nicht besser gleich auf
moderne Werkzeuge ausweicht, die i.d.R. dynamischer oder zumindest
leichtgewichtiger sind als Eclipse. *Fazit: für Python & Node.js Entwicklungen
gibt es passendere Werkzeuge.*

get started
===========

Das Basis-Setup des Eclipse wird beim ersten Start im HOME-Ordner abgelegt
(``.eclipse`` Ordner).  Ebenfalls beim ersten Start wird man gefragt, wo man
seinen Arbeitsbereich anlegen möchte.

.. figure:: eclipse/WorkspaceLauncher.png
   :scale: 50%

   Eclipse Workspace Launcher

.. tip::

   Will man seine Eclipse Settings komplett entfernen, so muss man den Ordner
   ``$HOME/.eclipse`` und den Ordner für den Arbeitsbereich
   (z.B. ``$HOME/workspace``) löschen.

In diesem Arbeitsbereich speichert Eclipse die Metadaten zu den Projekten, die
man in Eclipse einrichtet, da steht dann z.B. auch drin, wo man seinen
Arbeitsbereich angelegt hat.  Ist der Arbeitsbereich gesetzt, so startet Eclipse
und man kann sein PowerScript Studio Projekt anlegen (Kontextmenü im
Project-Explorer).

.. figure:: eclipse/cdb_instance.png
   :scale: 50%

   PowerScript Studio Projekt anlegen

.. tip::

   Neue Entwickler-Pakete leg man am einfachsten mit ``cdbpkg new`` an
   :ref:`[ref] <cdbpkg-new>`.


.. _powerscript_studio_pylint:

Pylint in PyDev einrichten
===========================

Das PyDev_ hat einen integrierten Code-Checker, wesentlich ausgereifter und
flexibler ist aber Pylint_, das sich inzwischen zum *Standard* etabliert hat
(s.a. :ref:`cdbtools-pylint`).  Die CDB-Tools bringen eine Pylint Installation
und ein Pylint Profil mit, das in Eclipse eingerichtet werden kann.  Dazu öffnet
man in Eclipse die Einstellungen unter :menuselection:`Window / Preferences`.

.. figure:: eclipse/PyDev_Pylint_prefs.png
   :scale: 50%

   PyDev Preferences (Pylint)

Unter :menuselection:`PyDev / Pylint` muss das Häkchen bei :guilabel:`Use
Pylint` gesetzt werden.  Als Launcher trägt man ``tools-pylint`` ein und unten
in den Argumenten wird noch ein Profil mitgeben, hier im Beispiel wird das
Profil aus den Vorlagen der CDB-Tools genutzt:

.. tip::

   Kopieren Sie die Vorlage in den Ordner der CDB-Instanz nach::

     $CADDOK_BASE\pylintrc

   und versionieren sie diese im Repository (s.a. :ref:`cdbtools-pylint`).  Die
   Option ``--rcfile`` in den Argumenten sollte dann wie folgt eingestellt
   werden::

     pylint --rcfile=%CADDOK_BASE%/pylintrc


Das reicht aber nicht, im jeweiligen PyDev Projekt muss man noch die Sourcen
einstellen, wenn man möchte, kann man unter den :guilabel:`External Libraries`
noch die Python Pfade aus den CDB-Tools eintragen (muss man aber nicht).


.. figure:: eclipse/PyDev-Project-Sources.png
   :scale: 50%

   PyDev Sourcen des Projekts


.. figure:: eclipse/PyDev-External-Sources.png
   :scale: 50%

   PyDev Sourcen des Projekts

Hat man alles eingestellt, so wird bei jedem Speichern einer geänderten Python
Datei nun ein Check mit dem Pylint durchgeführt.  Auf der linken Seite, sieht
man Symbole für die Meldungen aus dem Pylint-Lauf.  Rechts im Übersichtsbalken
sind entsprechend farblich hervorgehobene Bereiche.

.. figure:: eclipse/Pylint_example001.png
   :scale: 50%

   Pylint Meldungen in Eclipse.

