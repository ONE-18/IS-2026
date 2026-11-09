# Ejercicio 7: envío SMTP "en crudo" con plantilla de texto
import socket
import sys


def RecvReply(sock, codigo):
    respuesta = sock.recv(1024)
    print("S:", respuesta.decode("utf-8", errors="replace"), end="")
    if respuesta[:3] != codigo:
        print("Error: se esperaba", codigo, "y se recibió", respuesta[:3])
        sys.exit(1)
    return respuesta


server = "relay.uniovi.es"
port = 25
fromaddr = "tu_usuario@uniovi.es"   # <-- cámbialo
toaddr = "tu_usuario@uniovi.es"     # <-- cámbialo
subject = "Mensaje de prueba"
data = "Esto es una prueba"

message = "To: %s\r\nFrom: %s\r\nSubject: %s\r\n\r\n%s\r\n.\r\n" % (
    toaddr, fromaddr, subject, data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
RecvReply(s, b"220")

s.send(b"HELO mimaquina\r\n")
RecvReply(s, b"250")

s.send(b"MAIL From:<" + fromaddr.encode() + b">\r\n")
RecvReply(s, b"250")

s.send(b"RCPT To:<" + toaddr.encode() + b">\r\n")
RecvReply(s, b"250")

s.send(b"DATA\r\n")
RecvReply(s, b"354")

s.send(message.encode("utf-8"))
RecvReply(s, b"250")

s.send(b"QUIT\r\n")
RecvReply(s, b"221")
s.close()
