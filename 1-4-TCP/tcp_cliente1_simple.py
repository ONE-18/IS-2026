#!/usr/bin/env python3
"""Ejercicio 1 - Cliente para el servidor simple.

Uso:      python3 tcp_cliente1_simple.py [ip] [puerto]   (por defecto localhost 9999)
Opcional: MENSAJE=ABCD python3 tcp_cliente1_simple.py    (experimento: enviar 4 bytes en vez de 5)
"""
import os
import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
texto = os.environ.get("MENSAJE", "ABCDE")  # exactamente 5 bytes por defecto


def enviar(sock, texto):
    """Envía todos los bytes con un bucle sobre send() (send puede enviar menos de lo pedido)."""
    mensaje = bytes(texto, "ascii")
    while mensaje != b"":
        enviados = sock.send(mensaje)
        mensaje = mensaje[enviados:]  # Reasignar los restantes


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, puerto))

for _ in range(5):
    enviar(sock, texto)
enviar(sock, "FINAL")

sock.close()
