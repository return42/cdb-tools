# -*- coding: utf-8; mode: python -*-
u"""just some build tools"""
# pylint: disable=invalid-name

from __future__ import print_function

import sys
import os
import time
import zipfile
import re
import subprocess
import platform

from dm.cdbtools import (
    CDBTOOLS_HOME, CDBTOOLS_PY27, CDBTOOLS_CACHE, CDBTOOLS_DIST
    , CDBTOOLS_SW_DOWNLOAD, CDBTOOLS_PIP_DOWNLOAD, PIP_REQUIEMENTS)

CDBTOOLS_TEMPLATES = CDBTOOLS_HOME/'templates'

# die Versionsnummer bei github entspricht dem Tag und das hat immer ein
# führendes 'v' z.B. 'v1.0.0'
from dm import __pkginfo__ as pkginfo
download_url = 'https://github.com/return42/cdb-tools/releases/download/' + 'v' + pkginfo.version

from fspath import FSPath, CLI, OS_ENV, progressbar

if OS_ENV.get("CDBTOOLS_HOME", None) is None:
    raise Exception("Missing CDBTOOLS_HOME environment, can't build cdbtools without!")

# CDBTools environment


# python setup

PIP_PY_PLATFORM = 'win32'
PIP_PY_VERSION  = '27'

RE_SEP = re.escape(os.sep)
RE_TOP = "^" + RE_SEP

IGNORE_FOLDERS = [
    RE_SEP    + '__pycache__$'
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

_pip_download =  CDBTOOLS_PIP_DOWNLOAD.relpath(CDBTOOLS_HOME)

SOFTWARE_ARCHIVES = [

    # ( <relpath CDBTOOLS_HOME>, <zip-file name>
    #   , <RE_IGNORE_FOLDERS>, <RE_IGNORE_FILES>
    #   , <url without zip-file name>)
    ('.', "cdb-tools.zip", RE_IGNORE_FOLDERS, RE_IGNORE_FILES, download_url)
    , ('win_bin/ConEmu', 'ConEmu.zip', RE_IGNORE_FOLDERS, RE_IGNORE_FILES, download_url)
    #, (_pip_download, 'pip-download.zip', RE_IGNORE_FOLDERS, RE_IGNORE_FILES, download_url)

    , ]

# ==============================================================================
def main():
# ==============================================================================

    u"""cdbtools -- build maintenance script"""
    cli = CLI(description=main.__doc__)
    cli.addCMDParser(cli_build_get_pypkgs       , cmdName='get-pypkgs')
    cli.addCMDParser(cli_build_install_pypkgs   , cmdName='install-pypkgs')
    cli.addCMDParser(cli_build_get_software     , cmdName='get-software')
    cli.addCMDParser(cli_build_install_software , cmdName='install-software')
    cli.addCMDParser(cli_dist                   , cmdName='dist')
    cli()

def cli_build_install_software(cli): # pylint: disable=unused-argument
    u"""install software archieves (ZIP)"""
    CDBTOOLS_SW_DOWNLOAD.makedirs()
    for (src_folder, zip_fname, _x, _x, url) in SOFTWARE_ARCHIVES:
        if zip_fname == "cdb-tools.zip":
            # we are already in cdb-tools / no need to install once more
            continue
        sw_install(src_folder, zip_fname, url)

def cli_build_get_software(cli):  # pylint: disable=unused-argument
    u"""get software archieves (ZIP)"""
    CDBTOOLS_SW_DOWNLOAD.makedirs()
    for (_x, zip_fname, _x, _x, url) in SOFTWARE_ARCHIVES:
        if zip_fname == "cdb-tools.zip":
            # we are already in cdb-tools / no need to download once more
            continue
        sw_download(zip_fname, url)

def cli_build_install_pypkgs(cli):  # pylint: disable=unused-argument
    u"""install python requirements (pip download)"""
    pip  = FSPath(CDBTOOLS_PY27 / "bin" / "pip")
    if platform.system() == 'Windows':
        pip  = FSPath(CDBTOOLS_PY27 / "Scripts" / "pip.exe")
    proc =  subprocess.Popen(
        # https://pip.pypa.io/en/latest/reference/pip_download/#overview
        [ pip, 'install'
          , '--user'
          , '--no-index'
          , '--ignore-installed'
          , '--find-links', CDBTOOLS_PIP_DOWNLOAD
          ,  '-r'   , PIP_REQUIEMENTS ]
        , cwd = CDBTOOLS_HOME )
    retVal = proc.wait()
    return retVal

def cli_build_get_pypkgs(cli):  # pylint: disable=unused-argument
    u"""download python requirements (pip download)"""
    pip  = FSPath(CDBTOOLS_PY27 / "bin" / "pip")
    if platform.system() == 'Windows':
        pip  = FSPath(CDBTOOLS_PY27 / "Scripts" / "pip.exe")
    proc =  subprocess.Popen(
        # https://pip.pypa.io/en/latest/reference/pip_download/#overview
        [ pip, 'download'
          , '--dest'           , CDBTOOLS_PIP_DOWNLOAD
          , '--python-version' , PIP_PY_VERSION
          , '--platform'       , PIP_PY_PLATFORM
          , '--only-binary'    , ':all:'
          , '--requirement'    , PIP_REQUIEMENTS ]
        , cwd = CDBTOOLS_HOME )
    retVal = proc.wait()
    return retVal

def cli_dist(cli): # pylint: disable=unused-argument
    u"""build distribution"""
    # Software archives
    for (src_folder, zip_fname, ignore_folders, ignore_files, _x) in SOFTWARE_ARCHIVES:
        _zip(src_folder, CDBTOOLS_DIST / zip_fname, ignore_folders, ignore_files)
        print("")

def sw_download(zip_fname, url):
    u"""download file from url into CDBTOOLS_SW_DOWNLOAD"""
    url = url + "/" + zip_fname
    print("download: %s ..." % url)
    arch = CDBTOOLS_SW_DOWNLOAD / zip_fname
    if arch.EXISTS:
        print("  --> overwrite existing ZIP: %s" % zip_fname)
    arch.download(url, ticker=True)

def sw_install(src_folder, zip_fname, url):
    u"""Install zip_fname dwonloaded at CDBTOOLS_SW_DOWNLOAD into CDBTOOLS_HOME"""
    src_folder = FSPath(src_folder)
    print("install: %s" % src_folder)
    arch = CDBTOOLS_SW_DOWNLOAD / zip_fname
    if not arch.EXISTS:
        print("  missing %s" % zip_fname)
        sw_download(zip_fname, url)
    if (CDBTOOLS_HOME / src_folder).EXISTS:
        print("  %s already installed\n  --> to update first remove: %s\n  --> "
              % (zip_fname, CDBTOOLS_HOME / src_folder), end='')
        while (CDBTOOLS_HOME / src_folder).EXISTS:
            print(".", end='')
            time.sleep(1)
        print('')
    _unzip(arch, CDBTOOLS_HOME)
    print("install: %s OK" % src_folder)


def _unzip(arch, folder):
    myzip = zipfile.ZipFile(arch)
    ml = myzip.namelist()
    mx = len(ml) - 1
    zn = arch.BASENAME if len(arch.BASENAME) < 20 else arch.BASENAME[:18] + ".."
    for c, member in enumerate(ml):
        mn = FSPath(member).BASENAME
        mn = mn if len(mn) < 20 else mn[:18] + ".."
        progressbar(c, mx, prompt="  --> %s: %-20s" % (zn, mn))
        myzip.extract(member, folder)
    print("")

def _zip(src_folder, zip_fname, ignore_folders, ignore_files):
    u"""zip a ``src_folder`` relative to CDBTOOLS_HOME"""

    src_folder  = FSPath(src_folder)
    zip_fname   = FSPath(zip_fname)

    arch_prefix = src_folder
    src_abspath = CDBTOOLS_HOME / src_folder

    if src_abspath == CDBTOOLS_HOME:
        arch_prefix = "cdb-tools"

    zip_fname.DIRNAME.makedirs()

    def _ign_folder(folder):
        retVal = [x for x in ignore_folders if x.search("/" + folder)]
        return bool(retVal)

    def _ign_file(folder, fname):
        retVal = [x for x in ignore_files if x.search("/" + folder/fname)]
        return bool(retVal)

    if zip_fname.EXISTS:
        print("overwrite existing ZIP: %s" % zip_fname)
    else:
        print("create ZIP: %s" % zip_fname)

    with zipfile.ZipFile(zip_fname, 'w', zipfile.ZIP_DEFLATED) as myZIP:
        print("  compress folder: %s" % src_folder)
        ignored = []
        for folder, _drinames, filenames in src_abspath.walk():

            folder = folder.relpath(src_abspath)
            doIgn  = bool([x for x in ignored if folder[:len(x)] == x])
            if doIgn:
                continue
            if _ign_folder(src_folder/folder):
                print("    ignore folder  : %s"  % arch_prefix/folder)
                ignored.append(folder)
                continue
            #print("    archive folder : %s" % arch_prefix/folder )
            for fname in filenames:
                if _ign_file(src_folder/folder, fname):
                    #print("    ignore file    : %s" % arch_prefix/folder/fname)
                    continue
                src_name = src_abspath/folder/fname
                arc_name = arch_prefix/folder/fname
                if (CDBTOOLS_TEMPLATES/src_folder/folder/fname).EXISTS:
                    src_name = CDBTOOLS_TEMPLATES/src_folder/folder/fname
                    print("    use template of: %s"  % src_folder/folder/fname)
                myZIP.write(src_name, arc_name)


    print("  OK: %s" % zip_fname)

if __name__ == '__main__':
    sys.exit(main())
