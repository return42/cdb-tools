.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cheat-sheet:

===========
Cheat Sheet
===========

.. _cdbpkg-new:

CDB Paket erstellen
===================

::

   cdbpkg new cust.plm

Das Kommando legt ein (Entwickler) Paket im Instanzordner an.  Die Setup-Tools
von Python legen dabei z.T. mehr an, als man benötigt.  So gibt es auf Windows
z.B. eine ``site-packages/cust.plm-nspkg.pth``, die kann gelöscht werden.
Wichtig ist die ``cust.plm.egg-link`` Datei, darin ist eigentlich nicht mehr als
nur ein Verweis auf das Paket.::

  C:\share\cdb_cust_dev\cust.plm

Den Inhalt sollte man ändern und den Pfad relativ einsetzen, da wir in der
CDB-Instanz sind ist der relative Pfad immer gleich.::

  ../cust.plm

Die Verwendung von Slash (``../``) gewährleistet, dass der Pfad auf allen
Plattformen und nicht nur auf MS-Windows funktioniert.
