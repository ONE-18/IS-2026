# Ejercicio 1 (mejorado): descarta el mensaje de bienvenida con read_until
import getpass
import telnetlib

HOST = "localhost"
user = input("Usuario remoto: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(user.encode("ascii") + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode("ascii") + b"\n")

tn.read_until(b"$")          # Descarta bienvenida hasta el primer prompt
tn.write(b"ls /home\n")
tn.write(b"exit\n")
print(tn.read_all().decode("utf-8"))
