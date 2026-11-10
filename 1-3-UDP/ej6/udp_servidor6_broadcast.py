import socket
import sys

PUERTO = 12345
if len(sys.argv) > 1:
    PUERTO = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # modo broadcast
s.bind(("", PUERTO))
print("Servidor HOLA escuchando en el puerto", PUERTO)

while True:
    datagrama, origen = s.recvfrom(1024)
    texto = datagrama.decode("utf8").strip()
    print("Recibido", repr(texto), "de", origen)

    if texto == "BUSCANDO HOLA":
        s.sendto("IMPLEMENTO HOLA".encode("utf8"), origen)
    elif texto == "HOLA":
        respuesta = "HOLA: " + origen[0]  # IP del cliente
        s.sendto(respuesta.encode("utf8"), origen)
    else:
        print("Datagrama no reconocido, se ignora")

