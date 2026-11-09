# Ejercicio 13: descargar todos los ficheros regulares de una carpeta remota
# Uso: python sftp_descarga.py carpeta_remota
import base64
import getpass
import os
import sys
from stat import S_ISDIR
import paramiko

HOST = "localhost"
CLAVE_PUBLICA_SERVIDOR = b'AAAAC3NzaC1lZDI1NTE5AAAA...'

carpeta = sys.argv[1] if len(sys.argv) > 1 else input("Carpeta remota: ")

c = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_PUBLICA_SERVIDOR))
c.get_host_keys().add(HOST, 'ssh-ed25519', key)
c.connect(HOST, username='alumno', password=getpass.getpass("Clave: "))

sftp = c.open_sftp()
sftp.chdir(carpeta)
for nombre in sftp.listdir():
    if S_ISDIR(sftp.stat(nombre).st_mode):
        print("Salto la carpeta:", nombre)
        continue
    sftp.get(nombre, os.path.join(".", nombre))
    print("Descargado:", nombre)

sftp.close()
c.close()
