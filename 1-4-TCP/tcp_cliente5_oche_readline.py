#!/usr/bin/env python3
"""Ejercicio 5 - Cliente "oche" que recibe con makefile() + readline().

Uso: python3 tcp_cliente5_oche_readline.py [ip] [puerto]   (por defecto localhost 9999)
"""
import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, puerto))
f = sock.makefile(encoding="utf8", newline="\r\n")

for linea in ["UNO", "DOS", "TRES"]:
    sock.sendall(bytes(linea + "\r\n", "utf8"))

for _ in range(3):
    print(repr(f.readline()))

f.close()
sock.close()
