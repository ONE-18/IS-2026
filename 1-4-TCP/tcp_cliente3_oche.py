#!/usr/bin/env python3
"""Ejercicio 3 - Cliente de prueba: envía una línea, lee su respuesta, y así sucesivamente.

Uso: python3 tcp_cliente3_oche.py [ip] [puerto]   (por defecto localhost 9999)
"""
import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, puerto))

for linea in ["HOLA", "Ingeniería de Servicios", "UNO"]:
    sock.sendall(bytes(linea + "\r\n", "utf8"))
    respuesta = sock.recv(80)
    print("Enviado: %-25r Recibido: %r" % (linea, str(respuesta, "utf8")))

sock.close()
