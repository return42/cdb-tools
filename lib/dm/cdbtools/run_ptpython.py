#!/usr/bin/env python
u"""simple wrapper to start ptpython"""

from __future__ import absolute_import, unicode_literals

from ptpython.repl import embed, enable_deprecation_warnings, run_config

from fspath import FSPath

def main():
    u"""start ptpython"""
    cfg_dir  = FSPath('~/.ptpython').EXPANDUSER
    cfg_dir.makedirs()
    cfg_file = cfg_dir / 'config.py'

    enable_deprecation_warnings()

    # Apply config file
    def configure(repl):
        u"""load cfg"""
        if cfg_file.EXISTS:
            run_config(repl, cfg_file)
    embed(
        history_filename = cfg_dir/ 'history'
        , configure      = configure )

if __name__ == '__main__':
    main()
