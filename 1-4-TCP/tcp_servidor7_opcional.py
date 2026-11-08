#!/usr/bin/env python3
"""Ejercicio 7 (opcional) - "oche" con la longitud en binario: 2 bytes, big endian (struct ">H").

Formato de cada mensaje:  <2 bytes: longitud> + <mensaje en UTF-8>   (máx. 65535 bytes)

Uso:      python3 tcp_servidor7_opcional.py [puerto]   (por defecto 9999)
Opcional: RETARDO=1 python3 tcp_servidor7_opcional.py
"""
import os
import socket
import struct
import sys
import time

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
retardo = float(os.environ.get("RETARDO", 0))


def recvall(sock, n):
    """Lee exactamente n bytes (o menos si el otro extremo cierra)."""
    partes = []
    restantes = n
    while restantes > 0:
        trozo = sock.recv(restantes)
        if trozo == b"":
            break
        partes.append(trozo)
        restantes -= len(trozo)
    return b"".join(partes)


def recibe_mensaje(sock):
    cabecera = recvall(sock, 2)  # Siempre 2 bytes: no hace falta terminador
    if len(cabecera) < 2:
        return None
    (longitud,) = struct.unpack(">H", cabecera)  # unpack devuelve una TUPLA
    datos = recvall(sock, longitud)
    if len(datos) < longitud:
        return None
    return datos.decode("utf8")


def envia_mensaje(sock, mensaje):
    datos = mensaje.encode("utf8")
    if len(datos) > 0xFFFF:
        raise ValueError("Mensaje demasiado largo para 2 bytes de longitud")
    sock.sendall(struct.pack(">H", len(datos)) + datos)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)
print("Servidor oche (longitud binaria) escuchando en el puerto %d" % puerto)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    if retardo:
        time.sleep(retardo)

    while True:
        mensaje = recibe_mensaje(sd)
        if mensaje is None:
            print("Cliente desconectado")
            sd.close()
            break
        envia_mensaje(sd, mensaje[::-1])
