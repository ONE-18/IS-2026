# Ejercicio 10: política por defecto (rechazar) + registrar la clave pública del servidor
# Obtén la clave con:  cat /etc/ssh/ssh_host_ed25519_key.pub
# Formato: "ssh-ed25519 AAAAC3Nza... root@maquina"  -> copia solo la parte AAAA...
import base64
import getpass
import paramiko
import time

CLAVE_PUBLICA_SERVIDOR = b'AAAAC3NzaC1lZDI1NTE5AAAA...'   # <-- PEGAR AQUÍ

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_PUBLICA_SERVIDOR))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)

clave = getpass.getpass("Clave de alumno: ")
client.connect('localhost', username='alumno', password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')
for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
