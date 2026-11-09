# Experimento 2.1.3.1: sockets en crudo + función mostrar_hex
import socket

def mostrar_hex(datos):
    print(" ".join(format(b, "02X") for b in datos))

s = socket.socket()
s.connect(("localhost", 23))
respuesta = s.recv(1024)
mostrar_hex(respuesta)   # Esperable: FF FD 18 ... (IAC DO TERMINAL-TYPE, RFC 1091)
s.close()
