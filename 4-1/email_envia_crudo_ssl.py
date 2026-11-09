# Ejercicio 11: SMTP en crudo contra Gmail con STARTTLS + AUTH LOGIN
# Usa una "contraseña de aplicación" de Google, no tu contraseña normal.
import base64
import email.message
import email.policy
import email.utils
import getpass
import socket
import ssl
import sys


def RecvReply(sock, codigo):
    respuesta = sock.recv(1024)
    print("S:", respuesta.decode("utf-8", errors="replace"), end="")
    if respuesta[:3] != codigo:
        print("Error: se esperaba", codigo, "y se recibió", respuesta[:3])
        sys.exit(1)
    return respuesta


server = "smtp.gmail.com"
port = 587
username = input("Usuario (ej. tucuenta@gmail.com): ")
password = getpass.getpass("Contraseña de aplicación: ")

fromaddr = username
toaddr = input("Destinatario: ")
subject = "Mensaje de prueba por Gmail"
data = "Esto es una prueba enviada con SMTP + STARTTLS."

mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)
binario = mensaje.as_bytes(policy=email.policy.SMTP) + b"\r\n.\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
RecvReply(s, b"220")

s.send(b"EHLO mimaquina\r\n")
RecvReply(s, b"250")

s.send(b"STARTTLS\r\n")
RecvReply(s, b"220")

context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# Tras STARTTLS el estándar exige repetir EHLO sobre el canal seguro
sc.send(b"EHLO mimaquina\r\n")
RecvReply(sc, b"250")

sc.send(b"AUTH LOGIN\r\n")
RecvReply(sc, b"334")

sc.send(base64.b64encode(username.encode("ascii")) + b'\r\n')
RecvReply(sc, b"334")
sc.send(base64.b64encode(password.encode("utf8")) + b'\r\n')
RecvReply(sc, b"235")

sc.send(b"MAIL From:<" + fromaddr.encode() + b">\r\n")
RecvReply(sc, b"250")

sc.send(b"RCPT To:<" + toaddr.encode() + b">\r\n")
RecvReply(sc, b"250")

sc.send(b"DATA\r\n")
RecvReply(sc, b"354")

sc.sendall(binario)
RecvReply(sc, b"250")

sc.send(b"QUIT\r\n")
RecvReply(sc, b"221")
sc.close()
