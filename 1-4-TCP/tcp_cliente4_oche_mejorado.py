#!/usr/bin/env python3
"""Ejercicio 4 - Cliente que envía tres líneas seguidas y lee tres respuestas con recibe_mensaje().

Uso: python3 tcp_cliente4_oche_mejorado.py [ip] [puerto]   (por defecto localhost 9999)
"""
import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999


def recibe_mensaje(sock):
    """Devuelve una línea completa (bytes, con "\r\n"), leyendo byte a byte. b"" si se cierra."""
    buffer = []
    while True:
        byte = sock.recv(1)
        if byte == b"":
            return b""
        buffer.append(byte)
        if byte == b"\n" and len(buffer) >= 2 and buffer[-2] == b"\r":
            return b"".join(buffer)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, puerto))

for linea in ["UNO", "DOS", "TRES"]:
    sock.sendall(bytes(linea + "\r\n", "utf8"))

for _ in range(3):
    respuesta = recibe_mensaje(sock)
    print(repr(respuesta.decode("utf8")))

sock.close()
