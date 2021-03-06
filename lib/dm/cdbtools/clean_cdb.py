# -*- mode: python; coding: utf-8 -*-
# pylint: disable=wrong-import-position, missing-docstring, invalid-name, unused-argument
# pylint: disable=too-many-statements, too-many-branches
"""Bereinigung der Datenbank

In CDB sammeln sich z.T. DB Einträge die nicht alle immer benötigt werden.
Nicht benötigte Einträge sollten von Zeit zu Zeit aufgeräumt werden um die DB
*schlank* und damit performant zu halten.

Das Aufräumen dieser Einträge lohnt sich insbesondere in Systemen die schon
länger im Betrieb sind und die bisher nicht aufgeräumt wurden.  In solchen
Systemen werden z.T. bis zu 60% der DB Resourcen auf *unnütze* Einträge
verschwendet.  Beispiele hierfür sind eine über mehrere Jahre angesammelte
Lizenzstatistik, alte ERP-Logs oder auch Message-Queue Einträge aus der
Historie.

Ob Optimierungen solcher Art für Ihre konkreten Anwendungszenarien überhaupt
geeignet sind oder ob dabei ggf. noch benötigte Daten gelöscht werden kann nicht
allgemein beantwortet werden.

ACHTUNG:  ES WERDEN DATEN GELÖSCHT!

  Das Löschen von Daten muss immer gegen die eigenen Anwendungszenarien geprüft
  werden! Testen Sie die Tools sorgfältig in einer Entwickler-Kopie bevor Sie
  diese auf ein produktives System anwenden!

  Weitere Infos: https://return42.github.io/cdb-tools/tools/clean_cdb.html

"""

# ==============================================================================
# imports
# ==============================================================================

import sys
from datetime import datetime, timedelta

from fspath.sui import SUI
from fspath.cli import CLI

from cdb import sqlapi
from cdb import util
from cdb.platform.tools import CDBObjectIDFixer
from cdb import progress

print_info_once_flag = False

def print_info_once(cliArgs):
    # pylint: disable=global-statement
    global print_info_once_flag
    if print_info_once_flag:
        return
    print_info_once_flag = True
    SUI.rst_title(u"ACHTUNG:  ES WERDEN DATEN GELÖSCHT!", level='part')
    SUI.rst_p(u"In Systemen, die noch nie oder schon länger nicht aufgeräumt wurden,"
              u" können die SQL Statements z.T. auch mal länger dauern oder beim Löschen"
              u" von großen Mengen kann das Statement auch mal an den Grenzen des "
              u" Transaction-Log scheitern!!")

    SUI.rst_p(u"Lesen Sie die Hinweise auf:")
    SUI.rst_p(u"https://return42.github.io/cdb-tools", level=1)
    if not SUI.ask_yes_no(u"Es werden Daten geändert, fortfahren?", default='n'):
        raise cliArgs.Error(42, "Abbruch durch den Benutzer")

def count_db_rows(table_name, condition=""):
    t = sqlapi.SQLselect("COUNT(*) FROM %s %s" % (table_name, condition))
    return sqlapi.SQLinteger(t, 0, 0)

def truncate_table(table_name):
    c = count_db_rows(table_name)
    if not c:
        SUI.rst_p("Tabelle %s enthält keine Datensätze." % table_name)
        return

    SUI.rst_p(u"ACHTUNG, ES WERDEN ALLE EINTRÄGE IN DER TABELLE::", level=1)
    SUI.rst_p(table_name, level=2)
    SUI.rst_p(u"GELÖSCHT!!!", level=1)

    if SUI.ask_yes_no(u"Sollen ALLE Einträge jetzt gelöscht werden?", default='n'):
        sqlapi.SQL("TRUNCATE TABLE %s" % table_name)
        SUI.rst_p("Tabelle %s wurde geleert." % table_name)
        SUI.echo("fixing object dict ...")
        util.ObjectDictionary.repair(table_name, SUI.echo, progress)

    else:
        SUI.rst_p("Kein Daten gelöscht")

def cli_clean_lstatistics(cliArgs):
    u"""
    Löschen aller Einträge der Lizenz-Statistik ('lstatistics')

    Die Lizenstatistik wächst kontinuierlich an. In lang laufenden Systemen mit
    vielen Benutzern ist die Statistik oftmals eine der größten Tabellen. Sofern
    die Statistik nicht ausgewertet wird, kann sie auch von Zeit zu Zeit mal
    gelöscht werden.
    """
    print_info_once(cliArgs)
    _doc = cli_clean_lstatistics.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    SUI.rst_p('\n'.join(_doc[1:]))

    c = count_db_rows('lstatistics')
    SUI.rst_p("Anzahl Einträge in der Lizenzstatistik total: %s" % c)

    if cliArgs.truncate:
        truncate_table('lstatistics')
        return

    clause = []
    if cliArgs.days != 0:
        d = datetime.now() - timedelta(days=cliArgs.days)
        clause.append("lbtime < '%s'" % d.strftime('%Y.%m.%d %H:%M:%S'))

    if clause:
        clause = "WHERE " + " AND ".join(clause)
        SUI.rst_p("Einschränkung auf Datensätze (Relation lstatistics)::")
        SUI.rst_p(clause, level=1)
    else:
        clause=""

    c = count_db_rows('lstatistics', clause)
    if not c:
        SUI.rst_p("Keine passenden Datensätze vorhanden.")
        return
    SUI.rst_p("Es werden %s Datensätze gelöscht." % c)

    c = 0
    if SUI.ask_yes_no(u"Sollen die Lizenz-Statistik Einträge jetzt gelöscht werden?", default='n'):
        c = sqlapi.SQLdelete("FROM lstatistics " + clause)
    if c == 0:
        SUI.rst_p(u"Es wurden keine Daten gelöscht.")
    else:
        SUI.rst_p(u"%s Einträge gelöscht" % c)


def cli_clean_mq(cliArgs):
    u"""
    Bereinigen der MQ-Anwendungen

    Es werden alle Message-Queues aufgelistet und Vorschläge zum Reduziern der
    Daten gemacht.
    """
    def _drop_txt(mq):
        SUI.rst_p(u"Löschen der Langtext Einträge zu denen kein Job mehr existiert:")
        c = sqlapi.SQLdelete(
            "FROM %s_txt WHERE cdbmq_id NOT IN (SELECT cdbmq_id FROM %s)" % (mq, mq))
        SUI.rst_p("%s Langtext-Zeilen (%s) gelöscht." % (c, mq+'_txt'))

    print_info_once(cliArgs)
    _doc = cli_clean_mq.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    SUI.rst_p('\n'.join(_doc[1:]))

    clause = ["cdbmq_state in ('F', 'D')"]

    if cliArgs.days != 0:
        d = datetime.now() - timedelta(days=cliArgs.days)
        clause.append("cdbmq_enqtime < %s" % sqlapi.SQLdbms_date(d))

    if clause:
        clause = "WHERE " + " AND ".join(clause)
    else:
        clause = ""

    rows = sqlapi.RecordSet2("cdb_tables", "type = 'T'")
    mq_tables = []
    mq_txt_tables = []
    for r in rows:
        if r.table_name.startswith('mq_'):
            if r.table_name.endswith('_txt'):
                mq_txt_tables.append(r.table_name)
            else:
                mq_tables.append(r.table_name)

    mq_tables.sort()
    for mq in mq_tables:

        SUI.rst_title(mq, level='section')

        c = count_db_rows(mq)
        SUI.rst_p("Anzahl Jobs total: %s" % c)

        if mq in ('mq_cad_job_server_param'
                  , 'mq_cad_job_server'
                  , 'mq_cad_job_server_cmd'
                  , 'mq_cad_job_server_log'
        ):
            SUI.rst_p("Muss manuell gelöscht werden, da diese MQ kein Standard ist.")
            continue
#        if c == 0:
#            continue

        if cliArgs.truncate:
            truncate_table(mq)
            if mq + '_txt' in mq_txt_tables:
                _drop_txt(mq)
            continue

        SUI.rst_p("Einschränkung auf Datensätze (Relation %s)::" % mq)
        SUI.rst_p(clause, level=1)

        c = count_db_rows(mq, clause)
        if not c:
            SUI.rst_p("Keine passenden Jobs in der MQ vorhanden.")
            if mq + '_txt' in mq_txt_tables:
                _drop_txt(mq)
            SUI.wait_key()
            continue
        SUI.rst_p("Es werden %s Jobs gelöscht." % c)

        c = 0
        if SUI.ask_yes_no(u"Sollen die Jobs jetzt gelöscht werden?", default='n'):
            c = sqlapi.SQLdelete("FROM %s " % mq + clause)
        if c == 0:
            SUI.rst_p(u"Es wurden keine Daten gelöscht.")
        else:
            SUI.rst_p(u"%s Einträge gelöscht" % c)
            c = count_db_rows(mq)
            SUI.rst_p("Anzahl Jobs total: %s" % c)

        if mq + '_txt' in mq_txt_tables:
            _drop_txt(mq)


def cli_clean_erplog(cliArgs):
    u"""Reduzieren der ERP-Log Einträge.

    Das ERP-Log wächst z.T. rasant an, mit diesem Tool können die Einträge im
    ERP-Log gelöscht werden.

    """
    print_info_once(cliArgs)
    _doc = cli_clean_erplog.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    SUI.rst_p('\n'.join(_doc[1:]))

    c = count_db_rows('erp_log')
    SUI.rst_p("Anzahl ERP-Log Einträge total: %s" % c)

    if cliArgs.truncate:
        truncate_table('erp_log')
        return

    clause = []
    if cliArgs.sap_system != "all":
        clause.append("erp_system = '%s'" % cliArgs.sap_system)

    if cliArgs.days != 0:
        d = datetime.now() - timedelta(days=cliArgs.days)
        clause.append("log_date < %s" % sqlapi.SQLdbms_date(d))

    if not cliArgs.drop_result:
        clause.append(r"log_text NOT LIKE '%Result:%'")

    clause = " AND ".join(clause)

    SUI.rst_p("Einschränkung auf Datensätze (Relation erp_log)::")
    SUI.echo("    WHERE " + clause)
    c = count_db_rows('erp_log', "WHERE " + clause)
    SUI.echo("")
    if not c:
        SUI.rst_p("Keine passenden Datensätze vorhanden.")
        return

    SUI.rst_p("Es werden %s Datensätze gelöscht." % c)

    if not SUI.ask_yes_no(u"Sollen die Log-Einträge jetzt gelöscht werden?", default='n'):
        SUI.rst_p(u"Es wurden keine Daten gelöscht.")
        return

    c = sqlapi.SQLdelete("FROM erp_log WHERE " + clause)
    SUI.rst_p(u"%s Einträge gelöscht" % c)


def cli_clean_all(cliArgs):
    u"""Alle Bereinigungen nacheinander durchführen."""

    print_info_once(cliArgs)
    _doc = cli_clean_all.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0], level='part')

    cli_clean_lstatistics(cliArgs)
    SUI.wait_key()
    cli_clean_erplog(cliArgs)
    SUI.wait_key()
    cli_clean_mq(cliArgs)
    SUI.wait_key()
    cli_clean_object_dict(cliArgs)


def cli_clean_object_dict(cliArgs):
    u"""Bereinigung des Object-Dictionary (cdb_object).

    Ruft die Methode util.ObjectDictionary.repair zum Bereinigen der Object-IDs
    für alle Basisklassen (Relationen) auf.

    Alternative:

      powerscript $CADDOK_INSTALLDIR/cdb/schema/updates/tools/repair-cdbobjid.py

    """
    print_info_once(cliArgs)
    _doc = cli_clean_object_dict.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    SUI.rst_p('\n'.join(_doc[1:]))

    id_fixer = CDBObjectIDFixer(SUI.echo, progress)
    for rel in id_fixer.find_affected_relations():
        SUI.echo("fixing %s ..." % rel)
        util.ObjectDictionary.repair(rel, SUI.echo, progress)


# Noch zu klären:
#
# - kann 'cdbwf_role_cache' geleert werden?
# - Kriterien um 'cdb_evlog' Einträge zu löschen?
# - Die Relation cdbqc_history (Kennzalen, Historie) ist ein Resourcenfresser


def main():

    def add_common_options(cmd):
        cmd.add_argument(
            '--days', type = int, default = 30
            , help = 'cleanup aller Daten die mind. <days> Tage alt sind'
        )
        cmd.add_argument(
            '--truncate', action = 'store_true'
            , help = ("Tabelle komplett leeren. ACHTUNG: Es werden ALLE"
                      " Einträge in der Tabelle mit SQL-TRUNCATE gelöscht"))

    cli = CLI(description=__doc__)

    lstatistics = cli.addCMDParser(cli_clean_lstatistics, cmdName='lstatistics')
    add_common_options(lstatistics)

    mq = cli.addCMDParser(cli_clean_mq, cmdName='mq')
    add_common_options(mq)

    erplog = cli.addCMDParser(cli_clean_erplog, cmdName='erplog')
    add_common_options(erplog)
    erplog.add_argument(
        '--sap-system', default = 'all'
        , help = 'SAP-System dessen Logs bereinigt werden sollen.')
    erplog.add_argument(
        '--drop-result', action = 'store_true'
        , help = "Die 'Result' Meldungen des SAP-GW sollen auch gelöscht werden")

    object_dict = cli.addCMDParser(cli_clean_object_dict, cmdName='object-dict')

    aio = cli.addCMDParser(cli_clean_all, cmdName='all')
    add_common_options(aio)
    aio.add_argument(
        '--sap-system', default='all'
        , help = 'SAP-System dessen Logs bereinigt werden sollen.')
    aio.add_argument(
        '--drop-result', action = 'store_true'
        , help = "Die 'Result' Meldungen des SAP-GW sollen auch gelöscht werden")

    cli()

if __name__ == '__main__':
    sys.exit(main())
