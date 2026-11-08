#!/usr/bin/env python3
"""Ejercicio 6 - "oche" con la longitud del mensaje enviada antes, en ASCII y terminada en "\n".

Formato de cada mensaje (en ambos sentidos):   "<longitud en bytes>\n" + <mensaje en UTF-8>
Ejemplo: "HOLA" -> b"4\nHOLA"

Uso:      python3 tcp_servidor6_oche_len.py [puerto]   (por defecto 9999)
Opcional: RETARDO=1 python3 tcp_servidor6_oche_len.py
"""
import os
import socket
import sys
import time

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
retardo = float(os.environ.get("RETARDO", 0))


def recibe_mensaje(f):
    """Lee la longitud (hasta "\n") y después exactamente esos bytes. Devuelve str, o None si se cierra."""
    cabecera = f.readline()  # f es un fichero binario ("rb")
    if cabecera == b"":
        return None
    longitud = int(cabecera)  # ValueError si la cabecera no es un número
    datos = f.read(longitud)  # En un fichero con buffer, read(n) espera hasta tener n bytes
    if len(datos) < longitud:  # Cierre a mitad de mensaje
        return None
    return datos.decode("utf8")


def envia_mensaje(sock, mensaje):
    datos = mensaje.encode("utf8")
    longitud = "%d\n" % len(datos)  # Longitud en BYTES, no en caracteres
    sock.sendall(longitud.encode("ascii") + datos)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)
print("Servidor oche (longitud ASCII) escuchando en el puerto %d" % puerto)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    if retardo:
        time.sleep(retardo)
    f = sd.makefile("rb")  # Todas las lecturas deben pasar por f (tiene el buffer)

    try:
        while True:
            mensaje = recibe_mensaje(f)
            if mensaje is None:
                print("Cliente desconectado")
                break
            envia_mensaje(sd, mensaje[::-1])
    except ValueError:
        print("Cabecera de longitud inválida: se cierra la conexión")
    finally:
        f.close()
        sd.close()
