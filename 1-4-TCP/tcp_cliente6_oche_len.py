#!/usr/bin/env python3
"""Ejercicio 6 - Cliente "oche" con longitud ASCII + "\n" delante de cada mensaje.

(En el enunciado el fichero aparece como tcp_cliente.6_oche_len.py; aquí sin el punto.)

Uso: python3 tcp_cliente6_oche_len.py [ip] [puerto]   (por defecto localhost 9999)
"""
import socket
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999


def envia_mensaje(sock, mensaje):
    datos = mensaje.encode("utf8")
    longitud = "%d\n" % len(datos)
    sock.sendall(longitud.encode("ascii") + datos)


def recibe_mensaje(f):
    cabecera = f.readline()
    if cabecera == b"":
        return None
    longitud = int(cabecera)
    datos = f.read(longitud)
    if len(datos) < longitud:
        return None
    return datos.decode("utf8")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, puerto))
f = sock.makefile("rb")

mensajes = ["UNO", "DOS", "TRES", "Ingeniería de Servicios", "línea\ncon salto"]
for m in mensajes:  # Enviamos todo seguido...
    envia_mensaje(sock, m)
for m in mensajes:  # ...y leemos después las respuestas
    print("%r -> %r" % (m, recibe_mensaje(f)))

f.close()
sock.close()
