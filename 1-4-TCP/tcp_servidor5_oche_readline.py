#!/usr/bin/env python3
"""Ejercicio 5 - Servicio "oche" usando makefile() + readline().

Uso:      python3 tcp_servidor5_oche_readline.py [puerto]   (por defecto 9999)
Opcional: RETARDO=1 python3 tcp_servidor5_oche_readline.py
"""
import os
import socket
import sys
import time

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
retardo = float(os.environ.get("RETARDO", 0))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)
print("Servidor oche (readline) escuchando en el puerto %d" % puerto)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    if retardo:
        time.sleep(retardo)

    # "Convertimos" el socket en un fichero: readline() gestiona el buffer y la decodificación
    f = sd.makefile(encoding="utf8", newline="\r\n")

    while True:
        mensaje = f.readline()  # str, incluye el \r\n final
        if mensaje == "":  # Fin de fichero: el cliente cerró
            print("Cliente desconectado")
            break
        linea = mensaje[:-2]  # Quitar \r\n
        sd.sendall(bytes(linea[::-1] + "\r\n", "utf8"))

    f.close()
    sd.close()
