# Ejercicio 16: resumen de cada mensaje usando poplib + email
import email
import email.header
import getpass
import poplib


def imprime_resumen_mensaje(msg_bytes):
    msg = email.message_from_bytes(msg_bytes)
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")

    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))

    cuerpo = msg.get_payload()
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + str(parte_1)

    print("From:", remite)
    print("Subject:", asunto)
    print(cuerpo[:500])
    if len(cuerpo) > 500:
        print("...[omitido]")
    print("-" * 80)


server = "pop.gmail.com"
username = input("Usuario: ")
password = getpass.getpass("Contraseña de aplicación: ")

pop3_mail = poplib.POP3_SSL(server)
pop3_mail.user(username)
pop3_mail.pass_(password)

num_msgs, _ = pop3_mail.stat()
for i in range(1, num_msgs + 1):
    resp, lineas, octetos = pop3_mail.retr(i)
    imprime_resumen_mensaje(b"\r\n".join(lineas))

pop3_mail.quit()
