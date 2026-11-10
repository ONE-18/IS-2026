import getpass
import telnetlib

HOST = "192.168.1.144"   # Cambiar por la IP del servidor

user = input("Usuario remoto: ")
password = getpass.getpass("Clave: ")

tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(user.encode("ascii") + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode("ascii") + b"\n")

tn.read_until(b"$")
tn.write(b"docker ps -a --format '{{.Names}}|{{.Status}}'\n")
respuesta = tn.read_until(b"$")
tn.write(b"exit\n")
tn.read_all()
tn.close()

contenedores = []
for linea in respuesta.decode("utf-8", errors="replace").splitlines():
    if "|" not in linea:
        continue
    nombre, estado = linea.split("|", maxsplit=1)
    if not nombre or any(caracter.isspace() for caracter in nombre):
        continue
    if not estado.startswith("Up"):
        contenedores.append((nombre, estado))

if contenedores:
    print("Contenedores detenidos o no ejecutándose:")
    for nombre, estado in contenedores:
        print(f"- {nombre}: {estado}")
else:
    print("No hay contenedores detenidos o no ejecutándose.")
