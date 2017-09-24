#!powerscript
# -*- mode: python; coding: utf-8 -*-
"""
Bereinigung der Datenbank

In CDB sammeln sich z.T. DB Einträge z.B. aus Message-Queue Anwendungen oder
dem ERP-Log die nicht alle immer benötigt werden. Nicht benötigte Einträge
sollten von Zeit zu Zeit aufgeräumt werden um die DB *schlank* und damit
performant zu halten.

Das Aufräumen dieser Einträge lohnt sich insbesondere in schon lang laufenden
Systemen die bisher nicht aufgeräumt wurden. In solchen Systemen werden z.T.
bis zu 60% der DB Resourcen auf *unnütze* Einträge verschwendet (z.B. eine
über mehrere Jahre angesammelte Lizenzstatistik).

Ob Optimierungen solcher Art für Ihre konkreten Anwendungszenarien überhaupt
geeignet sind oder ob dabei ggf. noch benötigte Daten gelöscht werden kann
nicht allgemein beantwortet werden. Das Löschen von Daten muss immer gegen
die eigenen Anwendungszenarien geprüft werden! Testen Sie die Tools sorgfältig
in einer Entwickler-Kopie bevor Sie diese auf ein produktives System anwenden!

ACHTUNG:  ES WERDEN DATEN GELÖSCHT!

"""
# pylint: disable=wrong-import-position, missing-docstring, invalid-name, unused-argument

# ==============================================================================
# imports
# ==============================================================================

import dm # muss zuert importiert werden!

import sys
import os
import re
from datetime import datetime, timedelta

from fspath.sui import SUI
from fspath.cli import CLI

from cdb import sqlapi

print_info_once_flag = False

def print_info_once():
    # pylint: disable=global-statement
    global print_info_once_flag
    if print_info_once_flag:
        return
    print_info_once_flag = True
    _doc = __doc__.strip().split('\n')
    for block in '\n'.join(_doc[1:]).split('\n\n'):
        SUI.rst_p(block, level=1)
    SUI.wait_key()

def count_db_rows(table_name, condition=""):
    t = sqlapi.SQLselect("COUNT(*) FROM %s %s" % (table_name, condition))
    return sqlapi.SQLinteger(t, 0, 0)

def shrink_erp_log(obj_id, delete=False):

    # Wieviel Log-Einträge zu einem Objekt sind noch *unauffällig*?
    ERP_LOG_MAX  = 100

    # Abstand in Sekunden zw. zwei identischen Log-Einträgen, die als
    # 'voneinander unabhängig' bewertet werden können.
    TIME_DELTA = 1200

    ERP_LOG_MAX_SQL = (
        "SELECT obj_id, logcount FROM"
        "       (SELECT OBJ_ID, COUNT(*) AS LOGCOUNT FROM erp_log GROUP BY obj_id)"
        " WHERE logcount > %s"
        " ORDER BY logcount desc"
        )

    BY_ID = (
        "SELECT OBJ_ID, COUNT(*) AS LOGCOUNT FROM erp_log WHERE OBJ_ID='%s' GROUP BY obj_id"
        )

    if obj_id == 'all':
        sql = ERP_LOG_MAX_SQL % ERP_LOG_MAX
    else:
        sql = BY_ID % obj_id

    retVal = 0
    for obj in sqlapi.RecordSet2(sql = sql):

        sql = ("SELECT erp_system, counter, obj_id, log_date as date_time"
               " FROM erp_log"
               " WHERE obj_id = '%s'"
               " ORDER BY = log_date asc") % (obj.obj_id)

        # FIXME ... max_rows=100000
        rows = sqlapi.RecordSet2(sql=sql, max_rows=1000)

        row_1 = None
        row_2 = None
        try:
            row_1 = rows.next()
        except StopIteration:
            continue

        while True:
            try:
                row_2 = rows.next()
            except StopIteration:
                break

            if re.compile("Result: OK", re.IGNORECASE).search(row_2.log_text):
                row_1 = row_2
                continue

            elif row_1.log_text == row_2.log_text:
                row_1_time = datetime.strptime(row_1.log_date, '%Y.%m.%d %H:%M:%S')
                max_time   = row_1_time + timedelta(seconds = TIME_DELTA)
                row_2_time = datetime.strptime(row_2.log_date, '%Y.%m.%d %H:%M:%S')

                if row_2_time < max_time:
                    if delete:
                        retVal += 1
                        row_2.Delete()
                        row_1 = row_2
                else:
                    row_1 = row_2
    return retVal


def cli_shrink_erp_log(cliArgs):
    u"""Reduzieren der ERP-Log-Einträge.

    Das ERP-log wächst bei Fehlern im SAP-Abgleich rasant an. Mit dieser
    Operation können die sich wiederholenden ERP Einträge im Log eines Objektes
    auf das wesentlich *runter* gekürzt werden.
    """
    _doc = cli_shrink_erp_log.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    SUI.rst_p('\n'.join(_doc[1:]))
    print_info_once()

    c = count_db_rows('erp_log')
    if not c:
        SUI.rst_p(u"Es kann nichts bereinigt werden, das ERP-log ist leer")
        return

    SUI.rst_p(u"Es existieren insgesammt über alle Objekte %s Einträge." % c)
    if SUI.ask_yes_no(u"Sollen die Logs reduziert werden (kann lange dauern)?", default='n'):
        c = shrink_erp_log('all')
        SUI.rst_p(u"%s Einträge gelöscht" % c)
    else:
        SUI.rst_p(u"Es wurden keine Daten gelöscht.")

    return shrink_erp_log(cliArgs.obj_id, delete=False)


def cli_clean_lstatistics(cliArgs):
    u"""
    Löschen aller Einträge der Lizenz-Statistik ('lstatistics')

    Die Lizenstatistik wächst kontinuierlich an. In lang laufenden Systemen mit
    vielen Benutzern ist die Statistik oftmals eine der größten Tabellen. Sofern
    die Statistik nicht ausgewertet wird, kann sie auch von Zeit zu Zeit mal
    gelöscht werden.
    """
    _doc = cli_clean_lstatistics.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    SUI.rst_p('\n'.join(_doc[1:]))
    print_info_once()

    c = count_db_rows('lstatistics')
    if not c:
        SUI.rst_p(u"Es kann nichts bereinigt werden, die Lizenzstatistik ist leer")
        return

    SUI.rst_p(u"Es existieren %s Einträge." % c)
    if SUI.ask_yes_no(u"Soll die Daten wirklich gelöscht werden?", default='n'):
        c = sqlapi.SQLdelete("FROM lstatistics")

        SUI.rst_p(u"%s Einträge gelöscht" % c)
    else:
        SUI.rst_p(u"Es wurden keine Daten gelöscht.")

def cli_clean_mq(cliArgs):
    u"""
    Bereinigen der MQ-Anwendungen

    Es werden alle Message-Queues aufgelistet und Vorschläge zum Reduziern der
    Daten gemacht.
    """
    _doc = cli_clean_mq.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    SUI.rst_p('\n'.join(_doc[1:]))
    print_info_once()

    rows = sqlapi.RecordSet2("cdb_tables", "type = 'T'")
    mq_tables = []
    for r in rows:
        if r.table_name.startswith('mq_') and not r.table_name.endswith('_txt'):
            mq_tables.append(r.table_name)

    for mq in mq_tables:

        SUI.rst_title(mq, level='section')
        c = count_db_rows(mq)

        if not c:
            SUI.rst_p(u"Es kann nichts bereinigt werden, die Message-Queue '%s' ist leer." % mq)
        else:
            msg = u"In der Message-Queue '%s' sind %d Jobs eingetragen." % (mq, c)
            f = count_db_rows(mq, "WHERE cdbmq_state in ('F', 'D')")
            if not f:
                msg += u" Davon ist noch kein Job beendet (Fehler oder Done)."
            else:
                msg += (u" Davon sind %d Jobs beendet (Fehler oder Done)" % f)
            SUI.rst_p(msg)
            if f and SUI.ask_yes_no(u"Sollen die beendeten Jobs jetzt gelöscht werden?", default='n'):
                c = sqlapi.SQLdelete("FROM %s WHERE cdbmq_state in ('F', 'D')" % mq)
                SUI.rst_p(u"%s Einträge gelöscht" % c)

        c = sqlapi.SQLdelete("FROM mq_acs_txt WHERE cdbmq_id NOT IN (SELECT cdbmq_id FROM %s)" % mq)
        if c:
            SUI.rst_p("%s Zeilen Langtext (%s) gelöscht." % (c, mq+'_txt'))
        SUI.wait_key()


def cli_clean_all(cliArgs):
    u"""Alle Bereinigungen nacheinander durchführen."""

    _doc = cli_clean_all.__doc__.strip().split('\n')
    SUI.rst_title(_doc[0])
    print_info_once()

    cli_shrink_erp_log(cliArgs)
    cli_clean_lstatistics(cliArgs)
    cli_clean_mq(cliArgs)

# Noch zu klären:
#
# - kann 'cdbwf_role_cache' geleert werden?
# - Kriterien um 'cdb_evlog' Einträge zu löschen?

def main():
    cli = CLI(description=__doc__)
    _ = cli.addCMDParser(cli_clean_all, cmdName='all')
    _ = cli.addCMDParser(cli_clean_lstatistics, cmdName='lstatistics')
    _ = cli.addCMDParser(cli_shrink_erp_log, cmdName='erplog')
    _ = cli.addCMDParser(cli_clean_mq, cmdName='mq')
    cli()

if __name__ == '__main__':
    sys.exit(main())
