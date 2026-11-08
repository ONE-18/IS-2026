#!/usr/bin/env python3
"""Ejercicio 4 - Servicio "oche" con recibe_mensaje(): lee byte a byte hasta "\r\n".

Uso:      python3 tcp_servidor4_oche_mejorado.py [puerto]   (por defecto 9999)
Opcional: RETARDO=1 python3 tcp_servidor4_oche_mejorado.py
"""
import os
import socket
import sys
import time

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
retardo = float(os.environ.get("RETARDO", 0))
FIN = b"\r\n"


def recibe_mensaje(sock):
    """Devuelve una línea completa (bytes, incluido el "\r\n" final).

    Lee de byte en byte y acumula en una lista (eficiente en Python).
    Devuelve b"" si el otro extremo cierra la conexión.
    """
    buffer = []
    while True:
        byte = sock.recv(1)
        if byte == b"":  # Conexión cerrada
            return b""
        buffer.append(byte)
        if byte == b"\n" and len(buffer) >= 2 and buffer[-2] == b"\r":
            return b"".join(buffer)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)
print("Servidor oche (mejorado) escuchando en el puerto %d" % puerto)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    if retardo:
        time.sleep(retardo)

    while True:
        mensaje = recibe_mensaje(sd)
        if mensaje == b"":
            print("Cliente desconectado")
            sd.close()
            break
        linea = mensaje.decode("utf8")[:-2]  # Quitar el \r\n
        sd.sendall(bytes(linea[::-1] + "\r\n", "utf8"))
