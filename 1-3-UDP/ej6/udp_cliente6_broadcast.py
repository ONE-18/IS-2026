import socket
import sys

# Uso: python udp_cliente6_broadcast.py [ip_broadcast] [puerto]
IP_BROADCAST = "255.255.255.255"
PUERTO = 12345
if len(sys.argv) > 1:
    IP_BROADCAST = sys.argv[1]
if len(sys.argv) > 2:
    PUERTO = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# 1. Enviar el datagrama por broadcast
s.sendto("BUSCANDO HOLA".encode("utf8"), (IP_BROADCAST, PUERTO))

# 2. y 3. Recibir respuestas hasta que expire el timeout
s.settimeout(2)
primero = None
while True:
    try:
        datagrama, origen = s.recvfrom(1024)
    except socket.timeout:
        break
    texto = datagrama.decode("utf8")
    if texto == "IMPLEMENTO HOLA":
        print("Servidor encontrado:", origen[0])
        if primero is None:
            primero = origen

# 4. Probar el servicio con el primer servidor que respondió
if primero is None:
    print("No ha respondido ningún servidor")
else:
    print("Probando el servicio con", primero[0])
    s.sendto("HOLA".encode("utf8"), primero)
    s.settimeout(2)
    try:
        datagrama, origen = s.recvfrom(1024)
        print("Respuesta:", datagrama.decode("utf8"))
    except socket.timeout:
        print("El servidor no respondió al HOLA")
