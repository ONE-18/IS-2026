import socket
import sys

# Uso: python dns_getaddrinfo_wikipedia.py [4|6]   (por defecto IPv4)
version = sys.argv[1] if len(sys.argv) > 1 else "4"
familia = socket.AF_INET6 if version == "6" else socket.AF_INET

host = "en.wikipedia.org"
infos = socket.getaddrinfo(host, "www", familia, socket.SOCK_STREAM, socket.IPPROTO_TCP)
print("Opciones devueltas por getaddrinfo:", infos)

af, socktype, proto, canonname, sockaddr = infos[0]
s = socket.socket(af, socktype, proto)
s.connect(sockaddr)

peticion = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)
s.sendall(peticion.encode("ascii"))

respuesta = b""
while True:
    trozo = s.recv(4096)
    if not trozo:
        break
    respuesta += trozo
s.close()

print(respuesta.decode("utf-8", errors="replace"))
