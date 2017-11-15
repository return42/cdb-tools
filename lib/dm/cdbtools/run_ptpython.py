#!/usr/bin/env python
u"""simple wrapper to start ptpython"""

from __future__ import absolute_import, unicode_literals

from ptpython.repl import embed, enable_deprecation_warnings, run_config

from dm.cdbtools import CDBTOOLS_HOME, CDBTOOLS_CACHE

def main():
    u"""start ptpython"""
    pt_dir   = CDBTOOLS_CACHE/'.ptpython'
    cfg_file = CDBTOOLS_HOME/'bootstrap'/'ptpython_config.py'

    enable_deprecation_warnings()

    # Apply config file
    def configure(repl):
        u"""load cfg"""
        if cfg_file.EXISTS:
            run_config(repl, cfg_file)
    embed(
        history_filename = pt_dir/'history'
        , configure      = configure )

if __name__ == '__main__':
    main()
