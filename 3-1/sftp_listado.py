# Ejercicio 12: listado de la carpeta del usuario por sftp
import base64
import getpass
import paramiko

HOST = "localhost"
CLAVE_PUBLICA_SERVIDOR = b'AAAAC3NzaC1lZDI1NTE5AAAA...'

c = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_PUBLICA_SERVIDOR))
c.get_host_keys().add(HOST, 'ssh-ed25519', key)
c.connect(HOST, username='alumno', password=getpass.getpass("Clave: "))

sftp = c.open_sftp()
for nombre in sftp.listdir():      # SSH ya fija la carpeta del usuario
    print(nombre)

sftp.close()
c.close()
