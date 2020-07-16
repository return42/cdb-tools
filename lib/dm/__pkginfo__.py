# -*- coding: utf-8; mode: python -*-
# pylint: disable=invalid-name,redefined-builtin
"""
python package meta informations
"""

package      = 'dm'
version      = '3.0'
authors      = ['Markus Heiser', ]
emails       = ['markus.heiser@darmarIT.de', ]
copyright    = '2020 Markus Heiser'
url          = 'https://github.com/return42/cdb-tools'
description  = 'Sammlung von Tools & Skripten zur Wartung einer CIM DATABASE Installation.'
license      = 'GPLv2'
keywords     = "CDB CIM DATABASE CONTACT ELEMENTS"

def get_entry_points():
    """get entry points of the python package"""
    return {
        'console_scripts': [
            'clean_cdb = dm.clean_cdb:main'
            , 'init_cdb_mirror = dm.init_cdb_mirror:main'
        ]}

install_requires = [
    "six" ]

classifiers = [
    "Development Status :: 5 - Production/Stable"
    , "Intended Audience :: Developers"
    , "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    , "Operating System :: OS Independent"
    , "Programming Language :: CDB Powerscript"
    , "Topic :: Utilities"
    , "Topic :: Software Development :: Tools" ]
