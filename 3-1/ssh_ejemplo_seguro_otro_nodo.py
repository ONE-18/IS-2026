# Ejercicio 11: igual que el seguro, pero contra el servidor de un compañero
import base64
import getpass
import paramiko
import time

HOST = "192.168.2.XX"                                   # <-- IP del compañero
CLAVE_PUBLICA_SERVIDOR = b'AAAAC3NzaC1lZDI1NTE5AAAA...'  # <-- su ssh_host_ed25519_key.pub

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_PUBLICA_SERVIDOR))
client.get_host_keys().add(HOST, 'ssh-ed25519', key)

clave = getpass.getpass(f"Clave de alumno en {HOST}: ")
client.connect(HOST, username='alumno', password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')
for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
