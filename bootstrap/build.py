# -*- coding: utf-8; mode: python -*-

import os
import zipfile
import re

from datetime import datetime
from fspath import FSPath


CDBTOOLS_HOME = FSPath(os.environ["CDBTOOLS_HOME"]).ABSPATH
CDBTOOLS_DIST = CDBTOOLS_HOME / "dist"
CDBTOOLS_ZIP  = CDBTOOLS_DIST / datetime.now().strftime("%Y%m%d_%H%M_cdb-tools.zip")

re_sep = re.escape(os.sep)
IGNORE_FOLDERS = [
    re_sep + '__pycache__$'
    , re_sep + '.cache$'
    , re_sep + '.cvsignore$'
    , re_sep + '.downloads$'
    #, re_sep + '.git$'
    , re_sep + '.svn$'
    , re_sep + '.tox$'
    , re_sep + 'build$'
    , 'dist$'
    , re_sep + 'gh-pages$'
    , re_sep + 'local$'
    , re_sep + 'py_dist$'
    , ]

IGNORE_FILES   = [
    r'.*~$'
    , r'\.#*$'
    , r'.DS_Store'
    , r'.*\.pyc$'
    #, r'.*\.elc$'
    , ]

IGNORE_FOLDERS = [ re.compile(x) for x in IGNORE_FOLDERS]
IGNORE_FILES = [ re.compile(x) for x in IGNORE_FILES]

CDBTOOLS_DIST.makedirs()

def ignore_folder(folder):
    retVal = [x for x in IGNORE_FOLDERS if x.search(folder)]
    return bool(retVal)

def ignore_file(folder, fname):
    retVal = [x for x in IGNORE_FILES if x.search(folder/fname)]
    return bool(retVal)

print("create ZIP: %s" % CDBTOOLS_ZIP)

with zipfile.ZipFile(CDBTOOLS_ZIP, 'w', zipfile.ZIP_DEFLATED) as cdbToolsZIP:
    print("  compress folder: %s" % CDBTOOLS_HOME)

    ignored = []
    for folder, dirnames, filenames in CDBTOOLS_HOME.ABSPATH.walk():
        folder = folder.relpath(CDBTOOLS_HOME.ABSPATH)
        doIgn  = bool([x for x in ignored if folder[:len(x)] == x])
        #import pdb; pdb.set_trace()
        if doIgn:
            continue

        if ignore_folder(folder):
            print("    ignore folder  : %s"  % folder)
            ignored.append(folder)
            continue

        #print("    archive folder : %s" % FSPath("cdb-tools") / folder )
        for fname in filenames:
            if ignore_file(folder, fname):
                #print("    ignore file    : %s"  % folder / fname)
                continue
            src_name = CDBTOOLS_HOME.ABSPATH / folder / fname
            arc_name = FSPath("cdb-tools") / folder / fname
            cdbToolsZIP.write(src_name, arc_name)


print("build: %s" % CDBTOOLS_ZIP)

