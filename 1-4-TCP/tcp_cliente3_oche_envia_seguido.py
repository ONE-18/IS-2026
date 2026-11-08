#!/usr/bin/env python3
"""Ejercicio 3 (experimento) - Envía tres líneas seguidas y DESPUÉS lee tres respuestas.

Las respuestas pueden llegar "pegadas" en el primer recv(), de modo que los
siguientes recv() se quedarían bloqueados. Para no colgarnos para siempre se
usa un timeout de 3 segundos.

Uso: python3 tcp_cliente3_oche_envia_seguido.py [ip] [puerto]
"""
import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
sock.connect((ip, puerto))

for linea in ["UNO", "DOS", "TRES"]:
    sock.sendall(bytes(linea + "\r\n", "utf8"))

for i in range(3):
    try:
        respuesta = sock.recv(80)
        print("Respuesta %d: %r" % (i + 1, str(respuesta, "utf8")))  # repr() muestra los \r\n
    except socket.timeout:
        print("Respuesta %d: TIMEOUT (todo llegó junto en un recv anterior)" % (i + 1))

sock.close()
