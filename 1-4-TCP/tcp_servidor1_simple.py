#!/usr/bin/env python3
"""Ejercicio 1 - Servidor TCP simple (mensajes de tamaño prefijado: 5 bytes).

Uso:      python3 tcp_servidor1_simple.py [puerto]      (por defecto 9999)
Opcional: RETARDO=1 python3 tcp_servidor1_simple.py     (pausa tras el accept, para el experimento)
"""
import os
import socket
import sys
import time

puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
retardo = float(os.environ.get("RETARDO", 0))

# Creación del socket de escucha (SOCK_STREAM = TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Permite relanzar el servidor sin esperar a que el SO libere el puerto
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Asignarle puerto
s.bind(("", puerto))
# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()
print("Servidor escuchando en el puerto %d" % puerto)

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    if retardo:
        time.sleep(retardo)  # Experimento: dejar que se acumulen envíos del cliente
    continuar = True

    # Bucle de atención al cliente conectado
    while continuar:
        datos = sd.recv(5)  # Observar que se lee del socket sd, no de s
        datos = datos.decode("ascii", errors="replace")  # Pasar los bytes a caracteres
        if datos == "":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)
