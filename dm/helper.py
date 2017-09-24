# -*- coding: utf-8; mode: python -*-

import socket

def port_is_free(port):
    # prüft ob der Port des localhost noch frei ist
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', int(port)))
        sock.listen(5)
        sock.close()
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.bind(('::1', int(port)))
        sock.listen(5)
        sock.close()
    except socket.error:
        return False
    return True
