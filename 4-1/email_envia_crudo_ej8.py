# Ejercicios 8 y 9: igual que email_envia_crudo.py pero con el módulo email
# (si lo prefieres, guárdalo con el nombre email_envia_crudo.py)
import email.message
import email.policy
import email.utils
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
toaddr = "tu_usuario@uniovi.es"     # <-- cámbialo (prueba también con una de gmail)
subject = "Mensaje de prueba con tildes: ñandú"
data = "Esto es una prueba, con acentuación."
adjunto = None  # Ejercicio 9: pon "logoatc.gif" para enviar el adjunto

mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)

if adjunto:
    with open(adjunto, "rb") as f:
        mensaje.add_attachment(f.read(), "image", "gif", filename="atc.gif")

# policy.SMTP usa \r\n como fin de línea
binario = mensaje.as_bytes(policy=email.policy.SMTP)
binario += b"\r\n.\r\n"

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

s.sendall(binario)
RecvReply(s, b"250")

s.send(b"QUIT\r\n")
RecvReply(s, b"221")
s.close()
