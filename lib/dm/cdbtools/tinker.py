# -*- mode: python; coding: utf-8 -*-
u"""Bastelecke
"""
# ==============================================================================
# imports
# ==============================================================================

import os

from ptpdb import set_trace as BREAK

from fspath import FSPath
from fspath.sui import SUI
from fspath.cli import CLI

from cdb import CADDOK

# ==============================================================================
def cli_collect_pdf(cli):
# ==============================================================================
    u"""Sammelt die Dateien aus der CDB-Infrastruktur in einem Ordner.

    Es werden alle CDB-Ordner durchwandert und die PDF Dateien die dort gefunden
    werden in einem Ordner zusammengeführt. Eigentlich kann man die ganze
    Dokumentation auch über das Dok-Portal von CDB recherchieren, ich mag es
    aber alle PDFs in einem Ordner zu haben, auf den ich ohne eine laufende CDB
    Instanz zugreifen kann.
    """
    SUI.rst_title(u"Einsammeln der PDF Dateien", level='part')
    SUI.rst_p("Ziel Ordner: %s" % cli.dest)
    if cli.dest.EXISTS:
        raise cli.Error(42, "Ordner %s existiert bereits" % cli.dest)
    cli.dest.makedirs()
    for folder in [FSPath(CADDOK.BASE), FSPath(CADDOK.RUNTIME)]:
        for pdf_f in folder.reMatchFind(".*\\.pdf"):
            x = pdf_f.split(os.sep)
            if x[-3] in ('de', 'en') and x[-2] == 'html':
                _dest = cli.dest / pdf_f.FILENAME + "_" + x[-3] + pdf_f.SUFFIX
                SUI.echo("cp --> %s" %(_dest))
                _dest.DIRNAME.makedirs()
                pdf_f.copyfile(_dest)
            else:
                SUI.echo("ignore: %s" % pdf_f)


# ==============================================================================
def main():
# ==============================================================================

    cli = CLI(description=__doc__)

    parser = cli.addCMDParser(cli_collect_pdf, cmdName='collect-pdf')
    parser.add_argument(
        'dest', type=FSPath, default = FSPath('./pdf')
        , help = 'Ziel Ordner in dem die PDFs abgelegt werden sollen')
    cli()

if __name__ == '__main__':
    sys.exit(main())
