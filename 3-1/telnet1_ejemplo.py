# Ejercicio 1: listado de /home por telnet
import getpass
import telnetlib   # Python <= 3.12 (ver nota sobre 3.13)

HOST = "localhost"          # En Windows: la IP del servidor Unix
user = input("Usuario remoto: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(user.encode("ascii") + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode("ascii") + b"\n")

tn.write(b"ls /home\n")
tn.write(b"exit\n")
print(tn.read_all().decode("utf-8"))
