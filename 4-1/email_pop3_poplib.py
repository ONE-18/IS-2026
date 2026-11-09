# Ejercicio 15: POP3 con poplib
import getpass
import poplib

server = "pop.gmail.com"
username = input("Usuario: ")
password = getpass.getpass("Contraseña de aplicación: ")

pop3_mail = poplib.POP3_SSL(server)
pop3_mail.set_debuglevel(2)

pop3_mail.user(username)
pop3_mail.pass_(password)

num_msgs, tam_total = pop3_mail.stat()
print("Mensajes:", num_msgs, "Tamaño total:", tam_total)

if num_msgs > 0:
    # retr devuelve (respuesta, [líneas en bytes], octetos)
    resp, lineas, octetos = pop3_mail.retr(1)
    for linea in lineas:
        print(linea.decode("utf-8", errors="replace"))

pop3_mail.quit()
