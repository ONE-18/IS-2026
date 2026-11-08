#!/usr/bin/env python3
"""Ejercicio 7 (opcional) - Cliente "oche" con longitud binaria de 2 bytes big endian.

Uso: python3 tcp_cliente7_opcional.py [ip] [puerto]   (por defecto localhost 9999)
"""
import socket
import struct
import sys

ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999


def recvall(sock, n):
    partes = []
    restantes = n
    while restantes > 0:
        trozo = sock.recv(restantes)
        if trozo == b"":
            break
        partes.append(trozo)
        restantes -= len(trozo)
    return b"".join(partes)


def envia_mensaje(sock, mensaje):
    datos = mensaje.encode("utf8")
    sock.sendall(struct.pack(">H", len(datos)) + datos)


def recibe_mensaje(sock):
    cabecera = recvall(sock, 2)
    if len(cabecera) < 2:
        return None
    (longitud,) = struct.unpack(">H", cabecera)
    datos = recvall(sock, longitud)
    return datos.decode("utf8") if len(datos) == longitud else None


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, puerto))

mensajes = ["UNO", "DOS", "TRES", "Ingeniería de Servicios", "x" * 1000]
for m in mensajes:
    envia_mensaje(sock, m)
for m in mensajes:
    r = recibe_mensaje(sock)
    print("%r -> %r" % (m if len(m) < 40 else m[:10] + "...", r if len(r) < 40 else r[:10] + "..."))

sock.close()
