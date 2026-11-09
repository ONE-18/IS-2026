# Ejercicio 14: Subject y From de TODOS los mensajes
import email
import email.header
import getpass
import socket
import ssl
import sys


def RecvReply(sock):
    respuesta = sock.recv(1024)
    print("S:", respuesta.decode("utf-8", errors="replace"), end="")
    if respuesta[:3] != b"+OK":
        print("Error en la respuesta del servidor")
        sys.exit(1)
    return respuesta


def recibe_multilinea(sock):
    datos = b""
    while not datos.endswith(b"\r\n.\r\n"):
        trozo = sock.recv(4096)
        if not trozo:
            break
        datos += trozo
    if datos[:3] != b"+OK":
        print("Error:", datos[:100])
        sys.exit(1)
    return datos


def decodifica(valor):
    return str(email.header.make_header(email.header.decode_header(valor)))


server = "pop.gmail.com"
port = 995
username = input("Usuario: ")
password = getpass.getpass("Contraseña de aplicación: ")

s = socket.socket()
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)
RecvReply(sc)

sc.send(b"USER " + username.encode() + b"\r\n")
RecvReply(sc)
sc.send(b"PASS " + password.encode() + b"\r\n")
RecvReply(sc)

sc.send(b"STAT\r\n")
num_msgs = int(RecvReply(sc).split()[1])
print("Mensajes disponibles:", num_msgs)

for i in range(1, num_msgs + 1):
    sc.send(b"TOP " + str(i).encode() + b" 0\r\n")   # solo cabeceras
    datos = recibe_multilinea(sc)
    crudo = datos.split(b"\r\n", 1)[1]
    msg = email.message_from_bytes(crudo)
    print(f"--- Mensaje {i} ---")
    print("From:", decodifica(msg.get("From", "<desconocido>")))
    print("Subject:", decodifica(msg.get("Subject", "<sin asunto>")))

sc.send(b"QUIT\r\n")
RecvReply(sc)
sc.close()
