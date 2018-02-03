.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _release_management:

======================================
Releasemanagement und CONTACT Elements
======================================

Eine Voraussetzung einer soliden Projekt-planung/durchführung ist ein *sauberes*
Releasemanagement, das soweit als möglich parallele Entwicklungen an (Teil-)
Projekten erlaubt. Softwareentwicklung ist immer eine Team Leistung bei der die
Team-Mitglieder ihre Änderungs-Beiträge aus den Teil-Projekten in eine
Infrastruktur einbringen. Diese Änderungs-Beiträge durchwandern i.d.R. noch
(Anwender-) Tests und Bugfixing bevor sie in den *Rollout* gehen.

Das Releasemanagement ist nicht willkürlich, es wird bestimmt durch die
Verfahren, mit denen eine Änderung durch eine Infrastruktur transportiert werden
kann. Bei CONTACT Elements basiert der Transport von Änderungen auf der
Komponentenarchitektur und die kennt eine Teilung **nur entlang der
Pakete**. Damit ist gemeint, dass ein Transport immer alle Änderungen eines
**ganzen Pakets** umfasst. Bei typischen Kunden-Entwicklungen werden also immer
alle Änderungen in dem Kundenpaket (z.B. ``cust.pdm``) transportiert.

Aus Sicht der Weiterentwicklung von Kundenanpassungen (``cust.pdm``) wird hier
schon die erste Einschränkung deutlich: Im Grunde können Kundenanpassungen in
einem Paket nur *nacheinander* entwickelt, getestet und ausgerollt werden. In
der Praxis ist das Verfahren jedoch kaum aufrecht zu erhalten, es müssen immer
HOTFIXes angebracht und Änderungen parallel entwickelt werden.

Die hier vorgestellten Verfahren zum Releasemanagement basieren auf einem
allgemein als **Feature Branch** bekanntem Workflow. Dieser wird auch im CDB
Handbuch zur Komponentenarchitektur vorgestellt. Während die Beschreibung dort
von *idealen* Bedingungen der *CONTACT Elements* Infrastruktur ausgeht sind die
hier vorgestellten Verfahren robuster (da der Scope des Reposetory größer ist)
und hoffentlich auch praxisgerechter (weil auch Nutzdaten im Spiegel System
sind).

Big Picture
===========

.. _xref-figure-release_management-big_picture:
        
.. figure:: release_management/big_picture.svg
   :alt:     Figure (big_picture.svg)
