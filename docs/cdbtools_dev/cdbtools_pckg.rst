.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_pckg:

Paketmanagement der CDB-Tools
=============================

Die CDB-Tools bringen ihr eigenes Paket-Managment (pip) mit, dass wenige bis
keine Abhängigkeiten zu CDB hat, also unabhängig von CDB genutzt werden kann (in
CDB 10 gibt es beispielsweise kein pip). Um die CDB Instanz nicht zu
manipulieren muss die Installation der Pakete immer in das User-Scheme
(``PYTHONUSERBASE``) der :ref:`Laufzeitumgebung <cdbtools_rte>` erfolgen.

.. hint::

   Bei der Verwendung von ``pip install`` in den CDB-Tools muss immer die Option
   ``--user`` verwendet werden. Bei unsachgemäßer Installation von Paketen mit
   pip kann die CDB-Software u.U. geschädigt werden, deshalb immer erst mal in
   einem *unkritischen* System testen!

::

  [CDBTools]$ pip install --user <package-name>

Die `pip.ini`_ Konfiguration liegt unter::

  $CDBTOOLS_HOME/bootstrap/pip.ini

Die CDB-Tools beziehen bereits diverse Pakete über PyPi_ die in der
`requirements.txt`_ Datei aufgelistet sind.


Hinweise
========

Setzt man im Rahmen der CDB-Tools den Schalter ``--user`` nicht, dann besteht
immer die Gefahr, dass das pip versucht ein Paket aus der CDB-Software zu
deinstallieren und durch ein aktuelleres im User-Scheme zu ersetzen. Damit wäre
die CDB-Software manipuliert, was unbedingt vermieden werden muss (Stichwort:
*non invasive Installation*).

Ab CDB15 ist auch ein pip in CDB enthalten. Dieses wird nicht von den CDB-Tools
genutzt, die haben (wie bereits erwähnt) ihr eigenes pip resp. Paketmanagment.
Bei dem pip aus CDB kann man den Schalter ``--user`` (eigentlich) nicht nutzen
und so ersetzt auch dieses pip einfach ältere CDB-Pakete in der CDB Software
durch neuere. Ein gutes Beispiel ist das von vielen Paketen genutzte `six
<https://pypi.python.org/pypi/six>`_ Paket, das auch in der CDB Software in
einer etwas älteren Version installiert ist. Dieses wird vermutlich als erstes
ersetzt sobald man moderne Pakete mit dem pip aus CDB installiert (wenn das zu
installierende Paket eine aktuellere Version des six benötigt). Bei dem six
Modul ist das evtl. nicht so ganz kritisch, es gibt aber auch recht betagte
Pakete in CDB die inzwischen schon mehrere Major-Releases hinter sich haben,
also auch funktional anders sein können.

Kurzum: auch das pip aus CDB beläßt die CDB-Software nicht im original. Dies ist
auch mit ein Grund, warum wir uns bei den CDB-Tools für die Installation in das
User-Scheme entschieden haben.

.. hint::

   Egal ob CDB oder CDB-Tools, wenn Sie auch bei unsachgemäßer Nutzung sicher
   vermeiden wollen, dass Manipulationen an der CDB-Software sattfinden, dann
   müssen Sie den CDB -Admins bzw. -Entwicklern die Schreibberechtigungen auf
   den ``CADDOK_RUNTIME`` Ordner entziehen.
