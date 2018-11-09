#!powerscript
# -*- mode: python; coding: utf-8 -*-
# pylint: disable=wrong-import-position, missing-docstring
"""Initialsierung eines CDB Spiegel-Systems

Zum Anlegen eines solchen Spiegels werden ein DB-Export und eine (Clone-) Kopie
des CADDOK_BASE Ordners benötigt (ohne BLOB storage).

Die Initialisierung einer CDB Instanz ist für Entwickler-Systeme gedacht,
die aus einem DB-Dump und einem Abzug der Sourcen aufgebaut werden.

Die Änderungen aus einer solchen Initialisierung sind unumkehrbar und
sollten nur von Personen durchgeführt werden, die wissen, was sie machen!

"""

import sys
import socket

from fspath.sui import SUI
from fspath.cli import CLI
from fspath import FSPath

# pylint: disable=import-error
from cdb import sqlapi
from cdb import version
# pylint: enable=import-error

from dm.cdbtools.helper import port_is_free

ELEMENTS_MAJOR = int(version.getVersionDescription().split(" ")[0].split(".")[0])
ELEMENTS_MINOR = int(version.getVersionDescription().split(" ")[0].split(".")[1])

FQDN = socket.getfqdn()

def deactivate_services():
    SUI.rst_title(u"CDB-Dienste deaktivieren")

    SUI.rst_p(
        u"Dies ist ein Spiegelsystem, damit die CDB-Clients nicht versuchen sich gegen"
        u" einen der CDB-Dienste des *original* Systems zu verbinden, sollten in einem"
        u" Spiegel alle Dienste des *original* Systems deaktiviert werden. Folgendes"
        u" Statement deaktiviert alle CDB-Dienste.::")

    sql = "cdbus_svcs SET active=0"
    SUI.rst_p(u"UPDATE " + sql, level=1)
    if SUI.ask_yes_no(u"Sollen die Dienste deaktiviert werden?") == SUI.YES:
        rows = sqlapi.SQLupdate(sql)
        SUI.rst_p(u"--> %s rows updated" % rows)
    else:
        SUI.rst_p(u"Dienste bleiben unverändert")
    SUI.wait_key()

def takeover_service():
    SUI.rst_title(u"CDB-Dienste einrichten")
    SUI.rst_p(u'Der FQDN dieses Hosts (localhost) ist: %s' % FQDN)
    SUI.rst_p(u"Es werden die minimal erforderlichen CDB-Dienste eingerichtet"
              u" um CDB starten zu können. Alle weiteren Dienste können danach"
              u" in einer CDB Sitzung interaktiv eingerichtet werden. Die Dienste"
              u" werden eingerichtet, indem die Konfiguration eines Application"
              u" Servers des *original* Systems für diesen Host *übernommen* und"
              u" als *default* Site eingerichtet wird."
              u" In CDB sind derzeit Dienste für folgende Hosts konfiguriert:")

    query = """
  SELECT hostname FROM cdbus_svcs
   WHERE svcname IN (
           'cdb.uberserver.Uberserver'
           , 'cdb.uberserver.services.apache.Apache'
           , 'cdb.uberserver.services.server.Launcher'
           , 'cdb.uberserver.services.blobstore.BlobStore' )
   GROUP BY hostname ORDER BY COUNT(hostname) DESC
"""

    if ELEMENTS_MAJOR == 15 and ELEMENTS_MINOR >= 1:
        query = """
  SELECT hostname FROM cdbus_svcs
   WHERE svcname IN (
           'cdb.uberserver.Uberserver'
           , 'cdb.uberserver.services.apache.Apache'
           , 'cdb.uberserver.services.authentication.GateKeeper'
           , 'cdb.uberserver.services.authentication.SessionCache'
           , 'cdb.uberserver.services.blobstore.BlobStore' )
   GROUP BY hostname ORDER BY COUNT(hostname) DESC
"""

    hostnames = [ x.hostname for x in sqlapi.RecordSet2(sql=query) ]
    orig_host = SUI.ask_choice(
        u"Von welchem Application Server soll die Konfiguration übernommen werden?", hostnames)

    sql = """
  UPDATE cdbus_svcs
     SET hostname='%s'
   WHERE hostname='%s'""" % (FQDN, orig_host)

    SUI.echo("\nÜbernahme der Konfiguration:: \n%s" % sql)
    rows = sqlapi.SQL(sql)
    SUI.rst_p(u"--> %s rows updated" % rows)
    SUI.wait_key()

    sql = """
  UPDATE cdbus_svcs SET active=1, autostart=1, site='default'
   WHERE hostname='%s' AND svcname IN (
           'cdb.uberserver.Uberserver'
           , 'cdb.uberserver.services.apache.Apache'
           , 'cdb.uberserver.services.server.Launcher'
           , 'cdb.uberserver.services.blobstore.BlobStore' )""" % (FQDN)

    if ELEMENTS_MAJOR == 15 and ELEMENTS_MINOR >= 1:
        sql = """
  UPDATE cdbus_svcs SET active=1, autostart=1, site='default'
   WHERE hostname='%s' AND svcname IN (
           'cdb.uberserver.Uberserver'
           , 'cdb.uberserver.services.apache.Apache'
           , 'cdb.uberserver.services.authentication.GateKeeper'
           , 'cdb.uberserver.services.authentication.SessionCache'
           , 'cdb.uberserver.services.blobstore.BlobStore' )""" % (FQDN)

    SUI.echo("Aktivierung der Basis-Dienste:: \n%s" % sql)
    rows = sqlapi.SQL(sql)
    SUI.rst_p(u"--> %s rows updated" % rows)
    SUI.wait_key()


def assert_service(svcname, hostname):
    cdbus_svcs = sqlapi.RecordSet2(
        sql="SELECT svcid FROM cdbus_svcs WHERE svcname='%s' AND hostname='%s'"
        % (svcname, hostname))
    query = ("SELECT hostname FROM cdbus_svcs WHERE svcname='%s' "
             " GROUP BY hostname ORDER BY COUNT(hostname) DESC") % (svcname)
    hostnames = [ x.hostname for x in sqlapi.RecordSet2(sql=query) ]
    if not cdbus_svcs and len(hostnames):
        SUI.rst_p((u"Dienst '%s' ist nicht für Host '%s' eingerichtet!"
                  u" Es stehen folgende Konfigurationen zur Verfügung,"
                  u" suchen Sie sich eine aus, die sie für %s "
                  u" verwenden möchten.") % (svcname, hostname, hostname))
        orig_host = SUI.ask_choice(
            u"Welche Server-Konfiguration soll übernommen werden?", hostnames)
        sql = """
  UPDATE cdbus_svcs
     SET hostname='%s', active=1, autostart=1, site='default'
   WHERE hostname='%s' AND svcname='%s' """ % (FQDN, orig_host, svcname)
        rows = sqlapi.SQL(sql)
        SUI.echo(u"\n--> %s rows updated" % rows)
    elif not len(hostnames):
        SUI.rst_p(u"Der Dienst %s existiert in dieser Umgebung nicht." % svcname)

    else:
        SUI.rst_p(u"Der Dienst %s ist bereits für den Host %s eingerichtet."
                  % (svcname, hostname))

def print_opts(opts):
    SUI.rst_p("Dienst-Optionen:")
    if not opts:
        SUI.echo('  keine')
    for row in opts:
        SUI.echo("* %-12s --> '%s'" % (row.name, row.value))

def check_port(opts):
    port = None
    for row in opts:
        if row.name in ('port', '--port'):
            port = row
            break

    if port and port.value:
        msg = "Der Dienst benutzt den IP-Port %s." % port.value
        isfree = port_is_free(port.value)
        if isfree:
            msg += " Der Port ist aktuell nicht belegt (kann vermutlich genutzt werden)."
        else:
            msg += " Der Port ist aktuell belegt (kann vermutlich NICHT genutzt werden)."
        SUI.rst_p(msg)
        p = SUI.ask("Auf welchem Port soll die Anwendung bereit gestellt werden?"
                    , default=port.value, count=5, valid_chars=r'\d')
        if int(p) != int(port.value):
            sql = ("update cdbus_svcopts SET value='%s' WHERE svcid='%s' AND name='%s' AND value='%s'"
                   % (p, port.svcid, port.name, port.value))
            rows = sqlapi.SQL(sql)
            SUI.rst_p(u"--> %s rows updated" % rows)

def auth_method():
    SUI.rst_title("Authentifizierung")
    opt_query = """
   SELECT svcid, name, value
     FROM cdbus_svcopts WHERE svcid IN (
           SELECT svcid FROM cdbus_svcs
            WHERE svcname='%s'
             AND hostname='%s')"""
    hostname = FQDN
    svcname  = 'cdb.uberserver.services.apache.Apache'
    opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))

    row_wsgi_auth_method = None

    for row in opts:
        if row.name == "wsgi_auth_method":
            row_wsgi_auth_method = row
            break

    if row_wsgi_auth_method is None:
        return

    SUI.rst_p("Aktuelle Methode zur Authentifizierung: %s" % row_wsgi_auth_method.value)

    x = sqlapi.RecordSet2('cdb_auth_plugin', "name = 'password'")

    if x and row_wsgi_auth_method.value != 'password':
        pwd_plugin = x[0]
        if SUI.ask_yes_no(u"Soll die Authentifizierung auf CDB-Passwörter umgestellt werden?") == SUI.YES:
            if not pwd_plugin.active:
                SUI.rst_p("Das Plugin zur Authentifizierung wird aktiviert ..")
                SUI.rst_p(u"--> %s rows updated"
                          % pwd_plugin.updated(active = 1))
            SUI.rst_p(u"Setze die Dienst-Option des Apache: %s = 'password' (es werden die CDB Passwörter genutzt)"
                      % (row_wsgi_auth_method.name, ))
            sql = ("update cdbus_svcopts SET value='password' WHERE svcid='%s' AND name='%s' AND value='%s'"
                   % (row_wsgi_auth_method.svcid, row_wsgi_auth_method.name, row_wsgi_auth_method.value))
            SUI.rst_p(u"--> %s rows updated" % sqlapi.SQL(sql))

    if row_wsgi_auth_method.value == 'password':
        reset_password()

def check_path(opts):
    for row in opts:
        if not row.name in ('base_path', 'path', 'vault_path'):
            continue
        SUI.echo("")
        SUI.echo("Der Dienst benutzt den Pfad (%s): %s" % (row.name, row.value))
        path = FSPath(row.value)
        if not path.EXISTS:
            SUI.rst_p("Der Pfad existiert nicht!")

        while True:
            new_path = SUI.ask_fspath(msg="Neuer Pfad: ", default=path)
            sql = ("update cdbus_svcopts SET value='%s' WHERE svcid='%s' AND name='%s' AND value='%s'"
                   % (new_path, row.svcid, row.name, row.value))
            rows = sqlapi.SQL(sql)
            SUI.rst_p(u"--> %s rows updated" % rows)
            try:
                new_path.makedirs()
                break
            except OSError:
                SUI.rst_p("Pfad kann nicht angelegt werden!")
                SUI.wait_key()


def check_login(opts):
    username = 'caddok'
    password = 'welcome'
    x = False
    for row in opts:
        if row.name in ('username', ):
            x = True
            SUI.echo(u"- setze Dienst-Option: %s = %s" % (row.name, username))
            sql = ("update cdbus_svcopts SET value='%s' WHERE svcid='%s' AND name='%s' AND value='%s'"
                   % (username, row.svcid, row.name, row.value))
            rows = sqlapi.SQL(sql) # pylint: disable=unused-variable

        if row.name in ('password',):
            x=True
            SUI.echo(u"- setze Dienst-Option: %s = %s" % (row.name, password))
            sql = ("update cdbus_svcopts SET value='%s' WHERE svcid='%s' AND name='%s' AND value='%s'"
                   % (password, row.svcid, row.name, row.value))
            rows = sqlapi.SQL(sql) # pylint: disable=unused-variable
    if x:
        SUI.echo('')

def reset_password():
    sql = "angestellter set password='welcome', password_rule='Unsafe'"
    SUI.rst_title(u"Zurücksetzen der Benutzer-Passwörter")
    SUI.rst_p(u"Folgendes Statement setzt die Passwörter (welcome) der Benutzer in CDB::")
    SUI.rst_p(u"UPDATE " + sql, level=1)
    if SUI.ask_yes_no(u"Sollen die Passwörter zurückgesetzt werden?") == SUI.YES:
        rows = sqlapi.SQLupdate(sql)
        SUI.rst_p(u"-->%s rows updated" % rows)
    else:
        SUI.rst_p(u"Passwörter bleiben unverändert")
    SUI.wait_key()


def setup_basic_services():

    opt_query = """
   SELECT svcid, name, value
     FROM cdbus_svcopts WHERE svcid IN (
           SELECT svcid FROM cdbus_svcs
            WHERE svcname='%s'
             AND hostname='%s')"""

    hostname = FQDN

    svcname  = 'cdb.uberserver.Uberserver'
    SUI.rst_title(svcname)
    assert_service(svcname, hostname)
    opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
    check_login(opts)
    check_port(opts)
    opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
    print_opts(opts)

    svcname  = 'cdb.uberserver.services.blobstore.BlobStore'
    SUI.rst_title(svcname)
    assert_service(svcname, hostname)
    opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
    check_login(opts)
    check_port(opts)
    check_path(opts)
    opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
    print_opts(opts)

    svcname  = 'cdb.uberserver.services.apache.Apache'
    SUI.rst_title(svcname)
    assert_service(svcname, hostname)
    opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
    check_login(opts)
    check_port(opts)
    opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
    print_opts(opts)

    if ELEMENTS_MAJOR == 15 and ELEMENTS_MINOR >= 1:
        for svcname in ['cdb.uberserver.services.authentication.GateKeeper'
                        , 'cdb.uberserver.services.authentication.SessionCache']:
            SUI.rst_title(svcname)
            assert_service(svcname, hostname)
            opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
            check_login(opts)
            check_port(opts)
            opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
            print_opts(opts)

    else:
        svcname  = 'cdb.uberserver.services.server.Launcher'
        SUI.rst_title(svcname)
        assert_service(svcname, hostname)
        opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
        check_login(opts)
        check_port(opts)
        opts = sqlapi.RecordSet2(sql = opt_query % (svcname, hostname))
        print_opts(opts)


def _main(cliArgs): # pylint: disable=unused-argument
    _doc = __doc__.strip().split('\n')
    SUI.rst_title(_doc[0], level='part')
    SUI.rst_p('\n'.join(_doc[1:]))
    SUI.rst_p('ELEMENTS Version %s.%s' % (ELEMENTS_MAJOR, ELEMENTS_MINOR))
    if not SUI.ask_yes_no(u"Soll die DB initialisiert werden?", default='n'):
        SUI.echo("\nEND")
        return 42
    SUI.echo("")

    deactivate_services()
    takeover_service()
    setup_basic_services()
    auth_method()
    SUI.rst_p(u"""\
Ein minimales Setup wurde eingerichtet. Es kann der CDBSVCD gestartet werden.
Alle weiteren Einstellungen sollten von nun an in CDB möglich sein.""")
    return 0

def main():
    sys.exit(CLI(cmdFunc = _main)())
