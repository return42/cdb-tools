# -*- coding: utf-8; mode: python -*-

from __future__ import print_function

import sys
import os
import time
import zipfile
import re

from datetime import datetime
from fspath import FSPath, CLI, OS_ENV

if OS_ENV.get("CDBTOOLS_HOME", None) is None:
    raise Exception("Missing CDBTOOLS_HOME environment, can't build cdbtools without!")

CDBTOOLS_HOME  = FSPath(os.environ["CDBTOOLS_HOME"]).ABSPATH
CDBTOOLS_DIST  = CDBTOOLS_HOME / "dist"
CDBTOOLS_CACHE = CDBTOOLS_HOME / ".cache"

SOFTWARE_ARCHIVES = (
    ('win_bin/ConEmu', 'ConEmu.zip', 'https://storage/SoftwareDB/darmarIT/cdb-tools')
    , )

RE_SEP = re.escape(os.sep)
RE_TOP = "^" + RE_SEP
IGNORE_FOLDERS = [
    RE_SEP    + '__pycache__$'
    #, RE_TOP + '.cache$'
    , RE_SEP  + '.cache$'
    , RE_SEP  + '.cvsignore$'
    , RE_SEP  + '.downloads$'
    #, RE_SEP + '.git$'
    , RE_SEP  + '.svn$'
    , RE_SEP  + '.tox$'
    , RE_SEP  + 'build$'
    , RE_SEP  + 'dist$'
    , RE_SEP  + 'gh-pages$'
    , RE_SEP  + 'local$'
    , RE_SEP  + 'py_dist$'
    , ]

IGNORE_FILES = [
    r'.*~$'
    , r'\.#*$'
    , r'.DS_Store'
    , r'.*\.pyc$'
    #, r'.*\.elc$'
    , ]

RE_IGNORE_FOLDERS = [ re.compile(x) for x in IGNORE_FOLDERS]
RE_IGNORE_FILES   = [ re.compile(x) for x in IGNORE_FILES]

# ==============================================================================
def main():
# ==============================================================================

    u"""cdbtools -- build maintenance script"""
    cli = CLI(description=main.__doc__)
    cmd = cli.addCMDParser(cli_dist, cmdName='dist')
    cmd = cli.addCMDParser(cli_zip_cdbtools, cmdName='zip-cdbtools')
    cmd = cli.addCMDParser(cli_build_zip_software, cmdName='zip-software')
    cmd = cli.addCMDParser(cli_build_get_software, cmdName='get-software')
    cmd = cli.addCMDParser(cli_build_install_software, cmdName='install-software')
    cli()

def cli_dist(cli):
    u"""build distribution"""
    cli_build_zip_software(cli)
    cli_zip_cdbtools(cli)

def cli_zip_cdbtools(cli):
    u"""build complete zip"""
    zip_fname  = CDBTOOLS_DIST / datetime.now().strftime("%Y%m%d_%H%M_cdb-tools.zip")
    do_zip(zip_fname, CDBTOOLS_HOME, FSPath("cdb-tools"))


def cli_build_zip_software(cli):
    u"""build software archieves (ZIP)"""
    for src_folder, zip_fname, url in SOFTWARE_ARCHIVES:
        do_zip(CDBTOOLS_DIST / zip_fname, CDBTOOLS_HOME / src_folder, FSPath(src_folder))

def cli_build_get_software(cli):
    u"""get software archieves (ZIP)"""
    sw_folder = CDBTOOLS_CACHE / "software"
    sw_folder.makedirs()

    for src_folder, zip_fname, url in SOFTWARE_ARCHIVES:
        url = url + "/" + zip_fname
        arch = sw_folder / zip_fname
        if arch.EXISTS:
            print("overwrite existing ZIP: %s" % zip_fname)
        arch.download(url, ticker=True)

def cli_build_install_software(cli):
    u"""get software archieves (ZIP)"""
    sw_folder = CDBTOOLS_CACHE / "software"

    if not sw_folder.EXISTS:
        raise IOError("missing downloaded software in %s" % sw_folder)

    for src_folder, zip_fname, url in SOFTWARE_ARCHIVES:
        src_folder = FSPath(src_folder)
        print("install: %s" % src_folder)
        arch = sw_folder / zip_fname
        if not arch.EXISTS:
            print("  missing %s\n  --> can't install: %s\n  --> to update run download first"
                  % (zip_fname, src_folder))
            print("FAILED: %s" % src_folder)
            continue
        if (CDBTOOLS_HOME / src_folder).EXISTS:
            print("  %s already installed\n  --> to update first remove: %s\n  --> "
                  % (zip_fname, CDBTOOLS_HOME / src_folder), end='')
            while (CDBTOOLS_HOME / src_folder).EXISTS:
                print(".", end='')
                time.sleep(1)
            print('')

        myzip = zipfile.ZipFile(arch)
        for member in myzip.namelist():
            myzip.extract(member, CDBTOOLS_HOME)

        print("OK: %s" % src_folder)

def do_zip(zip_fname, src_folder, arch_prefix, ignore_folders=None, ignore_files=None):

    if ignore_files is None:
        ignore_files   = RE_IGNORE_FILES
    if ignore_folders is None:
        ignore_folders = RE_IGNORE_FOLDERS

    zip_fname.DIRNAME.makedirs()

    def ignore_folder(folder):
        retVal = [x for x in ignore_folders if x.search("/" + folder)]
        return bool(retVal)

    def ignore_file(folder, fname):
        retVal = [x for x in ignore_files if x.search("/" + folder/fname)]
        return bool(retVal)

    if zip_fname.EXISTS:
        print("overwrite existing ZIP: %s" % zip_fname)
    else:
        print("create ZIP: %s" % zip_fname)

    with zipfile.ZipFile(zip_fname, 'w', zipfile.ZIP_DEFLATED) as myZIP:
        print("  compress folder: %s" % src_folder)

        ignored = []
        for folder, dirnames, filenames in src_folder.ABSPATH.walk():
            folder = folder.relpath(src_folder.ABSPATH)
            doIgn  = bool([x for x in ignored if folder[:len(x)] == x])
            #import pdb; pdb.set_trace()
            if doIgn:
                continue


            if ignore_folder(folder):
                print("    ignore folder  : %s"  % folder)
                ignored.append(folder)
                continue

            #print("    archive folder : %s" % arch_prefix / folder )
            for fname in filenames:
                if ignore_file(folder, fname):
                    #print("    ignore file    : %s"  % folder / fname)
                    continue
                src_name = src_folder.ABSPATH / folder / fname
                arc_name = arch_prefix / folder / fname
                myZIP.write(src_name, arc_name)


    print("build: %s" % zip_fname)

if __name__ == '__main__':
    sys.exit(main())
