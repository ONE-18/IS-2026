#!/usr/bin/env python3
"""Ejercicio 2 - Cliente que usa sendall() en lugar de send().

Uso:      python3 tcp_cliente2_sendall.py [ip] [puerto]  (por defecto localhost 9999)
Opcional: MENSAJE=ABCD python3 tcp_cliente2_sendall.py   (experimento con 4 bytes)
"""
import os
import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
texto = os.environ.get("MENSAJE", "ABCDE")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, puerto))

for _ in range(5):
    sock.sendall(bytes(texto, "ascii"))  # sendall repite send() hasta enviar todo
sock.sendall(b"FINAL")

sock.close()
