# -*- coding: utf-8; mode: python -*-

import os
import sys
import socket
import inspect

from fspath import debug

HOSTNAME = socket.gethostname()
CDBTOOLS_DEBUG_ADDR = os.environ.get("CDBTOOLS_DEBUG_ADDR", "127.0.0.1")
CDBTOOLS_DEBUG_PORT = int(os.environ.get("CDBTOOLS_DEBUG_PORT", 4444))

def breakpoint(port=CDBTOOLS_DEBUG_PORT, addr=CDBTOOLS_DEBUG_ADDR):
    bp = debug.RemotePdb(port, addr)
    bp.set_trace(frame = inspect.currentframe().f_back)

def client(port=CDBTOOLS_DEBUG_PORT, addr=CDBTOOLS_DEBUG_ADDR, polltime=None):
    sys.stderr.write(
        "debug client listening on address/port: %s:%s" % (addr, port))
    debug.rtrace_client(port, addr, polltime)
