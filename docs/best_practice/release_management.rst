.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. |HotFix| image:: release_management/hotfix-point.svg
.. |branch-point| image:: release_management/branch-point.svg
.. |merge-point| image:: release_management/merge-point.svg
             
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

Die Abbildung :ref:`big picture <figure-rm-big_picture>` zeigt den zeitlichen
Verlauf dreier Änderungen in einer Infrastruktur mit PROD und QS. Jeder
kreisförmige Punkt entspricht einer (Teil-) Änderung die im SCM festgestellt
wird (kurz **commit**). Die Teil-Änderungen (Punkte) entlang einer
Entwicklungslinie (z.B. ``foo``) beschreiben in ihrer Gesamtheit den
Änderungsauftrag (das Feature) und werden allgemein auch als **Patch-Serie**
bezeichnet.

.. _figure-rm-big_picture:

.. figure:: release_management/big-picture.svg
   :alt:    Figure (big-picture.svg)
   :align:  center

   big picture (t\ :sub:`0`): Änderungsverlauf mit PROD & QS

Links von t\ :sub:`0` (*jetzt-Zeit*) ist die Historie und rechts der
Planungsverlauf zu sehen. In oberster Linie ist der Verlauf des im Betrieb
befindlichen PROD Systems zu sehen. Darunter der Verlauf des QS Systems.  Des
weiteren sind noch die Entwicklungslinien zweier Weiterentwicklungen zu sehen,
die folgend nur mit den *Platzhaltern* ``foo`` und ``bar`` bezeichnet werden
sollen.

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

.. _rm_merge_branch:

Zusammenführung zweier Entwicklungslinien
=========================================

Die Zusammenführung zwei Entwicklungslinien wird allgemein auch als **merge**
bezeichnet. Ziel ist es, die Änderungen aus der einen Entwicklungslinie mit
denen aus einer anderen Entwicklungslinie zusammenzuführen. Im folgendem
Beispiel sollen die vier Änderungen aus dem QS Branch in den PROD Branch
gemischt werden. Die Abbildung :ref:`qs-merge <figure-rm-qs-merge>` zeigt die
Entwicklungslinie des QS Branch bevor (obere Hälfte) und nachdem (untere Hälfte)
die Änderungen aus diesem Branch in den **master** (PROD) gemerged wurden.

.. _figure-rm-qs-merge:

.. figure:: release_management/merge-qs.svg
   :alt:    Figure (merge-qs.svg)
   :align:  center

   qs-merge: Zusammenführung der Änderungen aus QS mit PROD

Die Vorgehensweise beim Mergen ist immer gleich, egal ob man einen (Feature-)
Branch merged, oder wie hier eine Änderung aus dem QS übernehmen will. Die
Abbildung :ref:`merge-qs <figure-rm-qs-merge>` ist von daher, für sich alleine
erst mal nur abstrakt. Um das Beispiel etwas *konkreter* zu machen sei folgender
Kontext gegeben:

  Im PROD war ein Maskenfeld mit einem Auswahlbrowser konfiguriert. Dieser
  Auswahlbrowser lieferte aber falsche Werte. Damit die Anwender erst mal weiter
  arbeiten können wurde im PROD ein HotFix |HotFix| angebracht, mit dem die
  Editierbarkeit des Maskenfeld von *'nur aus dem Katalog zu befüllen'*
  (``catalog``) in *'frei editierbar'* (``free``) geändert wurde.  Anschließend
  hat man das Problem mit dem Auswahlbrowser (zeitnah) in der QS
  korrigiert. Dazu wurde keine neue QS aufgesetzt, sondern die bestehende
  genutzt, die wurde allerdings bereits abgespalten (branch) als der HotFix noch
  nicht im PROD war.

Das Beispiel mag etwas *konstruiert* anmuten, es beschreibt aber einen typischen
Fall (**conflict**), dem bei einem Merge besondere Beachtung geschenkt werden
muss. Schon aus der Beschreibung oben wird klar, dass im PROD und im QS parallel
und unabhängig voneinander an dem problematischen Maskenfeld (bzw.
Auswahlbrowser) Änderungen vorgenommen wurden: im PROD ist das Feld ``free`` und
im QS muss es -- mit dem korrigierten Auswahlbrowser -- auf ``catalog``
konfiguriert sein.  Werden die beiden Entwicklungslinien nun zusammengeführt, so
besteht ein *Konflikt* zw. dem HotFix |HotFix| und dem letztem Stand der QS, der
*nun* gemerged werden soll.

An welchem Commit der Konflikt mit der QS Entwicklungslinie auftritt brauchen
wir nicht zu wissen, wir sollten nur wissen, dass es immer zu Konflikten kommen
kann, wenn zwei Entwicklungslinien zusammengeführt werden. Konflikte müssen
erkannt und dann *fachlich* aufgelöst werden, so dass aus der Summe der beiden
Entwicklungslinien eine funktionierende und sinnvolle Anwendung entsteht.

.. admonition:: Konflikte müssen fachlich/inhaltlich aufgelöst werden, dafür
                gibt es keine Tools.
   :class: tip

   Vorausgesetzt die Entwicklungslinien sind sauber und bauen aufeinander auf,
   so sind die meisten Konflikte eher inhaltlicher/fachlicher Natur. Tools
   können helfen solche Konflikte zu erkennen, sie können aber keine fachlichen
   Fragen beantworten und sind somit auch nicht in der Lage die detektierten
   Konflikte selbständig aufzulösen.

Bei Weiterentwicklungen auf Basis der CONTACT Elements gibt es zwei Arten von
Konflikten:

- Konflikte im Quellcode: meist werden diese schon durch das SCM System (git)
  beim Merge erkannt. Der Merge Vorgang bleibt an der Stelle dann stehen und man
  muss ggf. manuell noch korrigierend eingreifen.

- Konflikte in der Konfiguration: Die Konfigurationen in der DB werden in JSON
  Dateien exportiert und im (Kunden-) Paket transportiert. Die JSON Dateien kann
  man nicht mit dem SCM mergen. Für die Zusammenführung zweier Konfigurationen
  gibt es die Tools ``cdbpkg diff`` und ``cdbpkg patch``. Nach dem ``cdbpkg
  patch`` kann man die Konflikte in CDB recherchieren und diese (fachlich) in
  CDB interaktiv auflösen.

Die Vorgehensweisen beim Merge werden im Abschnitt ":ref:`rm_merge_cdbpg_patch`"
detailliert beschrieben. Egal ob mit oder ohne Änderungen an der Konfiguration,
es gilt immer:

.. admonition:: Der Merge zweier Entwicklungslinien wird immer mit SCM-Commit
                abgeschlossen.
   :class: tip

   Beim Merge wird die **Patch-Serie** aus der einen Änderungslinie (QS) nahtlos
   an die andere Entwicklungslinie (PROD/master) angehängt. Alle einzelnen
   Commits aus QS sind jetzt Teil von PROD. Der merge-point |merge-point| ist
   auch ein Commit, er trägt u.A. die Änderungen in sich, die im Rahmen des
   Merge zur Konfliktauflösung vorgenommen wurden.

Im unteren Teil der Abbildung ":ref:`figure-rm-qs-merge`" ist bereits die PROD
Entwicklungslinie nach dem Merge dargestellt. Die Abb. ":ref:`rm-bp-merged-qs`"
zeigt das Eingangs gezeigte :ref:`big picture <figure-rm-big_picture>` nach dem
Merge.  In beiden Darstellungen ist zu sehen, dass sich die Commits, die vor dem
Merge nur in der QS-Linie waren, nun in der PROD-Linie wiederzufinden sind. Der
HotFix |HotFix| aus dem PROD verbleibt ebenfalls in der Historie, der
ggf. vorhandene Konflikt wurde ja im merge-point |merge-point| aufgelöst.

.. _rm-bp-merged-qs:

.. figure:: release_management/big-picture-merged-qs.svg
   :alt:    Figure (big-picture-merged-qs.svg)
   :align:  center

   big-picture (t\ :sub:`qs-merge`): Entwicklungslinien nach merge-qs 

Schaut man auf die Abbildung, so kann man schon erahnen, wie ein Merge des
Foo-branches aussehen würde. Ebenso wie eben beim Merge des QS in die PROD würde
später (gestrichelte Linien) der ``foo`` Branch in die QS gemerged werden, wobei
die Patch-Serie der grünen Linie (``foo``) an das Ende der QS angehängt würde.

.. _rm_merge_cdbpg_patch:

Merge mit SCM und cdbpkg Tools
==============================

Die Zusammenführung zweier Entwicklungslinien soll wieder am Beispiel
:ref:`merge-qs <figure-rm-qs-merge>` erfolgen, bei dem der QS-Branch in den PROD
gemerged wird.



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


   
.. _rm_create_branch:

Branch anlegen
==============

Die Aufgabe des Branch-Point ist es, einen klar definierten Zustand
festzuhalten. Dieser *eingefrorene* Zustand wird später beim Merge benötigt um
Konflikte der Weiterentwicklung mit den (letzten) Änderungen des Ziels seit dem
Branch zu erkennen und manuell in CDB *aufzulösen* anstatt einfach nur mit dem
Stand der Weiterentwicklung zu überspielen.

Die Abbildung :ref:`branch point <figure-rm-branch-foo>` zeigt den zeitlichen
Verlauf des Feature-Branch ``foo`` in einer Infrastruktur mit PROD und
QS. Inital beginnt der Branch am Branch-Point zum Zeitpunkt t\ :sub:`foo`.

.. _figure-rm-branch-foo:

.. figure:: release_management/branch-foo.svg
   :alt:    Figure (branch-foo.svg)
   :align:  center

   branch-point: Abzweigung für einen Feature-Branch


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
wurde). Hilfreich können Namen oder Listen sein, die das Datum des Exports und
den Namen des Branch-Points erkennen lassen, wie z.B.::

  PROD-EXP-<YYYYMMDD-HH:MM>-<branch-name>.


