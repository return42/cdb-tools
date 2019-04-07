.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _cdbtools-pylint:

======
Pylint
======


Pylint_ ist ein Werkzeug zur Code-Analyse, dass sich in alle gängigen IDEs
integrieren lässt `[ref]
<https://pylint.readthedocs.io/en/stable/user_guide/ide-integration.html>`_.
Alle Code-Checker auf dem *freien Markt* kennen i.d.R. die CDB-Runtime, das
Vererbungsmodell in CDB und den ORM von CDB nicht, weshalb ihr Einsatz immer nur
mit Auflagen möglich ist.  Dennoch kann man sagen, dass bei einem umsichtigen
Einsatz dieser Werkzeuge die Code-Qualität und die Produktivität signifikant
verbessert werden kann.

In den CDB-Tools ist bereits eine Pylint_ Installation und ein exemplarisches
Setup (``templates/pylintrc``) enthalten.  Die Vorlage kopiert man sich am
besten in den Ordner der CDB-Instanz nach::

  $CADDOK_BASE\pylintrc

und nimmt es in das Reposetory in die Versionsverwaltung mit auf.  Pylint findet
diese Datei automatisch `[ref]
<http://pylint.pycqa.org/en/latest/user_guide/run.html#command-line-options>`__.


Emacs_:
  Am besten flycheck_ und flycheck-pos-tip_ über MELPA_ installieren und im
  CDB-Instanz Ordner eine `.dir-locals.el`_ einrichten (s.a. `Python in flycheck
  <https://www.flycheck.org/en/latest/languages.html?#python>`_).::

    ;;; .dir-locals.el
    ((nil
      . ((indent-tabs-mode . t)
         (fill-column . 120)
         ))
     (python-mode
      . ((indent-tabs-mode . nil)
        (flycheck-pylintrc . "pylintrc")
        (python-shell-interpreter . "c:/share/cdb-tools/win_bin/cdbtools-activate.bat")
        (python-shell-interpreter-args . "powerscript")
        ))
    )

  In der ``~/.emacs`` empfiehlt sich::

    (global-set-key [f6]                    'flycheck-mode)
    (global-set-key "\M-n"                  'flycheck-next-error)
    (global-set-key "\M-p"                  'flycheck-previous-error)


PowerScript Studio:
  Siehe Abschnitt ":ref:`powerscript_studio_pylint`"

Kommandozeile:
  CDB-Tools Umgebung entweder mit :ref:`cdbtools-activate_bat` oder
  :ref:`tools_sh_bat` anziehen und direkt aufrufen::

    [CDBTools]$ cd %CADDOK_BASE%
    [CDBTools]$ pylint -f colorized cust.plm\cust
    Using config file C:\share\cdb_cust_dev\pylintrc
    ************* Module cust
    C:  1, 0: Missing module docstring (missing-docstring)
    ************* Module cust.plm.__init__
    ...

