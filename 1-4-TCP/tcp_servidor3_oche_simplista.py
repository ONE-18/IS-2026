#!/usr/bin/env python3
"""Ejercicio 3 - Servicio "oche" (echo al revés), versión simplista.

Supone (erróneamente en general) que cada recv() devuelve exactamente una línea
terminada en "\r\n" y de menos de 80 bytes.

Uso:      python3 tcp_servidor3_oche_simplista.py [puerto]   (por defecto 9999)
Opcional: RETARDO=1 python3 tcp_servidor3_oche_simplista.py  (equivale al time.sleep(1) del experimento)
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
print("Servidor oche (simplista) escuchando en el puerto %d" % puerto)

while True:
    sd, origen = s.accept()
    print("Cliente conectado desde %s, %d" % origen)
    if retardo:
        time.sleep(retardo)

    while True:
        # Primero recibir el mensaje del cliente
        mensaje = sd.recv(80)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
        if mensaje == b"":  # Cadena vacía: el cliente cerró la conexión
            print("Cliente desconectado")
            sd.close()
            break
        mensaje = str(mensaje, "utf8")  # Convertir los bytes a caracteres
        # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
        linea = mensaje[:-2]
        # Tercero, darle la vuelta
        linea = linea[::-1]
        # Finalmente, enviar la respuesta con un fin de línea añadido
        sd.sendall(bytes(linea + "\r\n", "utf8"))
