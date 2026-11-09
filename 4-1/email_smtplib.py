# Ejercicio 12: envío con smtplib
import email.message
import email.utils
import getpass
import smtplib

server = "smtp.gmail.com"
port = 587
username = input("Usuario (ej. tucuenta@gmail.com): ")
password = getpass.getpass("Contraseña de aplicación: ")
fromaddr = username
toaddr = input("Destinatario: ")

mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = 'Mensaje de prueba con smtplib'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba enviada con smtplib.")
binario = mensaje.as_bytes()   # aquí NO hace falta añadir el punto final

s = smtplib.SMTP(server, port)
s.set_debuglevel(1)
s.ehlo()
s.starttls()
s.ehlo()
s.login(username, password)
s.sendmail(fromaddr, [toaddr], binario)
s.quit()
