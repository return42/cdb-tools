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

Um die am System angebrachten Teil-Änderungen zu verwalten bedient man sich
eines Source-Code-Managment-Systems (SCM). Die parallelen Entwicklungen auf
Basis der Komponentenarchitektur bedingen entsprechend viele parallele
Entwicklungslinien, s.a. `SCM-Branching`_. Damit empfiehlt es sich git_ als
SCM-System einzusetzen, das über ein besonders leichtes, schnellws und flexibles
Branching-Model verfügt.

.. admonition:: Als SCM-System bietet sich git_ an
   :class: tip

   Andere SCM-System insbesondere zentrale SCM-Systeme wie SVN eignen sich
   weniger, da sie bei der Arbeit mit Branches zu schwach sind und kaum
   brauchbare Unterstützung bieten.  *Sollten Sie noch SVN verwenden, dann
   wechseln Sie JETZT zu* git_. Siehe auch Foliensammlung zur pragmatischen
   Einarbeitung: `get git started`_.

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
die Patch-Serie der grünen Linie (``foo``) an das Ende der QS angehängt werden
würde.

.. _rm_merge_cdbpg_patch:

Merge mit git und cdbpkg Tools
==============================

Die Zusammenführung zweier Entwicklungslinien soll wieder am Beispiel
:ref:`qs-merge <figure-rm-qs-merge>` erfolgen, bei dem der QS-Branch in die
PROD-Linie gemerged wird.

.. admonition:: Vor einem Merge oder Branch letzten Änderungsstand comitten.
   :class: tip

   Bevor eine Merge durchgeführt oder einen Branch abspaltet wird, sollte zuvor
   sichergestellt werden, dass auch der aktuelle Stand im SCM commited wurde.

Da bei CONTACT Elements Anpassungen auch in der DB vorhanden sein können, stellt
man zuerst sicher, dass alle Änderungen im SCM-System comitted sind. Dazu geht
man auf das Ziel-System -- hier im Beispiel ist das PROD (**master**) -- und
leitet die Konfiguration in die JSON Dateien aus:

.. code-block:: bash

   # !!! Auf dem Ziel-System / im Ziel-Branch (z.B. master)  !!!
   $ git checkout master
   $ cdbpkg build cust.plm               # DB export

Sollte danach ein ``git status`` eine Differenz anzeigen, so wird der nun im
Dateisystem vorliegende letzte Änderungsstand als der *aktuelle* Stand im SCM
(im **master** Branch) festgehalten:

.. code-block:: bash

   # Auf dem Ziel-System / im Ziel-Branch (z.B. master)
   $ git add --all .          # SCM-Commit ..
   $ git commit -m "retain last changes from PROD"
   $ cdbpkg commit cust.plm   # CDB-Commit
   $ git push                 # auf zentralem Server ablegen

.. admonition:: Vor einem Merge muss das Diff der CDB-Konfigurationen ermittelt
                werden.
   :class: tip

   Die Konfigurationen sind zwar in den JSON Dateien enthalten, für einen Merge
   eignet sich dieses Format aber nicht. Für die Zusammenführung zweier
   Konfigurationen erzeugt man mit ``cdbpkg diff`` einen Patch den man mit
   ``cdbpkg patch`` einspielen kann. Anschließend kann man die Änderungen in CDB
   recherchieren und ggf. vorhandene Konflikte auflösen..

Das Kommando ``cdbpkg diff`` erechnet die Differenz zwischen zwei Ständen der
Konfiguration eines Pakets. Um die Differenz des Kunden-Pakets (``cust.plm``) in
der Änderungslinie (QS) zu berechnen wird dazu der Ausgangspunkt, also
Branch-Point der QS Linie und der letzte Stand der Änderungslinie (QS)
benötigt, siehe Abb. :ref:`rm-cdbpkg-diff-qs`:

.. _rm-cdbpkg-diff-qs:

.. figure:: release_management/cdbpkg-diff-qs.svg
   :alt:    Figure (rm-cdbpkg-diff-qs)
   :align:  center

   merge: cdbpkg diff & cdbpkg patch

Der Ausgangspunkt des Feature-Branch ist der branch-point |branch-point| an dem
die Änderungslinie abzweigt. Den Commit der Abzweigung kann man mit folgendem
Kommando ermitteln::

  $ git log --oneline --decorate --graph --all
  ...
  | * 8e448cd (hello-world) hello-world: add changelog
  | * 0dd2abe add hello-world script
  * | c1ce07c add remark about 'hello world' order
  |/
  * 9af1a51 add README
  * 849c175 inital boilerplate

Obiges Log-Beispiel stammt aus der Foliensammlung `get git started`_, das
Reposetory dazu ist `github.com/return42/git-teaching
<https://github.com/return42/git-teaching/network>`__. Es soll hier ersatzweise
als ein Beispiel dienen um den Commit zu *finden*, an dem der branch-point
|branch-point| abzweigt, in dem Beispiel ist zu sehen, dass der
``(hello-world)`` Branch bei Commit ``9af1a51`` abzweigt. Neben dem ``git log``
kann man aber auch andere Werkzeuge wie z.B. die `Git Extensions
<https://gitextensions.github.io/>`__ verwenden (s.a. `git GUI Clients
<https://git-scm.com/downloads/guis>`__) um die Historie zu visualisieren.

Im Beispiel Abb. :ref:`rm-cdbpkg-diff-qs` zweigt die QS Linie zum Zeitpunkt t\
:sub:`qs` ab, wir nehmen an, dass der Branch-Point bei einem Commit ``4711``
liegt. Damit wir den Diff anfertigen können muss der Stand zum Zeitpunkt t\
:sub:`qs` (also commit ``4711``) nun in einen separaten Ordner ausgecheckt
werden. Hier im Beispiel verwenden wir ``/tmp/qs-branch-point`` (kann später
wieder gelöscht werden).

.. code-block:: bash

   # !!! Auf dem Quell-System / im Feature-Branch (z.B. foo oder qs)  !!!
   $ git checkout qs
   ...
   # git worktree add <workspace-folder> <branch-point>
   $ git worktree add /tmp/qs-branch-point 4711

Nachdem Feature-Branch ``qs`` und der Branch-Point ausgecheckt wurden, kann nun
mit ``cdbpkg diff`` die Differenz zwischen den beiden Konfigurationsständen des
``cust.plm`` Pakets berechnet werden.

.. code-block:: bash

   $ cdbpkg diff -p /tmp/qs-branch-point -d /tmp/merge-qs-patch cust.plm
   Writing changes to directory /tmp/merge-qs-patch

Der cdbpkg-Patch liegt nun im Ordner ``/tmp/merge-qs-patch`` und man kann mit
dem eigentlichen Merge anfangen. Als Erstes werden die Sourcen mit dem SCM
gemerged. Dazu wechselt man in den Branch, in den man die Änderungen mergen
will, wichtig ist wieder, dass die cdbpkg Tools auf einen BLOB-Store und die DB
(des Ziel Systems) zugreifen können.

.. admonition:: Die cdbpkg Tools müssen beim Merge Zugriff auf das Ziel System haben
   :class: tip

   Bei einem Merge z.B. von einem Feature-Branch in die QS wird man den Merge
   direkt im QS System ausführen, da hier Ausfallzeiten i.d.R. nicht relevant
   sind. Die im Betrieb befindliche PROD wird man kaum längere zeit ausfallen
   lassen können, deshalb wird man sich i.d.R. ein Spiegel-System (Kopie der
   PROD) aufsetzen und den Merge dort durchführen. Mit einem solchen
   Spiegel-System kann der RollOut vorbereitet und getestet werden.

Hier in den Beispielen *mergen* wir immer direkt in das Ziel System, in diesem
Beispiel also direkt in die PROD (``master``). **Bei dem Merge muss man beachten,
dass man nur den Source Code nicht aber die ganze Konfiguration in den JSON
Dateien mergen darf**. Der Merge beginnt deshalb erst mal ganz normal:

.. code-block:: bash

   # !!! Auf dem Ziel-System / im Ziel-Branch (z.B. master)  !!!
   $ git checkout master
   ...
   $ git merge qs --no-commit --no-ff     # SCM merge
   Auto-merging cust.plm/cust/plm/module_metadata.json
   ...
   CONFLICT (content): Merge conflict in cust.plm/cust/plm/module_metadata.json
   Automatic merge failed; fix conflicts and then commit the result.

Ganz gleich ob man an dieser Stelle einen Conflict erhalten hat oder nicht, das
merge Kommando hat (versucht) die JSON Dateien aus dem ``qs`` Branch in den
``master`` Branch zu mergen und dass soll ja nicht sein.

Deshalb muss nun der Merge für die JSON Dateien sozusagen wieder auf den Stand
*zurück gespult* werden, der im ``master`` als Letztes eingecheckt ist. Am
einfachsten geht das bei git mit ``checkout --ours``:

.. code-block:: bash

   $ cd cust.plm/cust/plm
   ...
   $ git checkout --ours configuration module_metadata.json
   $ git checkout --ours content_metadata.json patches # ab CDB15 nicht mehr erforderlich
   ...
   $ git add configuration module_metadata.json
   $ git add content_metadata.json patches             # ab CDB15 nicht mehr erforderlich


.. admonition:: Konfiguration (JSON) darf nicht vom SCM-System gemerged werden.
   :class: tip

   Die Konfigurationen in den JSON Dateien werden nicht gemerged! Für den Merge
   der Konfiguration hat man sich mit ``cdbpkg diff`` einen Patch erzeugt, den
   man einspielen muss. Anschließend kann man die Änderungen in CDB
   recherchieren und ggf. vorhandene Konflikte auflösen..

Mit ``git status`` kann man nun überprüfen ob es auch Konflikte außerhalb der
JSON Dateien im Source-Code gab. Wenn das der Fall ist, muss man diese Konflikte
auflösen und die dabei angebrachten Änderungen mit ``git add`` in den *Stage*
aufnehmen. Nachdem alle Konflikte aufgelöst sind sollte in der ``git status``
Ausgabe ein Satz wie *All conflicts fixed but you are still merging.* zu finden
sein, hier eine beispielhafte Ausgabe:

.. code-block:: bash

  On branch testmerge
  All conflicts fixed but you are still merging.
    (use "git commit" to conclude merge)

  Changes to be committed:

          modified:   cust/plm/configuration/misc/cdb_dialog.json
          modified:   cust/plm/configuration/patches/cs.documents/classes/document.json
          modified:   cust/plm/configuration/patches/cs.pcs.projects/classes/cdbpcs_project.json

Sollte in der Ausgabe noch ein *Unmerged paths* auftauchen, so hat man noch
nicht alle Konflikte im Source-Code aufgelöst.

.. code-block:: bash

   Unmerged paths:

       both modified:   cust/plm/foo.py

Erst wenn alle Konflikte im Source-Code aufgelöst sind hat man wieder eine
*lauffähige* Instanz. In der kann als nächstes die Konfiguration eingespielt
werden. Dazu nimmt man den zuvor erzeugten cdbpkg-Patch ``/tmp/merge-qs-patch``:

.. code-block:: bash

   $ cdbpkg patch /tmp/merge-qs-patch     # CDB-Merge

Nun kann man in CDB die Änderungen recherchieren und und etwaige Konflikte
auflösen. Der Merge ist abgeschlossen, sobald man der Überzeugung ist, dass alle
Änderungen korrekt übernommen wurden. Man hat dann Änderungen im Dateisystem und
an der Konfiguration in der DB die noch nicht ins SCM Commited wurden. Um den
Merge zu vollziehen und im SCM aufzunehmen muss man wieder einen *build*
erzeugen und dann alles ins SCM als auch in CDB (app_conf) *committen*:

.. code-block:: bash

   $ cdbpkg build cust.plm
   ...
   $ git add --all .
   $ git commit -m "merged branch 'qs'"
   $ cdbpkg commit cust.plm


.. _rm_create_branch:

Branch anlegen
==============

Die Aufgabe des Branch-Point ist es, einen klar definierten Zustand festzuhalten
(s.a. `Branches-in-a-Nutshell
<https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell>`__) auf
dem eine Änderungslinie aufbaut.  Dieser *eingefrorene* Zustand wird von CDB
später beim Merge benötigt um die Differenz zwischen zwei Ständen der
Konfig. (DB,JSON) eines Pakets zu berechnen, s.a. :ref:`rm-cdbpkg-diff-qs`.

.. _figure-rm-branch-foo:

.. figure:: release_management/branch-foo.svg
   :alt:    Figure (branch-foo.svg)
   :align:  center

   branch-point: Abzweigung für einen Feature-Branch

Die Abbildung :ref:`branch point <figure-rm-branch-foo>` zeigt den zeitlichen
Verlauf des Feature-Branch ``foo`` in einer Infrastruktur mit PROD und
QS. Abspaltungen für Systeme wie z.B. QS werden regelmäßig (nach einem Merge
oder Test) aus der PROD aktualisiert. Die Aktualisierung eines Feature-Branch
aus der PROD sollte i.d.R. nicht erforderlich sein, ist aber im Bedarfsfall
grundsätzlich möglich (s.a. `Merging vs. Rebasing
<https://www.atlassian.com/git/tutorials/merging-vs-rebasing>`__ & `The Golden
Rule of Rebasing
<https://www.atlassian.com/git/tutorials/merging-vs-rebasing#the-golden-rule-of-rebasing>`__).

Inital beginnt der foo-Branch am Branch-Point zum Zeitpunkt t\ :sub:`foo`.  Die
Abspaltung von Entwicklungslinien sollte immer vom *aktuellen* PROD (**master**)
aus erfolgen. Dort fangen alle Entwicklungen an, dort müssen sie am Ende auch
wieder hin.

Um sicherzustellen, dass alle Änderungen aus der DB bereits im SCM
sind wird prophylaktisch ein ``build`` erzeugt:

.. code-block:: bash

   # !!! Auf dem master (PROD)  !!!
   # sollte eigentlich schon ausgechekt sein ...
   $ git checkout master 

Wichtig ist wieder, dass die cdbpkg Tools auf einen BLOB-Store und die DB
zugreifen können (hier im Beispiel ist das der Applikation Server der PROD).


!!!!!!!!!!! hier gehts weiter !!!!!!!!!!!!



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


Commit-Messages
===============

In der Praxis wird den Commit-Messages leider in viel zu vielen Projekten und
leider auch von vielen Zulieferern noch zu wenig Beachtung geschenkt, dabei sind
die Commit-Messages insbesondere bei langlebigen Projekten und wechselnden
Projektteams von besonderem Wert.

Saubere Commit-Messages sind erste Voraussetzung für eine Recherche.  Eine
Commit-Message gibt Auskunft darüber, was eine Änderung bezwecken soll und was
die Motivation zu dieser Änderung war. Die Historie eines Änderungsverlaufs wird
durch die Summe der Commit-Messages beschrieben. In dieser Historie will man
sich als Entwickler bewegen und einen Änderungsverlauf verstehen, ohne dass man
dazu die einzelnen Teil-Änderungen im Detail anschaut. Es muss im Verlauf der
Historie zumindest grob erkennbar werden, *was, wann, wo und warum* geändert
wurde. Das wird z.B. deutlich wenn es um die Auflösung von Konflikten geht,
dabei muss man (beim Merge) wissen, warum *diese Änderung hier im Branch* anders
ausgefallen ist als *die gleiche Änderung im anderen Branch*. Ohne die
inhaltlichen, fachlichen und ggf. auch technischen Hintergründe einer Änderung
muss derjenige, der den Merge durchführt selber erahnen was die Gründe dafür
waren und wie man den Konflikt am besten auflöst .. keine gute Voraussetzung.

.. admonition:: Die Commit-Message sollte *einheitlich* und *ausdrucksstark*
                sein.
   :class: tip

   In der Praxis hat sich ein einfaches Schema bewährt::

      <tag>: <Zusammenfassung>

      Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
      eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
      voluptua.

Es hat sich bewährt die ersten Zeile am Anfang mit einem ``<tag>`` mit
anschließendem Doppelpunkt zu beginnen. Das ``<tag>`` sollte einen Hinweis auf
den Kontext geben, zu dem diese Änderung gehört. Z.B. ``FooFoo:`` für alle
Commits (Beiträge), die das FooFoo-Feature implementieren und/oder korrigieren.
Der Kontext kann eine Fehler-/Vorfall-nummer (z.B.: ``I004711:`` für *issue
4711*), die Kurzbezeichnung eines Projekts, einer Sparte, eine Modulzuordnung
(z.B. ``doc:`` für Korrekturen an der Doku) sein. Manchmal kann der Kontext aber
auch ganz allgemeiner Natur sein, z.B. ``HotFix:``.

Die erste Zeile sollte ein kompakter *one-liner* mit Kontext und Zusammenfassung
sein, der aber auch nicht mehr als 80 oder 120 Zeichen haben sollte.  Darauf
folgt eine Leerzeile und danach kann ein ausführlicherer Text kommen der die
Hintergründe dieser Änderung beschreibt. Dabei beschreibt man nicht den
Source-Code, sondern das, was die Änderung bezwecken soll.  Für das Beispiel von
oben, bei dem ein HotFix angebracht wurde, könnte man beispielsweise schreiben::

  HotFix: Maskenfeld XYZ auf 'free' gesetzt

  Das Maskenfeld XYZ war mit einem defekten Auswahlbrowser XYZ konfiguriert, der
  falsche Werte lieferte. Damit die Anwender erst mal weiter arbeiten können
  wird dieser HotFix angebracht, mit dem die Editierbarkeit des Maskenfelds von
  'catalog' (nur aus dem Katalog zu befüllen) in 'free' (frei editierbar)
  geändert wird.

  Eine Überarbeitung des Auswahlbrowser XYZ findet derzeit schon im QS statt und
  soll später diesen HotFix ersetzen.

Wenn man später (:ref:`so wie oben gezeigt <rm_merge_branch>`) dann die
Überarbeitung aus dem QS in die PROD merged, dann weiß man aufgrund der
ausführlichen Commit-Message genau, wie man mit dem Konflikt rund um das
Maskenfeld XYZ umzugehen hat.

Ohne eine derartige Commit-Message und ohne den Hinweis auf *HotFix* und
*Überarbeitung im QS* wüsste man beim Merge nicht mehr warum die Änderung damals
im Hotfix (der nicht als solcher bezeichnet wurde) in dieser Form angebracht
wurde und man muss erahnen ob 'free' oder 'catalog' die richtige Auflösung für
den Konflikt darstellen.

Hier noch ein negativ-Beispiel::

  BugFix: Maskenfeld XYZ auf 'free' gesetzt

  Das Maskenfeld XYZ sollte auf 'free' gesetzt werden; ist hiermit
  erledigt.

Letztere Commit-Message hat für andere Entwickler als den Ersteller kaum
Informationsgehalt. Es fehlt der Hinweis darauf, dass es sich eigentlich nur um
einen HotFix handelt, das eigentlich der Auswahlbrowser kaputt ist und das
dieser noch überarbeitet wird und das diese Überarbeitung diesen HotFix dann
ersetzen wird.
