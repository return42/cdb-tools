.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools_console:

=======
Konsole
=======

Features wie *tab-complition* oder *auto-doc*, wie man sie z.B. aus dem
Powerscript Studio kennt hat man bisher auf der Konsole vermisst. Die CDB-Tools
bringen Pakete wie ptpython_ und ptpdb_ mit, die solche Features auch in einer
Py-Konsole bereit stellen. Diese sind auf Linux & Unix Konsolen direkt nutzbar,
darüber hinaus haben Linux Konsolen schon immer *tab-completion* für die
Shell. Auf Windows gibt es lediglich die ``cmd.exe`` und deren Konsole ist wohl
eher eine Behinderung den eine Unterstützung bei der Arbeit .. um nicht zu sagen
echter Grumpf verglichen mit dem was man aus der Linx & Unix Welt kennt.

Die CDB-Tools schließen diese Lücke nun auch in der Windows Welt, indem sie den
Konsolen-Emulator `ConEmu`_ mit der clink_ Erweiterung bereit stellen.  Damit
hat man dann auch unter Windows Features wie *tab-complition* oder *auto-doc*
zur Verfügung.

Hier ein Beispiel für die Shell:

.. figure:: CunEmu-sh-completion.png


und hier ein Beispiel für einen Python oder Powerscript Interpreter in der
ConEmu mit ptpython_.


.. figure:: CunEmu-python-completion.png

