.. -*- coding: utf-8; mode: rst -*-
.. include:: ../refs.txt

.. _code-snipptes:

=============
Code Snippets
=============

In diesem Abschnitt finden Sie unsortierte Code-Schnippsel

CDB-Modul Checksumme
====================

Die Checksumme eines CDB Moduls (z.B. ``cust.plm``) ist in der Datei::

  cust.plm/cust/plm/module_metadata.json

Im Wert ``mudule.DATA.master_config_checksum`` hinterlegt:

.. code-block:: json

   { "module": {
     "DATA": {
       "cdb_object_id": "7332a770-2272-22e3-9b20-02cd3257cb0e",
       "is_interface_module": 0,
       "mandatory": 0,
       "master_config_checksum": "7df052a9478550db892a35677367abc5",
       "name": "Customizing",
       "package": "cust.plm"
     }
   }}

Die ``cdbpkg`` Kommandos nutzen diese Checksumme um z.B. zu ermitteln ob die
JSON Dateien konsistent sind und nicht durch ein unbeabsichtigtes SCM merge
beschädigt wurden.  Die Checksumme kann wie folgt berechnet werden:

.. code-block:: python

   from cdb.comparch import modules
   m = modules.Module.ByKeys("cust.plm")
   m._getLayout().refresh_std_conf_cheksum()
