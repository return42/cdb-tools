.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _release_management:

======================================
Releasemanagement und CONTACT Elements
======================================

Eine der wichtigen Voraussetzungen zur soliden Projektdurchführung ist ein
*sauberes* Releasemanagement, das -- soweit als möglich -- parallele
Weiterentwicklung an (Teil-) Projekten erlaubt. Softwareentwicklung ist immer
eine Team Leistung bei der die Team-Mitglieder ihre Änderungs-Beiträge aus den
Teil-Projekten in eine Infrastruktur einbringen. Diese Änderungs-Beiträge
durchwandern i.d.R. noch (Anwender-) Tests und Bugfixing bevor sie
schlussendlich in den *Rollout* gehen.

Das Releasemanagement ist nicht willkürlich, es wird bestimmt durch die
Verfahren, mit denen eine Änderung durch eine Infrastruktur transportiert werden
kann. Bei CONTACT Elements basiert der Transport von Änderungen auf der
Komponentenarchitektur (s. a. Foliensammlung `CDB Komponenten & Entwicklung
<slides/cdb_comp/index.html>`_) und die kennt eine Teilung **nur entlang der
Pakete**. Damit ist gemeint, dass ein Transport immer alle Änderungen eines
**ganzen Pakets** umfasst. Bei typischen Kunden-Entwicklungen werden also immer
alle Änderungen in dem Kundenpaket (z.B. ``cust.pdm``) transportiert.

.. admonition:: Der Scope einer Änderung umfasst immer das ganze Paket.
   :class: tip

   Ein (Kunden-) Paket kann immer nur als ganze Einheit transportiert werden. Es
   ist nicht möglich zwei unterschiedliche Entwicklungen an einem Paket
   gleichzeitig aber doch für sich getrennt durch ein System (z.B. QS) zu
   transportieren.

Aus Sicht der Weiterentwicklung von Kundenanpassungen (``cust.pdm``) wird hier
schon die erste Einschränkung deutlich: Im Grunde können Kundenanpassungen in
einem Paket nur *nacheinander* entwickelt, getestet und ausgerollt werden. In
der Praxis ist das Verfahren jedoch kaum aufrecht zu erhalten, es müssen immer
HOTFIXes angebracht und Änderungen parallel entwickelt werden können.

Die hier vorgestellten Verfahren zum Releasemanagement basieren auf einem
allgemein als **Feature Branch** bekanntem Workflow. Dieser wird auch im CDB
Handbuch zur Komponentenarchitektur vorgestellt. Während die Beschreibung dort
von *idealen* Bedingungen der *CONTACT Elements* Infrastruktur ausgeht sind die
hier vorgestellten Verfahren robuster (da der Scope des Reposetory größer ist)
und hoffentlich auch praxisgerechter (weil auch Nutzdaten im Spiegel System
sind).

.. admonition:: komplette Instanz wird versioniert
   :class: tip

   Es werden alle Dateien aus ``$CADDOK_BASE`` in die Versionsverwaltung mit
   aufgenommen. Das umschließt die komplette Installation des
   Applikation-Servers mit den Paketen in ``$CADDOK_BASE/site-packages`` und den
   Konfigurationen (z.B. aus ``$CADDOK_BASE/etc``). Nicht dazu gehören der
   BLOB-Store und temporäre Speicher wie z.B. ``./tmp`` und ``./app_conf``.

Die im CDB Handbuch zur Komponentenarchitektur vorgestellten Verfahren, gehen
davon aus, dass es reicht, dass Kundenpaket zu versionieren. Theoretisch werden
damit alle Änderungen des Pakets erfasst. Für Softwarepakte von Contact oder
dritt-Anbietern mag das (inzwischen) auch noch stimmen in der Praxis wird eine
Weiterentwicklung i.d.R. aber von weiteren Faktoren geprägt sein. Dazu gehören
Objekte zum Testen, Objekte die ggf. (noch) nicht im Kundenpakt aufgenommen
wurden oder beispielsweise die Anbindung von (Unternehms-) Software im
Customizing.


Big Picture
===========

Bereits in der Einleitung wurde festgestellt, dass ein *sauberess*
Releasemanagement nicht willkürlich sein kann; es muss kausalen Ketten folgen
und unter den gegebenen Rahmenbedingungen (s.o. ) abbildbar sein. Welche
**Rahmenbedingungen** im Einzelnen zu beachten sind soll im Weiterem erarbeitet
werden. Als Gegenstand dient eine exemplarische Infrastruktur mit:

- einer PROD Instanz für den *Betrieb* der Anwendung im Unternehmen und
- einer QS Instanz in der (Anwender-) Tests durchgeführt werden.

Eine solche Infrastruktur ist sicherlich die *kleinst-mögliche*, sie reicht aber
aus um die Anforderungen und Verfahren rund um das Releasemanagement zu
erörtern.  In der Praxis wird man oftmals eine etwas größere Infrastruktur,
beispielsweise mit einem HotFix-System und einer gemeinsamen Entwickler Umgebung
(DEV) vorfinden. Ganz gleich wie aufwendig die Infrastruktur letztendlich ist,
es wird eine koordinierende Instanz benötigt.

.. admonition:: Maintainer koordiniert alle Änderungen (im SCM) 
   :class: tip

   Die Koordination der Änderungen im Entwicklerteam, den Anwendertests und den
   RollOuts übernimmt der *Maintainer*. Der Maintainer vermittelt zw. den
   Projekt-Terminen und den dadurch erforderlichen Planungen in der Entwicklung
   & im Test.

Um die am System angebrachten (Teil-) Änderungen zu verwalten bedient man sich
eines Source-Code-Managment-Systems (SCM). Als SCM System empfiehlt es sich --
aufgrund der hohen Flexibilität -- die Versionsverwaltung mit git_ abzubilden
(s.a. Foliensammlung zur pragmatischen Einarbeitung: `get git started`_).

Die Abbildung :ref:`big picture <figure-release_management-big_picture>` zeigt
den zeitlichen Verlauf dreier Änderungen in einer Infrastruktur mit PROD und QS.

.. _figure-release_management-big_picture:
        
.. figure:: release_management/big_picture.svg
   :alt:    Figure (big_picture.svg)
   :align:  center
           
   big picture: Änderungsverlauf mit PROD & QS

Links von t\ :sub:`0` ist die Historie und rechts der Planungsverlauf zu
sehen. In oberster Linie ist der Verlauf des im Betrieb befindlichen PROD
Systems zu sehen. Darunter der Verlauf des QS Systems. Desweiteren sind noch die
Entwicklungslinien zweier Weiterentwicklungen zu sehen, die folgend nur mit den
*Platzhaltern* ``foo`` und ``bar`` bezeichnet werden sollen.

- ``foo`` und ``bar``

Zwei exemplarische Weiterentwicklungen die z.B. an einen Lieferanten beauftragt
wurden oder aber im eigenen Haus abgewickelt werden. Beide Entwicklungslinien
wurden, wie die QS vom PROD abgespalten (**branch**) und beide werden später
wieder mit der PROD zusammengeführt (**merge**).

- PROD

Die letzte Änderung vor t\ :sub:`0` war ein *Hotfix*. Planmäßig sollen als
Nächstes (in der Reihenfolge) die letzten Änderungen aus QS, aus ``foo`` und aus
``bar`` in den Betrieb genommen werden.

- QS

Zum Zeitpunkt t\ :sub:`0` befindet sich eine Änderung in der QS, die in der
Projektplanung als nächstes ausgerollt werden soll. Für den RollOut muss die QS
mit dem PROD zusammengeführt werden (**merge**). Etwaige Konflikte aus den
Änderungen aus dem HotFix mit den letzten Änderungen aus dem QS müssen aufgelöst
werden.

.. admonition:: Abspaltung immer von der Entwicklungslinie des PROD
   :class: tip

   Ob und in welcher Form eine *aktuelle* Änderung z.B. aus dem QS System
   überhaupt in Betrieb genommen wird, kann nie mit absoluter Sicherheit gesagt
   werden. Deswegen empfiehlt es sich, jede Änderungen immer vom *aktuellen*
   PROD ausgehend zu starten.

.. _rm_create_branch:

Branch anlegen
==============

Die Aufgabe des Branch-Point ist es, einen klar definierten Zustand
festzuhalten. Dieser *eingefrorene* Zustand wird später beim Merge benötigt um
Konflikte der Weiterentwicklung mit den (letzten) Änderungen des Ziels seit dem
Branch zu erkennen und manuell in CDB *aufzulösen* anstatt einfach nur mit dem
Stand der Weiterentwicklung zu überspielen.

Die Abspaltung von Entwicklungslinien sollte immer vom *aktuellen* PROD
(**master**) aus erfolgen. Dort fangen alle Entwicklungen an, dort müssen sie am
Ende auch wieder hin führen.

.. code-block:: bash

   $ git checkout master

Mit dem Aus-checken des ``master`` wird ein ``cdbsql`` Kommando dieser Instanz
auch gleichzeitig gegen die PROD Datenbank verbinden (s. ``etc/dbtab``). Sofern
man sich nicht bereits auf dem Applikation-Server befindet sollte man
sicherstellen, dass die ``cdbpkg`` Kommandos, die im Folgenden abgesetzt werden,
eine Verbindung zur Datenbank und dem BLOB-Store des PROD Systems aufbauen kann.

Abspaltungen für Systeme wie z.B. QS werden regelmäßig (nach einem Merge oder
test) aus der PROD aktualisiert. Die Aktualisierung eines Feature-Branch aus der
PROD sollte i.d.R. nicht erforderlich sein, ist aber im Bedarfsfall
grundsätzlich möglich (s.a. `Merging vs. Rebasing
<https://www.atlassian.com/git/tutorials/merging-vs-rebasing>`__ & `The Golden
Rule of Rebasing
<https://www.atlassian.com/git/tutorials/merging-vs-rebasing#the-golden-rule-of-rebasing>`__).

Bevor der Branch angelegt werden kann, sollte der aktuelle Zustand der
Konfigurationen in der DB gebaut und als letzte Version im SCM aufgenommen
werden, von der aus dann der Branch erfolgen kann.

.. code-block:: bash

   $ cdbpkg build cust.plm               # DB export

Sollte ein ``git status`` eine Differenz anzeigen, so wird der nun im
Dateisystem vorliegende Stand als der *aktuelle* Stand im SCM festgehalten:

.. code-block:: bash

   $ git add --all .          # SCM-Commit ..
   $ git commit -m "retain last changes from PROD"
   $ cdbpkg commit cust.plm   # CDB-Commit
   $ git push                 # auf zentralem Server ablegen

Der Branch-Point kann nun auf dem aktuellen Stand des **master** angelegt
werden, das geschieht immer erst mal lokal und dann schiebt man diesen
Branch-Point auf den git-Server:

.. code-block:: bash

   $ git branch <branch-name>         # Branch lokal anlegen aber nicht aus-checken
   $ git push -u origin <branch-name> # Branch auf dem zentralem Server bereitstellen

Vergleicht man die bisherige Vorgehensweise mit denen im CDB Handbuch zur
Komponentenarchitektur vorgestellt Verfahren, so wird man merken, dass die
Verfahren dort an diesem Punkt enden. In der Praxis wird man aber bei der
Weiterentwicklung auf Nutzdaten angewiesen sein, für die man sich nun ein
Transport-Mechanismus ausdenken müsste. Diesen und anderen Problemen geht man am
einfachsten aus dem Weg, indem man zu jedem Branch-Point einen Export der DB
erstellt.

.. admonition:: DB Export zu jedem Branch-Point
   :class: tip

   Das Spiegelsystem für die Entwicklung der geplanten Änderung wird aus dem DB
   Export aufgebaut (s.a. :ref:`init_cdb_mirror`).

Der DB Export wird im jeweiligen Management Tool des DB Anbieters erstellt.  Für
die Ablage eignet sich ein Share auf den die Entwickler zugreifen können um sich
ggf. Spiegel Systeme aufbauen zu können. Evtl. reicht aber auch schon die
jeweilige System-Sicherung der DB für einen Import im Spiegel System aus. Egal,
wie man es macht, man sollte sich den Export zum Branch-Point solange aufheben,
bis die Änderung im PROD gemerged wurde (die Änderung also in Betrieb genommen
wurde). Hilfreich können Namen oder Listen sein, die Datum des Exports und den
Namen des Branch-Points erkennen lassen, wie z.B.::

  PROD-EXP-<YYYYMMDD-HH:MM>-<branch-name>

 
.. _rm_merge_branch:

Änderungen zusammenführen
=========================

ToDo: https://return42.github.io/cdb-tools/slides/cdb_comp/index.html#/38

- Dump & Commit des Ziel-Systems (cdbpkg-build/-commit & git commit)
- git worktree add /tmp/foo-start <branch-point>
- git checkout foo
- cdbpkg diff cust.plm -p /tmp/foo-start -d /tmp
- $ cd cust.plm
- $ git checkout master
- $ git merge foo                               # SCM-Merge
- $ cdbpkg patch /tmp/patch_cust.fo_xx_yyyy     # CDB-Merge
- cdbpkg build cust.plm
- $ git add --all .
- $ git commit -m "merged branch 'foo'"
- $ cdbpkg commit cust.plm
