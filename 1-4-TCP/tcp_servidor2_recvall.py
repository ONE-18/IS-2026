#!/usr/bin/env python3
"""Ejercicio 2 - Servidor con recvall(): lee exactamente N bytes aunque lleguen fraccionados.

Uso:      python3 tcp_servidor2_recvall.py [puerto]      (por defecto 9999)
Opcional: RETARDO=1 python3 tcp_servidor2_recvall.py
"""
import os
import socket
import sys
import time

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
retardo = float(os.environ.get("RETARDO", 0))


def recvall(sock, n):
    """Lee del socket exactamente n bytes (salvo que el otro extremo cierre).

    Intenta leer lo que falta de una vez (no byte a byte) y acumula los trozos
    en una lista, que es más eficiente que concatenar bytes inmutables.
    Si el otro extremo cierra antes de completar, devuelve lo que haya llegado.
    """
    partes = []
    restantes = n
    while restantes > 0:
        trozo = sock.recv(restantes)
        if trozo == b"":  # El otro extremo cerró la conexión
            break
        partes.append(trozo)
        restantes -= len(trozo)
    return b"".join(partes)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)
print("Servidor escuchando en el puerto %d" % puerto)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    if retardo:
        time.sleep(retardo)
    continuar = True

    while continuar:
        datos = recvall(sd, 5)
        texto = datos.decode("ascii", errors="replace")
        if len(datos) < 5:  # Cierre antes de completar el bloque
            if datos:
                print("Conexión cerrada con un bloque incompleto: %r" % texto)
            else:
                print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif texto == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % texto)
